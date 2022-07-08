from flask_wtf import FlaskForm as Form
from wtforms import FieldList, FormField
from wtforms import StringField


class MinMaxEntriesForm:

    name = StringField('Name')
    min = StringField('Min')
    max = StringField('Name')


class MinMaxForm(Form):

    all_min_max_entries = FieldList(FormField(MinMaxEntriesForm))
