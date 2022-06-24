from flask_wtf import FlaskForm as Form
from wtforms import DecimalField, StringField

from slamd.materials.forms.base_materials_form import BaseMaterialsForm


class AggregatesForm(BaseMaterialsForm):

    fine_aggregates = DecimalField(label='Fine Aggregates')

    coarse_aggregates = DecimalField(label='Coarse Aggregates')

    type = StringField(label='Type')

    grading_curve = StringField(label='Grading Curve')
