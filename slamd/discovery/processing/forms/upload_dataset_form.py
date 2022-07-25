from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


class UploadDatasetForm(Form):

    dataset = FileField(
        label='CSV File Upload',
        validators=[
            FileRequired(),
            FileAllowed(['csv'], message='Only CSV files are allowed')
        ]
    )

    upload_button = SubmitField('Upload dataset')
