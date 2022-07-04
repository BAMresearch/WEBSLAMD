from slamd.materials.model.base_material import BaseMaterial


class Liquid(BaseMaterial):

    def __init__(self, composition=None):
        self.composition = composition


class Composition:

    def __init__(self, na2_si_o3=0, na_o_h=0, na2_si_o3_specific=0,
                 na_o_h_specific=0, total=0, na2_o=0, si_o2=0, h2_o=0,
                 na2_o_dry=0, si_o2_dry=0, water=0, na_o_h_total=0):
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
