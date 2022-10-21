from io import BytesIO

import pandas as pd


class ExcelStrategy:

    @classmethod
    def create_prediction_excel(cls, dataset_of_prediction, prediction):
        original_data = dataset_of_prediction.dataframe
        prediction_df = prediction.dataframe
        metadata_df = pd.DataFrame({k: pd.Series(v) for k, v in prediction.metadata.items()})

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            original_data.to_excel(writer, sheet_name='Original Data')
            prediction_df.to_excel(writer, sheet_name='Predictions')
            metadata_df.to_excel(writer, sheet_name='Metadata')
        output.seek(0)
        return output
