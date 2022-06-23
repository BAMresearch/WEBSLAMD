from flask import Blueprint, render_template, redirect, request, make_response, jsonify

from slamd.materials.forms.base_materials_form import BaseMaterialsForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.materials_service import MaterialsService

materials = Blueprint('materials', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='static',
                      url_prefix='/materials')


@materials.route('', methods=['GET'])
def material_page():
    return render_template('materials.html', base_materials_form=BaseMaterialsForm(), form=PowderForm())


@materials.route('/<type>', methods=['GET'])
def select_material_type(type):
    template_file, form = MaterialsService().create_material_form(type)
    body = {'template': render_template(template_file, form=form)}
    return make_response(jsonify(body), 200)


@materials.route('/add_property/<new_property_index>', methods=['GET'])
def add_property(new_property_index):
    """
    Return HTML for an additional property form.
    The <input> tags generated here must have different 'name' and 'id' attributes.
    We use indexes starting from zero to name them differently.
    The format matches what WTForms does when rendering a FieldList.
    """
    body = {'template': render_template('add_property_form.html', index=new_property_index)}
    return make_response(jsonify(body), 200)


@materials.route('', methods=['POST'])
def submit_material():
    form = BaseMaterialsForm(request.form)
    if form.validate():
        return redirect('/')
    return render_template('materials.html', base_materials_form=form, form=PowderForm())
