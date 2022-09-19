const DISCOVERY_URL = `${window.location.protocol}//${window.location.host}/materials/discovery`;

function updateCuriosityValue(curiosity) {
  value = parseFloat(curiosity);
  document.getElementById("selected-range").value = parseFloat(value.toFixed(2));
}

async function deleteDataset(datasetName) {
  const url = `${DISCOVERY_URL}/${datasetName}`;
  await deleteDataAndEmbedTemplateInPlaceholder(url, "datasets-table-placeholder");
}

function filterUnselectedOptionsAndAssignToSelectElement(options, selectorElementID) {
  let options_not_selected = "";

  for (const option of options) {
    if (!option.selected) {
      options_not_selected += `<option value="${option.value}">${option.value}</option>`;
    }
  }

  document.getElementById(selectorElementID).innerHTML = options_not_selected;
}

function updateTargetPropertiesChoices(event) {
  filterUnselectedOptionsAndAssignToSelectElement(event.target.options, "target_properties");
}

function updateAPrioriInformationChoices(event) {
  filterUnselectedOptionsAndAssignToSelectElement(event.target.options, "a_priori_information");
}

function collectSelectedValues(options) {
  const values = [];
  for (const option of options) {
    if (option.selected) {
      values.push(option.value);
    }
  }
  return values;
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

function getMaxMinValue(maxCheckboxId, minCheckboxId) {
  const maxCheckboxElem = document.getElementById(maxCheckboxId);
  const minCheckboxElem = document.getElementById(minCheckboxId);

  if (maxCheckboxElem.checked) {
    return maxCheckboxElem.value;
  } else if (minCheckboxElem.checked) {
    return minCheckboxElem.value;
  } else {
    throw "Invalid state";
  }
}

function parseTargetConfigurations(numberTargetProperties) {
  const result = [];
  for (let i = 0; i < numberTargetProperties; ++i) {
    const max_or_min = getMaxMinValue(
      `target_configurations-${i}-max_or_min-0`,
      `target_configurations-${i}-max_or_min-1`
    );
    const weight = document.getElementById(`target_configurations-${i}-weight`).value;
    result.push({ max_or_min, weight });
  }
  return result;
}

function parseAPrioriInformationConfigurations(numberAPrioriInformationProperties) {
  const result = [];
  for (let i = 0; i < numberAPrioriInformationProperties; ++i) {
    const max_or_min = getMaxMinValue(
      `a_priori_information_configurations-${i}-max_or_min-0`,
      `a_priori_information_configurations-${i}-max_or_min-1`
    );
    const weight = document.getElementById(`a_priori_information_configurations-${i}-weight`).value;
    result.push({ max_or_min, weight });
  }
  return result;
}

async function runExperiment() {
  const materials_data_input = collectSelectedValues(document.getElementById("materials_data_input").options);
  const target_properties = collectSelectedValues(document.getElementById("target_properties").options);
  const a_priori_information = collectSelectedValues(document.getElementById("a_priori_information").options);
  const model = collectSelectedValues(document.getElementById("model").options);
  const curiosity = document.getElementById("curiosity").value;
  const target_configurations = parseTargetConfigurations(target_properties.length);
  const a_priori_information_configurations = parseAPrioriInformationConfigurations(a_priori_information.length);

  // The endpoint is the current URL which should contain the dataset name
  // For example: http://127.0.0.1:5001/materials/discovery/MaterialsDiscoveryExampleData.csv
  insertSpinnerInPlaceholder("experiment-result-placeholder");
  await postDataAndEmbedTemplateInPlaceholder(window.location.href, "experiment-result-placeholder", {
    materials_data_input,
    target_properties,
    a_priori_information,
    model: model[0],
    curiosity,
    target_configurations,
    a_priori_information_configurations,
  });
  removeSpinnerInPlaceholder("experiment-result-placeholder");

  // The plot data is embedded in the HTML placeholder. Turn the JSON data into an actual plot.
  const plotJson = JSON.parse(document.getElementById("interactive-plot-placeholder").textContent);
  removeInnerHtmlFromPlaceholder("interactive-plot-placeholder");
  Plotly.plot("interactive-plot-placeholder", plotJson.data, plotJson.layout, { responsive: true });
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
