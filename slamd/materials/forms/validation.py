from flask import session
from wtforms import ValidationError


def name_is_unique(form, field):
    name_of_new_material = field.data
    type_of_new_material = form['material_type'].data

    saved_materials_of_given_type = f'{type_of_new_material.lower()}s'
    materials_of_given_type = session.get(saved_materials_of_given_type, None)
    if materials_of_given_type is not None:
        materials_of_type = session[saved_materials_of_given_type]
        material_names = list(map(lambda material: material.name, materials_of_type))
        if name_of_new_material in material_names:
            raise ValidationError('The chosen name is already in use. Please use a unique name.')
        else:
            print('VALID')
