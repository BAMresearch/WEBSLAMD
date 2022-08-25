const DISCOVERY_URL = `${window.location.protocol}//${window.location.host}/materials/discovery`;

function updateCuriosityValue(curiosity) {
  value = parseFloat(curiosity);
  document.getElementById("selected-range").value = parseFloat(value.toFixed(2));
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

async function getDiscoveryConfigurationForm(event) {
  const names = [];
  for (const option of event.target.options) {
    if (option.selected) {
      names.push(option.value);
    }
  }

  const url = `${DISCOVERY_URL}/create_discovery_configuration_form`;
  await postDataAndEmbedTemplateInPlaceholder(url, "discovery-configuration-form-placeholder", {
    names,
  });
}

function onChangeMaterialsDataInput(event) {
  updateTargetPropertiesChoices(event);
}

function onChangeTargetProperties(event) {
  updateAPrioriInformationChoices(event);
  getDiscoveryConfigurationForm(event);
}

window.addEventListener("load", () => {
  document.getElementById("materials_data_input").addEventListener("change", onChangeMaterialsDataInput);
  document.getElementById("target_properties").addEventListener("change", onChangeTargetProperties);
});
