import json
from flask import Blueprint, render_template, request, make_response, jsonify, redirect

from slamd.materials.processing.base_materials_service import BaseMaterialService

base_materials = Blueprint('base_materials', __name__,
                           template_folder='../templates',
                           static_folder='../static',
                           static_url_path='static',
                           url_prefix='/materials/base')


@base_materials.route('', methods=['GET'])
def base_material_page():
    form = BaseMaterialService.create_material_form('powder')
    materials_response = BaseMaterialService.list_materials(blended=False)
    return render_template('base_materials.html', form=form, materials_response=materials_response)


@base_materials.route('/<material_type>', methods=['GET'])
def select_base_material_type(material_type):
    form = BaseMaterialService.create_material_form(material_type)
    body = {'template': render_template('material_type_form.html', form=form)}
    return make_response(jsonify(body), 200)


@base_materials.route('/add_property', methods=['POST'])
def add_additional_property():
    current_additional_properties = json.loads(request.data)
    form = BaseMaterialService.create_additional_property_form(current_additional_properties)
    body = {'template': render_template('additional_property_form.html', form=form)}
    return make_response(jsonify(body), 200)


@base_materials.route('', methods=['POST'])
def submit_base_material():
    valid, form = BaseMaterialService.save_material(request.form)

    if valid:
        return redirect('/materials/base')

    materials_response = BaseMaterialService.list_materials(blended=False)
    return render_template('base_materials.html', form=form, materials_response=materials_response)


@base_materials.route('/<material_type>/<uuid>', methods=['GET'])
def populate_base_material_form(material_type, uuid):
    form = BaseMaterialService.populate_form(material_type, uuid)

    materials_response = BaseMaterialService.list_materials(blended=False)
    return render_template('base_materials.html', form=form, materials_response=materials_response)


@base_materials.route('/<material_type>/<uuid>', methods=['POST'])
def edit_material(material_type, uuid):
    valid, form = BaseMaterialService.edit_material(material_type, uuid, request.form)

    if valid:
        return redirect('/materials/base')

    materials_response = BaseMaterialService.list_materials(blended=False)
    return render_template('base_materials.html', form=form, materials_response=materials_response)


@base_materials.route('/<material_type>/<uuid>', methods=['DELETE'])
def delete_base_material(material_type, uuid):
    BaseMaterialService.delete_material(material_type, uuid)

    materials_response = BaseMaterialService.list_materials(blended=False)
    body = {'template': render_template('materials_table.html', materials_response=materials_response)}
    return make_response(jsonify(body), 200)
