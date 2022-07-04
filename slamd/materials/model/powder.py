from slamd.materials.model.base_material import BaseMaterial


class Powder(BaseMaterial):

    def __init__(self, composition=None, structure=None):
        self.structure = structure
        self.composition = composition


class Composition:

    def __init__(self, fe3_o2=0, si_o2=0, al2_o3=0, ca_o=0, mg_o=0, na2_o=0,
                 k2_o=0, s_o3=0, ti_o2=0, p2_o5=0, sr_o=0, mn2_o3=0):
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

    def __init__(self, fine=0, gravity=0):
        self.fine = fine
        self.gravity = gravity
