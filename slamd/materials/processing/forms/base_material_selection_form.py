from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField


class BaseMaterialSelectionForm(Form):

    base_material_selection = SelectMultipleField(
        label='3 - Base materials *',
        validators=[validators.DataRequired(message='Select at least two base materials')],
        choices=[]
    )
