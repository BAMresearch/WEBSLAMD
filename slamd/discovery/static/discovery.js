const DISCOVERY_URL = `${window.location.protocol}//${window.location.host}/materials/discovery`;

function updateCuriosityValue(curiosity) {
    value = parseFloat(curiosity);
    document.getElementById("selected-range").value = parseFloat(value.toFixed(2));
}

async function deleteDataset(datasetName) {
    const url = `${DISCOVERY_URL}/${datasetName}`;
    await deleteDataAndEmbedTemplateInPlaceholder(url, "datasets-table-placeholder");
}

function updateTargetPropertiesChoices(event) {
    filterUnselectedOptionsAndAssignToSelectElement(event.target.options, "target_properties");
}

function updateAPrioriInformationChoices(event) {
    filterUnselectedOptionsAndAssignToSelectElement(event.target.options, "a_priori_information");
}

async function getTargetConfigurationForm(event, placeholderId) {
    const names = collectSelectedValues(event.target.options);
    const url = `${DISCOVERY_URL}/create_target_configuration_form`;
    await postDataAndEmbedTemplateInPlaceholder(url, placeholderId, {
        names,
    });
}

async function getAPrioriInformationConfigurationForm(event, placeholderId) {
    const names = collectSelectedValues(event.target.options);
    const url = `${DISCOVERY_URL}/create_a_priori_information_configuration_form`;
    await postDataAndEmbedTemplateInPlaceholder(url, placeholderId, {
        names,
    });
}

function onChangeMaterialsDataInput(event) {
    updateTargetPropertiesChoices(event);
    // Delete all options for the third multi-select field
    removeInnerHtmlFromPlaceholder("a_priori_information");
    // Remove all forms corresponding to the two next multi-select fields
    removeInnerHtmlFromPlaceholder("target-configuration-form-placeholder");
    removeInnerHtmlFromPlaceholder("a-priori-information-configuration-form-placeholder");
}

function onChangeTargetProperties(event) {
    updateAPrioriInformationChoices(event);
    getTargetConfigurationForm(event, "target-configuration-form-placeholder");
    // Remove all forms corresponding to the next multi-select field
    removeInnerHtmlFromPlaceholder("a-priori-information-configuration-form-placeholder");
}

function onChangeAPrioriInformation(event) {
    getAPrioriInformationConfigurationForm(event, "a-priori-information-configuration-form-placeholder");
}

/**
 * In order to be consistent with Plotly's plot function, we use the fetch API slightly different as compared to
 * our other use cases where we use fetchDataAndEmbedTemplateInPlaceholder defined in global.js
 */
async function tsnePlotListener() {
    const alreadyFetched = document.getElementById("tsne-plot-placeholder").innerHTML.trim() !== ""

    if (alreadyFetched) {
        return;
    }

    insertSpinnerInPlaceholder("tsne-plot-placeholder");

    const response = await fetch(DISCOVERY_URL + "/tsne");
    removeSpinnerInPlaceholder("tsne-plot-placeholder");

    if (response.ok) {
        const tsnePlotData = await response.json();
        Plotly.plot("tsne-plot-placeholder", tsnePlotData.data, tsnePlotData.layout, {responsive: true});
    } else {
        const error = await response.text();
        document.write(error);
    }
}

async function runExperiment() {
    const experimentRequest = createRunExperimentRequest();
    // The endpoint is the current URL which should contain the dataset name
    // For example: http://127.0.0.1:5001/materials/discovery/MaterialsDiscoveryExampleData.csv

    insertSpinnerInPlaceholder("experiment-result-placeholder");
    await postDataAndEmbedTemplateInPlaceholder(window.location.href, "experiment-result-placeholder", experimentRequest);
    removeSpinnerInPlaceholder("experiment-result-placeholder");

    // The scatter plot data is embedded in the HTML placeholders. Turn the JSON data into actual plots.
    plotJsonDataInPlaceholder("scatter-plot-placeholder");

    document.getElementById("tsne-plot-button").addEventListener('click', tsnePlotListener)
}

function toggleRunExperimentButton() {
    const countMaterialDataInput = countSelectedOptionsMultipleSelectField(
        document.getElementById("materials_data_input")
    );
    const countTargetProperties = countSelectedOptionsMultipleSelectField(document.getElementById("target_properties"));
    document.getElementById("run-experiment-button").disabled = countMaterialDataInput < 1 || countTargetProperties < 1;
}

window.addEventListener("load", () => {
    document.getElementById("nav-bar-discovery").setAttribute("class", "nav-link active");
    document.getElementById("materials_data_input").addEventListener("change", onChangeMaterialsDataInput);
    document.getElementById("target_properties").addEventListener("change", onChangeTargetProperties);
    document.getElementById("a_priori_information").addEventListener("change", onChangeAPrioriInformation);
    document.getElementById("run-experiment-button").addEventListener("click", runExperiment);
    document.getElementById("materials_data_input").addEventListener("change", toggleRunExperimentButton);
    document.getElementById("target_properties").addEventListener("change", toggleRunExperimentButton);
});
