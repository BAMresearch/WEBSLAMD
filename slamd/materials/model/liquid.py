from slamd.materials.model.base_material import BaseMaterial


class Liquid(BaseMaterial):

    def __init__(self, composition=None):
        super().__init__()
        self.composition = composition


class Composition:

    def __init__(self, na2_si_o3=None, na_o_h=None, na2_si_o3_specific=None,
                 na_o_h_specific=None, total=None, na2_o=None, si_o2=None, h2_o=None,
                 na2_o_dry=None, si_o2_dry=None, water=None, na_o_h_total=None):
        self.na2_si_o3 = na2_si_o3
        self.na_o_h = na_o_h
        self.na2_si_o3_specific = na2_si_o3_specific
        self.na_o_h_specific = na_o_h_specific
        self.total = total
        self.na2_o = na2_o
        self.si_o2 = si_o2
        self.h2_o = h2_o
        self.na2_o_dry = na2_o_dry
        self.si_o2_dry = si_o2_dry
        self.water = water
        self.na_o_h_total = na_o_h_total
