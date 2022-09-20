from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, StringField, validators


class WeightsEntriesForm(Form):

    idx = StringField()

    weights = StringField(
        label='Weights',
        validators=[validators.DataRequired(message='Weight cannot be empty')]
    )


class WeightsForm(Form):
    all_weights_entries = FieldList(FormField(WeightsEntriesForm), min_entries=0)
