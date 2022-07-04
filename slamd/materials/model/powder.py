from slamd.materials.model.base_material import BaseMaterial


class Powder(BaseMaterial):

    def __init__(self, composition=None, structure=None):
        self.structure = structure
        self.composition = composition


class Composition:

    def __init__(self, fe3_o2=0, si_o2=0):
        self.fe3_o2 = fe3_o2
        self.si_o2 = si_o2


class Structure:

    def __init__(self, fine=0, gravity=0):
        self.fine = fine
        self.gravity = gravity
