from wtforms import ValidationError

from slamd.materials.materials_persistence import MaterialsPersistence


def name_is_unique(form, field):
    name_of_new_material = field.data
    type_of_new_material = form['material_type'].data

    materials_of_given_type = MaterialsPersistence.find_by_type(type_of_new_material)
    if materials_of_given_type:
        material_names = list(map(lambda material: material.name, materials_of_given_type))
        if name_of_new_material in material_names:
            raise ValidationError('The chosen name is already in use. Please use a unique name.')
