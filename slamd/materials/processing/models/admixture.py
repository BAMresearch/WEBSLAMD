from slamd.materials.processing.models.material import Material


class Admixture(Material):

    def __init__(self, composition=None, type=None):
        super().__init__()
        self.composition = composition
        self.type = type
