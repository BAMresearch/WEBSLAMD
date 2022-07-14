from flask import session


class MaterialsPersistence:

    @classmethod
    def save(cls, material_type, material):
        before = cls.query_by_type(material_type)

        if not before:
            cls.set_session_property(material_type, [material])
        else:
            cls.extend_session_property(material_type, material)

    @classmethod
    def query_by_type(cls, material_type):
        return MaterialsPersistence.get_session_property(material_type)

    @classmethod
    def query_by_type_and_uuid(cls, material_type, uuid):
        materials = MaterialsPersistence.get_session_property(material_type)
        return list(filter(lambda material: str(material.uuid) == uuid, materials))

    @classmethod
    def delete_by_type_and_uuid(cls, material_type, uuid):
        materials = cls.query_by_type(material_type)
        remaining_materials = list(
            filter(lambda material: str(material.uuid) != uuid, materials))
        cls.set_session_property(material_type, remaining_materials)

    """
    Wrappers for session logic. This way we can easily mock the methods in tests without any need for creating a proper
    context and session. Check test_materials_persistence for examples.
    """
    @classmethod
    def get_session_property(cls, material_type):
        return session.get(f'{material_type.lower()}_list', [])

    @classmethod
    def set_session_property(cls, material_type, materials):
        session[f'{material_type.lower()}_list'] = materials

    @classmethod
    def extend_session_property(cls, material_type, material):
        session[f'{material_type.lower()}_list'].append(material)
