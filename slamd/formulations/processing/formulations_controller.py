from flask import Blueprint, render_template

formulations = Blueprint('formulations', __name__,
                         template_folder='../templates',
                         static_folder='../static',
                         static_url_path='static',
                         url_prefix='/materials/formulations')


@formulations.route('', methods=['GET'])
def base_material_page():
    return render_template('formulations.html')
