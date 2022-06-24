from slamd.materials.model.base_material import BaseMaterial


class Powder(BaseMaterial):

    def __init__(self, composition, structure):
        self.structure = structure
        self.composition = composition


class Composition:

    def __init__(self, feo, sio):
        self.feo = feo
        self.sio = sio


class Structure:

    def __init__(self, fine, gravity):
        self.fine = fine
        self.gravity = gravity
