from slamd.materials.model.base_material import BaseMaterial


class Admixture(BaseMaterial):

    def __init__(self, composition=None, type=None):
        super().__init__()
        self.composition = composition
        self.type = type
