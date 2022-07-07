from flask import Blueprint, render_template, request, redirect

from slamd.materials.processing.forms.blending_form import BlendingForm

blended_materials = Blueprint('blended_materials', __name__,
                              template_folder='../templates',
                              static_folder='../static',
                              static_url_path='static',
                              url_prefix='/materials/blended')

blended_materials_service = None


@blended_materials.route('', methods=['GET'])
def blended_material_page():
    return render_template('blended_materials.html', form=BlendingForm())


@blended_materials.route('', methods=['POST'])
def submit_blending():
    blending_data = BlendingForm(request.form)

    if blending_data.validate():
        return redirect('/materials/blended')

    return render_template('blended_materials.html', form=blending_data)
