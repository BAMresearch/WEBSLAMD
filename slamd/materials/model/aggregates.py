from slamd.materials.model.base_material import BaseMaterial


class Aggregates(BaseMaterial):

    def __init__(self, composition=None):
        self.composition = composition


class Composition:

    def __init__(self, fine_aggregates=None, coarse_aggregates=None, fa_density=None, ca_density=None):
        self.fine_aggregates = fine_aggregates
        self.coarse_aggregates = coarse_aggregates
        self.fa_density = fa_density
        self.ca_density = ca_density
