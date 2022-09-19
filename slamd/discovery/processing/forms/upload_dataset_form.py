from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

from slamd.discovery.processing.forms.validation import DatasetNameIsUnique


class UploadDatasetForm(Form):

    dataset = FileField(
        label='CSV File Upload',
        validators=[
            FileRequired(message='Please select a file to upload'),
            FileAllowed(['csv'], message='Only CSV files are allowed'),
            DatasetNameIsUnique('The chosen filename is already in use. Please rename the file.')
        ]
    )

    upload_button = SubmitField('Upload dataset')
