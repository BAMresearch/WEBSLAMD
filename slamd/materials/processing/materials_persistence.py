from flask import session

from slamd.materials.processing.material_type import MaterialType


class MaterialsPersistence:

    @classmethod
    def find_all_materials(cls):
        all_material_types = MaterialType.get_all_materials()
        all_materials = [cls.query_by_type(material_type) for material_type in all_material_types]
        return all_materials

    @classmethod
    def find_all_processes(cls):
        return cls.query_by_type('process')

    @classmethod
    def save(cls, material_type, material):
        before = cls.query_by_type(material_type)

        if not before:
            cls.set_session_property(material_type, [material])
        elif not cls.query_by_type_and_uuid(material_type, str(material.uuid)):
            cls.extend_session_property(material_type, material)

    @classmethod
    def query_by_type(cls, material_type):
        return MaterialsPersistence.get_session_property(material_type)

    @classmethod
    def query_by_type_and_uuid(cls, material_type, uuid):
        """
        Return the first element matching the given uuid and material_type.
        Return None if no matching element was found.
        """
        materials = MaterialsPersistence.get_session_property(material_type)
        for material in materials:
            if str(material.uuid) == uuid:
                return material
        # Nothing found
        return None

    @classmethod
    def delete_by_type_and_uuid(cls, material_type, uuid_as_str):
        materials = cls.query_by_type(material_type)
        remaining_materials = [material for material in materials if str(material.uuid) != uuid_as_str]
        cls.set_session_property(material_type, remaining_materials)

    # Wrappers for session logic. This way we can easily mock the methods in tests without any need for creating a proper
    # context and session. Check test_materials_persistence for examples.

    @classmethod
    def get_session_property(cls, material_type):
        return session.get(f'{material_type.lower()}_list', [])

    @classmethod
    def set_session_property(cls, material_type, materials):
        session[f'{material_type.lower()}_list'] = materials

    @classmethod
    def extend_session_property(cls, material_type, material):
        session[f'{material_type.lower()}_list'].append(material)
