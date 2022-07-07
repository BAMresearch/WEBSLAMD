from slamd.materials.processing.models.material import Material


class Aggregates(Material):

    def __init__(self, composition=None):
        super().__init__()
        self.composition = composition


class Composition:

    def __init__(self, fine_aggregates=None, coarse_aggregates=None, fa_density=None, ca_density=None):
        self.fine_aggregates = fine_aggregates
        self.coarse_aggregates = coarse_aggregates
        self.fa_density = fa_density
        self.ca_density = ca_density
