from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField, StringField, validators, DecimalRangeField


class WeightsEntriesForm(Form):

    idx = StringField()

    weights = StringField(
        label='Weights',
        validators=[validators.DataRequired(message='Weight cannot be empty')]
    )


class WeightsForm(Form):

    all_weights_entries = FieldList(FormField(WeightsEntriesForm), min_entries=0)

    sampling_size_slider = DecimalRangeField(
        label='Specify ratio of combinations to include:',
        default=1.00,
        places=2,
        validators=[
            validators.NumberRange(min=0, max=1, message='The sampling value should be between 0 and 1')
        ]
    )
