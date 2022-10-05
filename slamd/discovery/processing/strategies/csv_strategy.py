import pandas as pd
from pandas import read_csv
from werkzeug.utils import secure_filename
from csv import Sniffer

from slamd.common.error_handling import ValueNotSupportedException, SlamdRequestTooLargeException, \
    SlamdUnprocessableEntityException
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.models.dataset import Dataset


class CsvStrategy:

    CSV_DELIM_SAMPLE_BYTES = 10000
    CSV_DELIM_SAMPLE_LINES = 2

    @classmethod
    def create_dataset(cls, file_data):
        # Generate a safe filename for the new dataset
        file_name = secure_filename(file_data.filename)

        try:
            delimiter = cls._determine_delimiter(file_data)
        except:
            raise SlamdUnprocessableEntityException(message='Could not parse the given CSV file.')

        decimal = '.'
        if delimiter == ';':
            decimal = ','

        if file_name == 'temporary.csv':
            raise ValueNotSupportedException('You cannot use the name temporary for your dataset!')

        try:
            dataset = Dataset(
                name=file_name,
                dataframe=read_csv(file_data, delimiter=delimiter, decimal=decimal, on_bad_lines='error')
            )
        except:
            raise ValueNotSupportedException('The dataset you submitted could not be read.')

        for col in dataset.dataframe.columns:
            # errors='ignore' => If non-numeric columns can not be converted, they are returned without conversion
            dataset.dataframe[col] = pd.to_numeric(dataset.dataframe[col], errors='ignore')

        return dataset

    @classmethod
    def save_dataset(cls, dataset):
        DiscoveryPersistence.save_dataset(dataset)

    @classmethod
    def to_csv(cls, dataset):
        return dataset.dataframe.to_csv(index=False, na_rep='NaN')

    @classmethod
    def _determine_delimiter(cls, file_data):
        head = file_data.read(cls.CSV_DELIM_SAMPLE_BYTES).decode('utf-8')

        if head.count('\n') < cls.CSV_DELIM_SAMPLE_LINES:
            if not file_data.read():
                # eof
                raise SlamdUnprocessableEntityException('The csv file you tried to upload does not contain enough '
                                                        'rows.')
            else:
                raise SlamdRequestTooLargeException('The csv file you tried to upload is too large or has too many '
                                                    'columns.')

        file_data.seek(0)   # reset file pointer to avoid side effects

        # csv.Sniffer() works best when reading at least the first two lines.
        split_head = head.split('\n')
        sample = '\n'.join(split_head[cls.CSV_DELIM_SAMPLE_LINES:])
        return Sniffer().sniff(sample).delimiter
