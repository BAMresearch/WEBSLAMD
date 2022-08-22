const FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations`;
let withConstraint = false;
let weightConstraint = "";

function toggleBasedOnSelectionAndConstraints() {
  const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");

  const validConstraintConfiguration = withConstraint && weightConstraint !== undefined && weightConstraint !== "";
  if (withConstraint) {
    changeSelectionButton.disabled = !validConstraintConfiguration;
  }
}

function toggleSelectionConfirmationButtonAfterConstraintChange() {
  weightConstraint = document.getElementById("weight_constraint").value;
  toggleBasedOnSelectionAndConstraints();
}

function autocorrectWeightValue() {
  const weightConstraintInput = document.getElementById("weight_constraint");
  correctInputFieldValue(weightConstraintInput);
}

function toggleWeightConstraintInput() {
  const with_constraint = document.getElementById("with_constraint");
  removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder");
  removeInnerHtmlFromPlaceholder("formulations_weights_placeholder");

  withConstraint = with_constraint.checked;
  if (withConstraint) {
    document.getElementById("weight_constraint").disabled = false;
    document.getElementById("change_materials_and_processes_selection_button").disabled = true;
  } else {
    document.getElementById("weight_constraint").disabled = true;
    document.getElementById("weight_constraint").value = "";
    document.getElementById("change_materials_and_processes_selection_button").disabled = false;
  }
}

async function confirmSelection() {
  removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder");
  removeInnerHtmlFromPlaceholder("formulations_weights_placeholder");
  document.getElementById("submit").disabled = true;
  weightConstraint = document.getElementById("weight_constraint").value;

  const selectedMaterials = collectAllSelectedMaterials();

  const processesPlaceholder = document.getElementById("process_selection");
  const selectedProcesses = collectSelection(processesPlaceholder);

  const url = `${FORMULATIONS_MATERIALS_URL}/add_min_max_entries/${selectedMaterials.length}/${selectedProcesses.length}`;
  await fetchDataAndEmbedTemplateInPlaceholder(url, "formulations_min_max_placeholder");

  prepareMaterialsMinMaxInputFieldsFromSelection(selectedMaterials);
  prepareProcessMinMaxInputFieldsFromSelection(selectedProcesses);
  assignKeyboardEventsToFormulationsMinMaxForm();
  assignConfirmFormulationsConfigurationEvent();
}

async function assignConfirmFormulationsConfigurationEvent() {
  const button = document.getElementById("confirm_formulations_configuration_button");
  enableTooltip(button);

  button.addEventListener("click", async () => {
    const requestData = collectFormulationsMinMaxRequestData();
    const url = `${FORMULATIONS_MATERIALS_URL}/add_weights`;
    await postDataAndEmbedTemplateInPlaceholder(url, "formulations_weights_placeholder", requestData);
    assignDeleteWeightEvent();
    assignCreateFormulationsBatchEvent();
  });
}

function assignCreateFormulationsBatchEvent() {
  const button = document.getElementById("create_formulations_batch_button");
  enableTooltip(button);

  button.addEventListener("click", async () => {
    const materialsRequestData = collectFormulationsMinMaxRequestData();
    const processesRequestData = collectProcessesRequestData();
    const targets = document.getElementById("targets_field").value;

    const formulationsRequest = {
      materials_request_data: materialsRequestData,
      processes_request_data: processesRequestData,
      targets: targets,
    };

    const url = `${FORMULATIONS_MATERIALS_URL}/create_formulations_batch`;
    await postDataAndEmbedTemplateInPlaceholder(url, "formulations_tables_placeholder", formulationsRequest);
  });
}

function assignDeleteWeightEvent() {
  let numberOfWeightEntries = document.querySelectorAll('[id^="all_weights_entries-"]').length;

  for (let i = 0; i < numberOfWeightEntries; i++) {
    let deleteButton = document.getElementById(`delete_weight_button___${i}`);
    deleteButton.addEventListener("click", () => {
      document.getElementById(`all_weights_entries-${i}-weights`).remove();
      deleteButton.remove();
    });
  }
}

function toggleFormulationConfirmationButton() {
  const targets = document.getElementById("targets_field").value;
  let regex = new RegExp("^([a-zA-Z\\d ]+;)*[a-zA-Z\\d ]+$");

  document.getElementById("change_materials_and_processes_selection_button").disabled = !regex.test(targets);
}

window.addEventListener("load", function () {
  document
    .getElementById("confirm_materials_and_processes_selection_button")
    .addEventListener("click", confirmSelection);
  document.getElementById("with_constraint").addEventListener("change", toggleWeightConstraintInput);
  document
    .getElementById("weight_constraint")
    .addEventListener("change", toggleSelectionConfirmationButtonAfterConstraintChange);
  document.getElementById("weight_constraint").addEventListener("keyup", autocorrectWeightValue);
  document.getElementById("targets_field").addEventListener("keyup", toggleFormulationConfirmationButton);
});
