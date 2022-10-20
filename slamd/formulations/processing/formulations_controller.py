import json

from flask import Blueprint, render_template, make_response, jsonify, request, redirect

from slamd.formulations.processing.forms.formulations_min_max_form import FormulationsMinMaxForm
from slamd.formulations.processing.formulations_service import FormulationsService

formulations = Blueprint('formulations', __name__,
                         template_folder='../templates',
                         static_folder='../static',
                         static_url_path='static',
                         url_prefix='/materials/formulations')


@formulations.route('/<building_material>', methods=['GET'])
def formulations_page(building_material):
    form, df = FormulationsService.load_formulations_page(building_material)

    df_table = None
    if df is not None:
        df_table = df.to_html(index=False,
                              table_id='formulations_dataframe',
                              classes='accordion-body table table-bordered table-striped table-hover topscroll-table')

    return render_template('formulations.html',
                           context=building_material,
                           materials_and_processes_selection_form=form,
                           formulations_min_max_form=FormulationsMinMaxForm(),
                           df=df_table)


@formulations.route('/<building_material>/add_min_max_entries', methods=['POST'])
def add_formulations_min_max_entry(building_material):
    formulation_selection = json.loads(request.data)
    min_max_form = FormulationsService.create_formulations_min_max_form(formulation_selection, building_material)
    body = {'template': render_template('formulations_min_max_form.html', formulations_min_max_form=min_max_form)}
    return make_response(jsonify(body), 200)


@formulations.route('/<building_material>/add_weights', methods=['POST'])
def add_weights(building_material):
    weights_request_data = json.loads(request.data)
    weights_form = FormulationsService.create_weights_form(weights_request_data, building_material)
    body = {'template': render_template('weights_form.html', weights_form=weights_form)}
    return make_response(jsonify(body), 200)


@formulations.route('/<building_material>/create_formulations_batch', methods=['POST'])
def submit_formulation_batch(building_material):
    formulations_request_data = json.loads(request.data)
    dataframe = FormulationsService.create_materials_formulations(formulations_request_data, building_material)

    html_dataframe = dataframe.to_html(index=False,
                                       table_id='formulations_dataframe',
                                       classes='table table-bordered table-striped table-hover topscroll-table')
    body = {'template': render_template('formulations_table.html', df=html_dataframe)}
    return make_response(jsonify(body), 200)


@formulations.route('/<building_material>', methods=['DELETE'])
def delete_formulation(building_material):
    FormulationsService.delete_formulation(building_material)
    body = {'template': render_template('formulations_table.html', df=None)}

    return make_response(jsonify(body), 200)


@formulations.route('/<building_material>', methods=['POST'])
def submit_dataset(building_material):
    FormulationsService.save_dataset(request.form, building_material)

    return redirect(f'/materials/formulations/{building_material}')
