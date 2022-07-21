from flask import Blueprint, render_template

from slamd.formulations.processing.formulations_service import FormulationsService

formulations = Blueprint('formulations', __name__,
                         template_folder='../templates',
                         static_folder='../static',
                         static_url_path='static',
                         url_prefix='/materials/formulations')


@formulations.route('', methods=['GET'])
def base_material_page():
    form = FormulationsService.populate_selection_form()
    return render_template('formulations.html', materials_and_processes_selection_form=form)
