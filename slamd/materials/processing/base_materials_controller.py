from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from slamd.materials.processing.base_materials_service import BaseMaterialService
from slamd.materials.processing.forms.powder_form import PowderForm

base_materials = Blueprint('base_materials', __name__,
                           template_folder='../templates',
                           static_folder='../static',
                           static_url_path='static',
                           url_prefix='/materials/base')

base_materials_service = BaseMaterialService()


@base_materials.route('', methods=['GET'])
def base_material_page():
    materials_response = base_materials_service.list_materials(blended=False)
    return render_template('base_materials.html', form=PowderForm(), materials_response=materials_response)


@base_materials.route('/<type>', methods=['GET'])
def select_base_material_type(type):
    template_file, form = base_materials_service.create_material_form(type)
    body = {'template': render_template(template_file, form=form)}
    return make_response(jsonify(body), 200)


@base_materials.route('/add_property/<new_property_index>', methods=['GET'])
def add_property(new_property_index):
    """
    Return HTML for an additional property form.
    The <input> tags generated here must have different 'name' and 'id' attributes.
    We use indexes starting from zero to name them differently.
    The format matches what WTForms does when rendering a FieldList.
    """
    body = {'template': render_template('add_property_form.html', index=new_property_index)}
    return make_response(jsonify(body), 200)


@base_materials.route('', methods=['POST'])
def submit_base_material():
    valid, form = base_materials_service.save_material(request.form)

    if valid:
        return redirect('/')

    materials_response = base_materials_service.list_materials(blended=False)
    return render_template('base_materials.html', form=form, materials_response=materials_response)

@base_materials.route('/<material_type>/<uuid>', methods=['GET'])
def populate_base_material_form(material_type, uuid):
    form = base_materials_service.populate_form(material_type, uuid)
    all_materials = base_materials_service.list_all()
    return render_template('base_materials.html', form=form, all_materials=all_materials)

@base_materials.route('/<material_type>/<uuid>', methods=['DELETE'])
def delete_base_material(material_type, uuid):
    all_base_materials = base_materials_service.delete_material(material_type, uuid)

    body = {'template': render_template('materials_table.html', materials_response=all_base_materials)}
    return make_response(jsonify(body), 200)
