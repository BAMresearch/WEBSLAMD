from werkzeug.utils import secure_filename

from slamd.discovery.processing.models.dataset import Dataset
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence


class CsvStrategy:

    @classmethod
    def create_dataset(cls, file_data):
        # Generate a safe filename for the new dataset
        file_name = secure_filename(file_data.filename)
        # Read the entire file into a string
        file_content = file_data.read().decode('utf-8')
        # Assume the first line contains the headers
        headers, content = file_content.split('\n', 1)
        # Parse the column names
        columns = headers.split(',')
        return Dataset(name=file_name, columns=columns, content=content)

    @classmethod
    def save_dataset(cls, dataset):
        DiscoveryPersistence.save_dataset(dataset)
