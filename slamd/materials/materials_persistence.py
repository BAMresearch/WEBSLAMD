from flask import session

from slamd.materials.material_type import MaterialType


class MaterialsPersistence:

    @classmethod
    def find_all(cls):
        all_materials = []
        all_material_types = MaterialType.get_all_types()
        for material_type in all_material_types:
            all_materials.extend(session.get(f'{material_type.lower()}_list', []))
        return all_materials

    @classmethod
    def save(cls, material_type, material):
        before = cls.find_by_type(material_type)

        if not before:
            session[f'{material_type.lower()}_list'] = [material]
        else:
            session[f'{material_type.lower()}_list'].append(material)

    @classmethod
    def find_by_type(cls, material_type):
        return session.get(f'{material_type.lower()}_list', [])
