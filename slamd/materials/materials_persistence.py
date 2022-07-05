from flask import session

from slamd.materials.material_type import MaterialType


class MaterialsPersistence:

    @classmethod
    def save(cls, material_type, material):
        before = cls.query_by_type(material_type)

        if not before:
            session[f'{material_type.lower()}_list'] = [material]
        else:
            session[f'{material_type.lower()}_list'].append(material)

    @classmethod
    def find_all(cls):
        all_materials = []
        all_material_types = MaterialType.get_all_types()
        for material_type in all_material_types:
            all_materials.extend(session.get(f'{material_type.lower()}_list', []))
        return all_materials

    @classmethod
    def query_by_type(cls, material_type):
        return session.get(f'{material_type.lower()}_list', [])

    @classmethod
    def delete_by_type_and_uuid(cls, material_name, uuid):
        materials = cls.query_by_type(material_name)
        remaining_materials = list(filter(lambda material: material.get('uuid') != uuid, materials))
        session[f'{material_name.lower()}_list'] = remaining_materials
