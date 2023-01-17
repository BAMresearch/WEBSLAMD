import json
import os
from flask import Blueprint, request, render_template, make_response, jsonify, redirect, send_file, url_for
from flask import flash
from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence
from slamd.discovery.processing.discovery_service import DiscoveryService
from slamd.discovery.processing.extend_service import ExtendService
from slamd.discovery.processing.forms.discovery_form import DiscoveryForm
from slamd.discovery.processing.forms.upload_dataset_form import UploadDatasetForm
from slamd.discovery.processing.targets_service import TargetsService

discovery = Blueprint('discovery', __name__,
                      template_folder='../templates',
                      static_folder='../static',
                      static_url_path='static',
                      url_prefix='/materials/discovery')

RUNNING_LOCALLY = bool(os.getenv('FLASK_ENV') == 'development')


@discovery.route('', methods=['GET'])
def discovery_page():
    upload_dataset_form = UploadDatasetForm()
    discovery_form = DiscoveryForm()
    datasets = DiscoveryService.list_datasets()

    return render_template(
        'discovery.html',
        upload_dataset_form=upload_dataset_form,
        discovery_form=discovery_form,
        datasets=datasets,
        tuned_models_explanation_active=RUNNING_LOCALLY
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
        datasets=datasets,
        tuned_models_explanation_active=RUNNING_LOCALLY
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
        datasets=datasets,
        tuned_models_explanation_active=RUNNING_LOCALLY
    )


# -- Zia ---
@discovery.route('/<dataset>', methods=['GET'])
def extend_dataset(dataset):
    discovery_form = DiscoveryForm()
    discovery_form.materials_data_input.choices = DiscoveryService.list_columns(dataset)

    datasets = DiscoveryService.list_datasets()
    return render_template(
        'discovery.html',
        upload_dataset_form=UploadDatasetForm(),
        discovery_form=discovery_form,
        datasets=datasets,
        tuned_models_explanation_active=RUNNING_LOCALLY
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
    dataframe, scatter_plot = DiscoveryService.run_experiment(dataset, request_body)
    html_dataframe = dataframe.to_html(index=False,
                                       table_id='formulations_dataframe',
                                       classes='table table-bordered table-striped table-hover topscroll-table')

    body = {'template': render_template('experiment_result.html', df=html_dataframe, scatter_plot=scatter_plot)}
    return make_response(jsonify(body), 200)


@discovery.route('/<dataset>/download', methods=['GET'])
def download_dataset(dataset):
    dataset_content = DiscoveryService.download_dataset(dataset)
    response = make_response(dataset_content.encode())
    response.headers['Content-Disposition'] = f'attachment; filename={dataset}'
    response.mimetype = 'text/csv'
    return response


@discovery.route('/download_prediction', methods=['GET'])
def download_prediction():
    filename, dataset_content = DiscoveryService.download_prediction()
    return send_file(dataset_content,
                     attachment_filename=filename,
                     as_attachment=True)


@discovery.route('/tsne', methods=['GET'])
def create_tsne_plot():
    tsne_plot = DiscoveryService.create_tsne_plot()
    return make_response(tsne_plot, 200)


@discovery.route('/<dataset>/add_targets', methods=['GET'])
def add_targets(dataset):
    target_page_data = TargetsService.get_data_for_target_page(dataset)
    html_dataframe = target_page_data.dataframe.to_html(
        index=False,
        table_id='formulations_dataframe',
        classes='table table-bordered table-striped table-hover topscroll-table'
    )

    return render_template('targets.html',
                           dataset_name=dataset,
                           form=target_page_data.targets_form,
                           df=html_dataframe,
                           all_dtos=target_page_data.all_dtos,
                           target_list=target_page_data.target_name_list)


@discovery.route('/<dataset>/<target_name>/add_target', methods=['GET'])
def add_target(dataset, target_name):
    target_page_data = TargetsService.add_target_name(dataset, target_name)
    html_dataframe = target_page_data.dataframe.to_html(
        index=False,
        table_id='formulations_dataframe',
        classes='table table-bordered table-striped table-hover topscroll-table'
    )

    body = {'template': render_template('targets_form.html',
                                        form=target_page_data.targets_form,
                                        df=html_dataframe,
                                        all_dtos=target_page_data.all_dtos,
                                        target_list=target_page_data.target_name_list)}
    return make_response(jsonify(body), 200)


# Zia# ----------------------------------------------------------------------------------------

@discovery.route('/<dataset>/extend_dataset_sample', methods=['GET', 'POST'])
def extend_dataset_sample(dataset):
    extend_page_data = ExtendService.get_data_for_extend_page(dataset)
    dataset = extend_page_data.dataframe
    form = extend_page_data.extend_form

    if request.method == 'POST':
        num_samples = request.form.get('num_samples')
        select_columns = request.form.getlist('select_columns')
        target_columns = request.form.getlist('target_columns')
        min_value = {col: request.form.get(f"min_{col}") for col in select_columns}
        max_value = {col: request.form.get(f"max_{col}") for col in select_columns}

        if not all(min_value.values()) or not all(max_value.values()) or not num_samples:
            flash('Please enter a value for all fields.')
            return render_template('extends.html',
                                   dataset_name=dataset,
                                   form=form,
                                   df=dataset,
                                   )
        try:
            num_samples = int(num_samples)
            min_value = {col: int(val) for col, val in min_value.items()}
            max_value = {col: int(val) for col, val in max_value.items()}
        except ValueError:
            flash('Please enter a valid integer value for all fields.')
            return render_template('extends.html',
                                   df=dataset,
                                   )

        dataset = ExtendService.generate_samples(dataset, num_samples, min_value, max_value, target_columns,
                                                 select_columns)

        # DiscoveryPersistence.save_dataset(dataset)

    return render_template('extends.html',
                           dataset_name=dataset,
                           form=form,
                           df=dataset,
                           )


''' 
@discovery.route('/<dataset>/generate_sample', methods=['GET', 'POST'])
def select_min_max(dataset):
    test = ExtendService.generate_samples(dataset)
    html_data = test.dataframe.to_html(
        index=False,
        table_id='formulations_dataframe',
        classes='table table-bordered table-striped table-hover topscroll-table'
    )
    return render_template('extends.html',
                           dataset_name=dataset,
                           df=html_data)

'''


# ----------------------------------------------------------------------------------------


@discovery.route('/<dataset>/toggle_targets', methods=['POST'])
def toggle_targets(dataset):
    request_body = json.loads(request.data)

    target_page_data = TargetsService.toggle_targets_for_editing(dataset, request_body['names'])

    html_dataframe = target_page_data.dataframe.to_html(
        index=False, table_id='formulations_dataframe',
        classes='table table-bordered table-striped table-hover topscroll-table')

    body = {'template': render_template('targets_form.html',
                                        form=target_page_data.targets_form,
                                        df=html_dataframe,
                                        all_dtos=target_page_data.all_dtos,
                                        target_list=target_page_data.target_name_list)}
    return make_response(jsonify(body), 200)


@discovery.route('/<dataset>/add_targets', methods=['POST'])
def submit_target_values(dataset):
    TargetsService.save_targets(dataset, request.form)

    return redirect('/materials/discovery')
