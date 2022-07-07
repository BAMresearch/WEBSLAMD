from slamd.materials.processing.models.material import Material


class Process(Material):

    def __init__(self, duration=None, temperature=None, relative_humidity=None):
        super().__init__()
        self.duration = duration
        self.temperature = temperature
        self.relative_humidity = relative_humidity
