from slamd.materials.processing.models.material import Material


class Process(Material):

    def __init__(self, name='', type='', costs=None, duration=None, temperature=None, relative_humidity=None, additional_properties=None):
        super().__init__(name=name, type=type, costs=costs,
                         additional_properties=additional_properties)
        self.duration = duration
        self.temperature = temperature
        self.relative_humidity = relative_humidity
