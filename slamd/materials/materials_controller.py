from flask import Blueprint, render_template

from slamd.materials.forms.base_materials_form import BaseMaterialsForm

materials = Blueprint('materials', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='static',
                      url_prefix='/materials')


@materials.route("", methods=['GET'])
def material_page():
    return render_template('materials.html', base_materials_form=(BaseMaterialsForm()))
