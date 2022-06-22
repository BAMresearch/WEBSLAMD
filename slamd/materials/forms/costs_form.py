from flask_wtf import FlaskForm as Form
from wtforms import DecimalField, IntegerField


class CostsForm(Form):

    co2_footprint = DecimalField(label='CO2-Footprint')

    costs = DecimalField(label='Costs')

    delivery_time = IntegerField(label='Delivery time')
