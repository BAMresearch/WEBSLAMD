from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from wtforms import StringField


class WeightsEntriesForm(Form):

    idx = StringField()

    weights = StringField(
        label='Weights',
        validators=[]
    )


class WeightsForm(Form):
    all_weights_entries = FieldList(FormField(WeightsEntriesForm), min_entries=0)
