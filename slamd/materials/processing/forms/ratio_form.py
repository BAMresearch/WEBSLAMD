from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from wtforms import StringField


class RatioEntriesForm(Form):

    ratio = StringField(
        'Ratio',
        validators=[])


class RatioForm(Form):
    all_ratio_entries = FieldList(FormField(RatioEntriesForm), min_entries=0)
