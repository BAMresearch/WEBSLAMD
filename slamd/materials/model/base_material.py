class BaseMaterial:

    def _init__(self, name, type, costs, additional_properties, is_blended=False):
        self.name = name
        self.type = type
        self.costs = costs
        self.additional_properties = additional_properties
        self.is_blended = is_blended


class Costs:

    def __init__(self, co2_footprint, costs, delivery_time):
        self.delivery_time = delivery_time
        self.costs = costs
        self.co2_footprint = co2_footprint
