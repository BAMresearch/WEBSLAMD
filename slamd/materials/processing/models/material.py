import uuid


class Material:

    def __init__(self, name='', type='', costs=None, additional_properties=None, is_blended=False, blending_ratios=''):
        self.uuid = uuid.uuid1()
        self.name = name
        self.type = type
        self.costs = costs
        self.additional_properties = additional_properties
        self.is_blended = is_blended
        self.blending_ratios = blending_ratios


class Costs:

    def __init__(self, co2_footprint=0, costs=0, delivery_time=0):
        self.delivery_time = delivery_time
        self.costs = costs
        self.co2_footprint = co2_footprint
