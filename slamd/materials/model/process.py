from slamd.materials.model.base_material import BaseMaterial


class Process(BaseMaterial):

    def __init__(self, duration=None, temperature=None, relative_humidity=None):
        super().__init__()
        self.duration = duration
        self.temperature = temperature
        self.relative_humidity = relative_humidity
