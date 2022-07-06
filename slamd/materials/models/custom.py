from slamd.materials.models.material import Material


class Custom(Material):

    def __init__(self, name=None, value=None):
        super().__init__()
        self.name = name
        self.value = value
