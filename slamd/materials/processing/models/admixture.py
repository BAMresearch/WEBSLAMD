from slamd.materials.processing.models.material import Material


class Admixture(Material):

    def __init__(self, name='', type='', costs=None, composition=None, admixture_type=None, additional_properties=None):
        super().__init__(name=name, type=type, costs=None)
        self.composition = composition
        self.admixture_type = admixture_type
        self.additional_properties = additional_properties
