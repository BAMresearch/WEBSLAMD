from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.processing.base.base_materials_service import BaseMaterialService

base_materials = Blueprint('materials', __name__,
                           template_folder='../../templates',
                           static_folder='../../static',
                           static_url_path='static',
                           url_prefix='/materials/base')

base_materials_service = BaseMaterialService()


@base_materials.route('', methods=['GET'])
def material_page():
    all_materials = base_materials_service.list_all()
    return render_template('base_materials.html', form=PowderForm(), all_materials=all_materials)


@base_materials.route('/<type>', methods=['GET'])
def select_material_type(type):
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
    body = {'template': render_template(
        'add_property_form.html', index=new_property_index)}
    return make_response(jsonify(body), 200)


@base_materials.route('', methods=['POST'])
def submit_material():
    valid, form = base_materials_service.save_material(request.form)

    if valid:
        return redirect('/')

    all_materials = base_materials_service.list_all()
    return render_template('base_materials.html', form=form, all_materials=all_materials)


@base_materials.route('/<material_type>/<uuid>', methods=['DELETE'])
def delete_material(material_type, uuid):
    all_materials = base_materials_service.delete_material(material_type, uuid)

    body = {'template': render_template('materials_table.html', all_materials=all_materials)}
    return make_response(jsonify(body), 200)
