from flask import session


class MaterialsPersistence:

    @classmethod
    def save(cls, material_type, material):
        before = cls.query_by_type(material_type)

        if not before:
            session[f'{material_type.lower()}_list'] = [material]
        else:
            session[f'{material_type.lower()}_list'].append(material)

    @classmethod
    def query_by_type(cls, material_type):
        return session.get(f'{material_type.lower()}_list', [])
