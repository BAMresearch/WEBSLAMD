from flask import Blueprint, render_template, redirect, request, make_response, jsonify

from slamd.materials.forms.base_materials_form import BaseMaterialsForm
from slamd.materials.forms.powder_form import PowderForm

materials = Blueprint('materials', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='static',
                      url_prefix='/materials')


@materials.route('', methods=['GET'])
def material_page():
    return render_template('materials.html', base_materials_form=BaseMaterialsForm())


@materials.route('/<type>', methods=['GET'])
def select_material_type(type):
    type = type.lower()
    # TODO: Select the correct form dynamically
    body = {'template': render_template(f'{type}.html', form=PowderForm())}
    print(f'Received GET request for {type}')
    return make_response(jsonify(body), 200)


@materials.route('', methods=['POST'])
def submit_material():
    form = BaseMaterialsForm(request.form)
    if form.validate():
        return redirect('/')
    return render_template('materials.html', base_materials_form=form)
