import json

from flask import Blueprint, render_template, make_response, jsonify, request, redirect

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
    df = FormulationsService.get_formulations()

    df_table = None
    if df is not None:
        df_table = df.to_html(index=False,
                              table_id='formulations_dataframe',
                              classes='accordion-body table table-bordered table-striped table-hover topscroll-table')

    return render_template('formulations.html',
                           materials_and_processes_selection_form=form,
                           formulations_min_max_form=FormulationsMinMaxForm(),
                           df=df_table)


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
def submit_formulation_batch():
    formulations_request_data = json.loads(request.data)
    dataframe = FormulationsService.create_materials_formulations(formulations_request_data)

    html_dataframe = dataframe.to_html(index=False,
                                       table_id='formulations_dataframe',
                                       classes='table table-bordered table-striped table-hover topscroll-table')
    body = {'template': render_template('formulations_table.html', df=html_dataframe)}
    return make_response(jsonify(body), 200)


@formulations.route('', methods=['DELETE'])
def delete_formulation():
    FormulationsService.delete_formulation()
    body = {'template': render_template('formulations_table.html', df=None)}

    return make_response(jsonify(body), 200)


@formulations.route('', methods=['POST'])
def submit_dataset():
    FormulationsService.save_dataset(request.form)

    return redirect('/materials/formulations')
