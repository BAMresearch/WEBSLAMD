from slamd.materials.model.base_material import BaseMaterial


class Powder(BaseMaterial):

    def __init__(self, composition=None, structure=None):
        self.structure = structure
        self.composition = composition


class Composition:

    def __init__(self, feo=0, sio=0):
        self.feo = feo
        self.sio = sio


class Structure:

    def __init__(self, fine=0, gravity=0):
        self.fine = fine
        self.gravity = gravity
