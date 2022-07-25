from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from wtforms import StringField


class WeightsEntriesForm(Form):

    ratio = StringField(
        'Weigths',
        validators=[])


class WeightsForm(Form):
    all_weights_entries = FieldList(FormField(WeightsEntriesForm), min_entries=0)
