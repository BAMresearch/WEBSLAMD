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
  let options = event.target.options;
  filterUnselectedOptionsAndAssignToSelectElement(options, "target_properties");
}

function updateAPrioriInformationChoices(event) {
  let options = event.target.options;
  filterUnselectedOptionsAndAssignToSelectElement(options, "a_priori_information");
}

window.addEventListener("load", () => {
  document.getElementById("materials_data_input").addEventListener("change", updateTargetPropertiesChoices);
  document.getElementById("target_properties").addEventListener("change", updateAPrioriInformationChoices);
});
