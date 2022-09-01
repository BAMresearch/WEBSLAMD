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


@discovery.route('/create_target_configuration_form', methods=['POST'])
def create_target_configuration_form():
    request_body = json.loads(request.data)
    form = DiscoveryService.create_target_configuration_form(request_body['names'])
    body = {'template': render_template('target_configuration_form.html', form=form)}
    return make_response(jsonify(body), 200)


@discovery.route('/create_a_priori_information_configuration_form', methods=['POST'])
def create_a_priori_information_configuration_form():
    request_body = json.loads(request.data)
    form = DiscoveryService.create_a_priori_information_configuration_form(request_body['names'])
    body = {'template': render_template('a_priori_information_configuration_form.html', form=form)}
    return make_response(jsonify(body), 200)


@discovery.route('/<dataset>', methods=['POST'])
def run_experiment(dataset):
    request_body = json.loads(request.data)
    dataframe = DiscoveryService.run_experiment(dataset, request_body)
    html_dataframe = dataframe.to_html(index=False,
                                       table_id='formulations_dataframe',
                                       classes='table table-bordered table-striped table-hover')

    body = {'template': render_template('experiment_result.html', df=html_dataframe)}
    return make_response(jsonify(body), 200)


@discovery.route('/<dataset>/download', methods=['GET'])
def download_dataset(dataset):
    dataset_content = DiscoveryService.download_dataset(dataset)
    response = make_response(dataset_content.encode())
    response.headers['Content-Disposition'] = f'attachment; filename={dataset}'
    response.mimetype = 'text/csv'
    return response


@discovery.route('/<dataset>/add_targets', methods=['GET'])
def add_targets(dataset):
    dataframe, all_dtos, target_list = DiscoveryService.show_dataset_for_adding_targets(dataset)
    html_dataframe = dataframe.to_html(index=False,
                                       table_id='formulations_dataframe',
                                       classes='table table-bordered table-striped table-hover df-collapsed')

    return render_template('targets.html',
                           dataset_name=dataset,
                           form=TargetsForm(),
                           df=html_dataframe,
                           all_dtos=all_dtos,
                           target_list=target_list)


@discovery.route('/<dataset>/<target_name>/add_target', methods=['GET'])
def add_target(dataset, target_name):
    dataframe, all_dtos, target_list = DiscoveryService.add_target_name(dataset, target_name)
    html_dataframe = dataframe.to_html(index=False,
                                       table_id='formulations_dataframe',
                                       classes='table table-bordered table-striped table-hover df-collapsed')

    body = {'template': render_template('targets_form.html',
                                        form=TargetsForm(),
                                        df=html_dataframe,
                                        all_dtos=all_dtos,
                                        target_list=target_list)}
    return make_response(jsonify(body), 200)


@discovery.route('/<dataset>/add_targets', methods=['POST'])
def submit_target_values(dataset):
    DiscoveryService.save_targets(dataset, request.form)

    return redirect('/materials/discovery')
