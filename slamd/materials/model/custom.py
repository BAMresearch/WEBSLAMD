from slamd.materials.model.base_material import BaseMaterial


class Custom(BaseMaterial):

    def __init__(self, name=None, value=None):
        super().__init__()
        self.name = name
        self.value = value
