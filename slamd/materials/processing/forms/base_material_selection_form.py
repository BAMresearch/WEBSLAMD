from flask_wtf import FlaskForm as Form
from wtforms import validators, SelectMultipleField


class BaseMaterialSelectionForm(Form):

    base_material_selection = SelectMultipleField(
        label='Base materials',
        validators=[validators.DataRequired()],
        choices=[]
    )
