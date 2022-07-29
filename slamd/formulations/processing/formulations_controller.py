import json

from flask import Blueprint, render_template, make_response, jsonify, request

from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.formulations_service import FormulationsService

formulations = Blueprint('formulations', __name__,
                         template_folder='../templates',
                         static_folder='../static',
                         static_url_path='static',
                         url_prefix='/materials/formulations')


@formulations.route('', methods=['GET'])
def base_material_page():
    form = FormulationsService.populate_selection_form()

    return render_template('formulations.html',
                           materials_and_processes_selection_form=form,
                           formulations_min_max_form=FormulationsMinMaxForm())


@formulations.route('/add_min_max_entries/<count_materials>/<count_processes>', methods=['GET'])
def add_formulations_min_max_entry(count_materials, count_processes):
    min_max_form = FormulationsService.create_formulations_min_max_form(count_materials, count_processes)
    body = {'template': render_template('formulations_min_max_form.html', formulations_min_max_form=min_max_form)}
    return make_response(jsonify(body), 200)


@formulations.route('/add_weights', methods=['POST'])
def add_weights():
    weights_request_data = json.loads(request.data)
    weights_form, formulations_composition = FormulationsService.create_weights_form(weights_request_data)
    body = {'template': render_template('weights_form.html', weights_form=weights_form,
                                        formulations_composition=formulations_composition)}
    return make_response(jsonify(body), 200)


@formulations.route('/create_formulations_batch', methods=['POST'])
def submit_formulations():
    formulations_request_data = json.loads(request.data)
    dataframe = FormulationsService.create_materials_formulations(formulations_request_data)

    # dataframe['name'] = [f'<input class="form-control" id="weigth_constraint" name="weigth_constraint" step="any" type="number" value="{x}">' for x in dataframe['name']]
    # html = dataframe.to_html(index=False, table_id='formulations_dataframe', escape=False)

    # html = html.replace('<th>','<th style="background-color: royalblue; color: white">')

    body = {'template': render_template('formulations_dataframe.html', df=dataframe.to_html(index=False,
                                                                                            table_id='formulations_dataframe'))}

    return make_response(jsonify(body), 200)
