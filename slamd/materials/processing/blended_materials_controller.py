import json

from flask import Blueprint, render_template, request, redirect, make_response, jsonify

from slamd.materials.processing.blended_materials_service import BlendedMaterialsService
from slamd.materials.processing.forms.base_material_selection_form import BaseMaterialSelectionForm
from slamd.materials.processing.forms.blending_name_and_type_form import BlendingNameAndTypeForm
from slamd.materials.processing.forms.min_max_form import MinMaxForm
from slamd.materials.processing.forms.ratio_form import RatioForm
from slamd.materials.processing.material_type import MaterialType

blended_materials = Blueprint('blended_materials', __name__,
                              template_folder='../templates',
                              static_folder='../static',
                              static_url_path='static',
                              url_prefix='/materials/blended')


@blended_materials.route('', methods=['GET'])
def blended_material_page():
    material_response = BlendedMaterialsService.list_materials(blended=True)
    base_material_selection_form = BlendedMaterialsService.list_base_material_selection_by_type(
        MaterialType.POWDER.value)
    return render_template('blended_materials.html',
                           blending_name_and_type_form=BlendingNameAndTypeForm(),
                           base_material_selection_form=base_material_selection_form,
                           min_max_form=MinMaxForm(),
                           ratio_form=RatioForm(),
                           materials_response=material_response)


@blended_materials.route('/<type>', methods=['GET'])
def select_base_material_type(type):
    base_material_selection_form = BlendedMaterialsService.list_base_material_selection_by_type(type)
    body = {'template': render_template('base_material_selection.html',
                                        base_material_selection_form=base_material_selection_form)}
    return make_response(jsonify(body), 200)


@blended_materials.route('', methods=['POST'])
def submit_blending():
    blending_data = BlendingNameAndTypeForm(request.form)
    base_material_selection = request.form.getlist('base_material_selection')

    if blending_data.validate():
        return redirect('/materials/blended')

    materials_response = BlendedMaterialsService.list_materials(blended=True)
    return render_template('blended_materials.html',
                           blending_name_and_type_form=blending_data,
                           base_material_selection_form=BaseMaterialSelectionForm(),
                           min_max_form=MinMaxForm(),
                           ratio_form=RatioForm(),
                           materials_response=materials_response)


@blended_materials.route('/add_min_max_entries/<count>', methods=['GET'])
def add_min_max_entry(count):
    min_max_form = BlendedMaterialsService.create_min_max_form(count)
    body = {'template': render_template('min_max_form.html', min_max_form=min_max_form)}
    return make_response(jsonify(body), 200)


@blended_materials.route('/add_ratios', methods=['POST'])
def add_ratios():
    all_min_max_values = json.loads(request.data)
    ratio_form = BlendedMaterialsService.create_ratio_form(all_min_max_values)
    body = {'template': render_template('ratio_form.html', ratio_form=ratio_form)}
    return make_response(jsonify(body), 200)


@blended_materials.route('/<material_type>/<uuid>', methods=['DELETE'])
def delete_blended_material(material_type, uuid):
    all_blended_materials = BlendedMaterialsService.delete_material(material_type, uuid)

    body = {'template': render_template('materials_table.html', materials_response=all_blended_materials)}
    return make_response(jsonify(body), 200)
