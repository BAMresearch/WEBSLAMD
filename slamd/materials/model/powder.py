from slamd.materials.model.base_material import BaseMaterial


class Powder(BaseMaterial):

    def __init__(self, composition=None, structure=None):
        super().__init__()
        self.structure = structure
        self.composition = composition


class Composition:

    def __init__(self, fe3_o2=None, si_o2=None, al2_o3=None, ca_o=None, mg_o=None, na2_o=None,
                 k2_o=None, s_o3=None, ti_o2=None, p2_o5=None, sr_o=None, mn2_o3=None):
        self.fe3_o2 = fe3_o2
        self.si_o2 = si_o2
        self.al2_o3 = al2_o3
        self.ca_o = ca_o
        self.mg_o = mg_o
        self.na2_o = na2_o
        self.k2_o = k2_o
        self.s_o3 = s_o3
        self.ti_o2 = ti_o2
        self.p2_o5 = p2_o5
        self.sr_o = sr_o
        self.mn2_o3 = mn2_o3


class Structure:

    def __init__(self, fine=None, gravity=None):
        self.fine = fine
        self.gravity = gravity
