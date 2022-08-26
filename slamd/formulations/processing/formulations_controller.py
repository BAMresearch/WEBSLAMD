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
    df, all_dtos, target_list = FormulationsService.get_formulations()

    df_table = None
    if df is not None:
        df_table = df.to_html(table_id='formulations_dataframe',
                              classes='table table-bordered table-striped table-hover')

    return render_template('formulations.html',
                           materials_and_processes_selection_form=form,
                           formulations_min_max_form=FormulationsMinMaxForm(),
                           df=df_table,
                           all_dtos=all_dtos,
                           target_list=target_list)


@formulations.route('/add_min_max_entries', methods=['POST'])
def add_formulations_min_max_entry():
    formulation_selection = json.loads(request.data)
    min_max_form = FormulationsService.create_formulations_min_max_form(formulation_selection)
    body = {'template': render_template('formulations_min_max_form.html', formulations_min_max_form=min_max_form)}
    return make_response(jsonify(body), 200)


@formulations.route('/add_weights', methods=['POST'])
def add_weights():
    weights_request_data = json.loads(request.data)
    weights_form = FormulationsService.create_weights_form(weights_request_data)
    body = {'template': render_template('weights_form.html', weights_form=weights_form)}
    return make_response(jsonify(body), 200)


@formulations.route('/create_formulations_batch', methods=['POST'])
def submit_formulations():
    formulations_request_data = json.loads(request.data)
    dataframe, all_dtos, target_list = FormulationsService.create_materials_formulations(formulations_request_data)

    body = {'template': render_template('formulations_tables.html',
                                        df=dataframe.to_html(table_id='formulations_dataframe',
                                                             classes='table table-bordered table-striped table-hover'),
                                        all_dtos=all_dtos,
                                        target_list=target_list)}

    return make_response(jsonify(body), 200)


@formulations.route('', methods=['DELETE'])
def delete_formulation():
    FormulationsService.delete_formulation()
    body = {'template': render_template('formulations_tables.html',
                                        df=None,
                                        all_dtos=[],
                                        target_list=[])}

    return make_response(jsonify(body), 200)


@formulations.route('/add_target', methods=['POST'])
def add_target():
    target_request = json.loads(request.data)

    df, all_dtos, target_list = FormulationsService.add_target_name(target_request)
    body = {'template': render_template('formulations_tables.html',
                                        df=df.to_html(table_id='formulations_dataframe',
                                                      classes='table table-bordered table-striped table-hover'),
                                        all_dtos=all_dtos,
                                        target_list=target_list)}

    return make_response(jsonify(body), 200)
