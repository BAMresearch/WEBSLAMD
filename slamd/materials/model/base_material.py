class BaseMaterial:

    def _init__(self, name='', type='', costs=None, additional_properties=None, is_blended=False):
        self.name = name
        self.type = type
        self.costs = costs
        self.additional_properties = additional_properties
        self.is_blended = is_blended


class Costs:

    def __init__(self, co2_footprint=0, costs=0, delivery_time=0):
        self.delivery_time = delivery_time
        self.costs = costs
        self.co2_footprint = co2_footprint