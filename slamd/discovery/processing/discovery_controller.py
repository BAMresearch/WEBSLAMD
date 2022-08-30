import json
from flask import Blueprint, request, render_template, make_response, jsonify, redirect

from slamd.discovery.processing.discovery_service import DiscoveryService
from slamd.discovery.processing.forms.discovery_form import DiscoveryForm
from slamd.discovery.processing.forms.targets_form import TargetsForm
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm

discovery = Blueprint('discovery', __name__,
                      template_folder='../templates',
                      static_folder='../static',
                      static_url_path='static',
                      url_prefix='/materials/discovery')

discovery_service = DiscoveryService()


@discovery.route('', methods=['GET'])
def discovery_page():
    upload_dataset_form = UploadDatasetForm()
    discovery_form = DiscoveryForm()
    datasets = DiscoveryService.list_datasets()

    return render_template(
        'discovery.html',
        upload_dataset_form=upload_dataset_form,
        discovery_form=discovery_form,
        datasets=datasets
    )


@discovery.route('', methods=['POST'])
def upload_dataset():
    valid, form = DiscoveryService.save_dataset(request.form, request.files)

    if valid:
        return redirect('/materials/discovery')

    datasets = DiscoveryService.list_datasets()
    return render_template(
        'discovery.html',
        upload_dataset_form=form,
        discovery_form=DiscoveryForm(),
        datasets=datasets
    )


@discovery.route('/<dataset>', methods=['GET'])
def select_dataset(dataset):
    discovery_form = DiscoveryForm()
    discovery_form.materials_data_input.choices = DiscoveryService.list_columns(dataset)

    datasets = DiscoveryService.list_datasets()
    return render_template(
        'discovery.html',
        upload_dataset_form=UploadDatasetForm(),
        discovery_form=discovery_form,
        datasets=datasets
    )


@discovery.route('/<dataset>', methods=['DELETE'])
def delete_dataset(dataset):
    DiscoveryService.delete_dataset(dataset)

    datasets = DiscoveryService.list_datasets()
    body = {'template': render_template('datasets_table.html', datasets=datasets)}
    return make_response(jsonify(body), 200)


@discovery.route('/create_discovery_configuration_form', methods=['POST'])
def create_discovery_configuration_form():
    request_body = json.loads(request.data)
    form = DiscoveryService.create_discovery_configuration_form(request_body['names'])
    body = {'template': render_template('discovery_configuration_form.html', form=form)}
    return make_response(jsonify(body), 200)


@discovery.route('/<dataset>/add_targets', methods=['GET'])
def add_targets(dataset):
    dataframe, all_dtos, target_list = DiscoveryService.show_dataset_for_adding_targets(dataset)

    return render_template('targets.html',
                           dataset_name=dataset,
                           form=TargetsForm(),
                           df=dataframe.to_html(index=False,
                                                table_id='formulations_dataframe',
                                                classes='table table-bordered table-striped table-hover'),
                           all_dtos=all_dtos,
                           target_list=target_list)


@discovery.route('/<dataset>/<target_name>/add_target', methods=['GET'])
def add_target(dataset, target_name):
    dataframe, all_dtos, target_list = DiscoveryService.add_target_name(dataset, target_name)

    body = {'template': render_template('targets_form.html',
                                        form=TargetsForm(),
                                        df=dataframe.to_html(index=False,
                                                             table_id='formulations_dataframe',
                                                             classes='table table-bordered table-striped table-hover'),
                                        all_dtos=all_dtos,
                                        target_list=target_list)}
    return make_response(jsonify(body), 200)


@discovery.route('/<dataset>/add_targets', methods=['POST'])
def submit_target_values(dataset):
    dataframe, all_dtos, target_list = DiscoveryService.save_targets(dataset, request.form)

    return redirect('/materials/discovery')
