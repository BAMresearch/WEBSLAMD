from flask_wtf import FlaskForm as Form
from wtforms import DecimalField, StringField


class AggregatesForm(Form):

    fine_aggregates = DecimalField(label='Fine Aggregates')

    coarse_aggregates = DecimalField(label='Coarse Aggregates')

    type = StringField(label='Type')

    grading_curve = StringField(label='Grading Curve')
