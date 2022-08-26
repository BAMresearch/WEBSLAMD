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

async function getDiscoveryConfigurationForm(event, placeholderId) {
  const names = [];
  for (const option of event.target.options) {
    if (option.selected) {
      names.push(option.value);
    }
  }

  const url = `${DISCOVERY_URL}/create_discovery_configuration_form`;
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
  getDiscoveryConfigurationForm(event, "target-configuration-form-placeholder");
  // Remove all forms corresponding to the next multi-select field
  removeInnerHtmlFromPlaceholder("a-priori-information-configuration-form-placeholder");
}

function onChangeAPrioriInformation(event) {
  getDiscoveryConfigurationForm(event, "a-priori-information-configuration-form-placeholder");
}

window.addEventListener("load", () => {
  document.getElementById("nav-bar-discovery").setAttribute("class", "nav-link active");
  document.getElementById("materials_data_input").addEventListener("change", onChangeMaterialsDataInput);
  document.getElementById("target_properties").addEventListener("change", onChangeTargetProperties);
  document.getElementById("a_priori_information").addEventListener("change", onChangeAPrioriInformation);
});
