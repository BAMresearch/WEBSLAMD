const FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations`;
let weightConstraint = "";

function toggleBasedOnSelectionAndConstraints() {
  const powderPlaceholder = document.getElementById("powder_selection");
  const liquidPlaceholder = document.getElementById("liquid_selection");
  const aggregatesPlaceholder = document.getElementById("aggregates_selection");

  const powderSelected = atLeastOneItemIsSelected(powderPlaceholder);
  const liquidSelected = atLeastOneItemIsSelected(liquidPlaceholder);
  const aggregatesSelected = atLeastOneItemIsSelected(aggregatesPlaceholder);

  const validSelectionConfiguration = powderSelected && liquidSelected && aggregatesSelected;
  const validConstraintConfiguration = weightConstraint !== undefined && weightConstraint !== "" &&
      weightConstraint > 0;

  const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");
  changeSelectionButton.disabled = !(validSelectionConfiguration && validConstraintConfiguration);
}

function toggleSelectionConfirmationButtonAfterConstraintChange() {
  weightConstraint = document.getElementById("weight_constraint").value;
  toggleBasedOnSelectionAndConstraints();
}

function autocorrectWeightValue() {
  const weightConstraintInput = document.getElementById("weight_constraint");
  correctInputFieldValue(weightConstraintInput, 0);
}

async function confirmSelection() {
  removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder");
  removeInnerHtmlFromPlaceholder("formulations_weights_placeholder");
  document.getElementById("submit").disabled = true;
  weightConstraint = document.getElementById("weight_constraint").value;

  const selectedMaterials = collectFormulationSelection();
  const url = `${FORMULATIONS_MATERIALS_URL}/add_min_max_entries`;

  insertSpinnerInPlaceholder("formulations_min_max_placeholder");
  await postDataAndEmbedTemplateInPlaceholder(url, "formulations_min_max_placeholder", selectedMaterials);
  removeSpinnerInPlaceholder("formulations_min_max_placeholder");

  addListenersToIndependentFields();
  assignConfirmFormulationsConfigurationEvent();
}

async function assignConfirmFormulationsConfigurationEvent() {
  const button = document.getElementById("confirm_formulations_configuration_button");
  enableTooltip(button);

  button.addEventListener("click", async () => {
    const requestData = collectFormulationsMinMaxRequestData();
    const url = `${FORMULATIONS_MATERIALS_URL}/add_weights`;

    insertSpinnerInPlaceholder("formulations_weights_placeholder");
    await postDataAndEmbedTemplateInPlaceholder(url, "formulations_weights_placeholder", requestData);
    removeSpinnerInPlaceholder("formulations_weights_placeholder");
    assignKeyboardEventsToWeightForm(true);
    assignDeleteWeightEvent();
    assignCreateFormulationsBatchEvent();
  });
}

function assignCreateFormulationsBatchEvent() {
  const button = document.getElementById("create_formulations_batch_button");
  enableTooltip(button);

  button.addEventListener("click", async () => {
    const materialsRequestData = collectMaterialRequestData();
    const weightsRequestData = collectWeights();
    const processesRequestData = collectProcessesRequestData();

    const formulationsRequest = {
      materials_request_data: materialsRequestData,
      weights_request_data: weightsRequestData,
      processes_request_data: processesRequestData,
    };

    const url = `${FORMULATIONS_MATERIALS_URL}/create_formulations_batch`;

    insertSpinnerInPlaceholder("formulations-table-placeholder");
    await postDataAndEmbedTemplateInPlaceholder(url, "formulations-table-placeholder", formulationsRequest);
    removeSpinnerInPlaceholder("formulations-table-placeholder");

    document.getElementById("submit").disabled = false;
    document.getElementById("delete_formulations_batches_button").disabled = false;
  });
}

function assignDeleteWeightEvent() {
  const numberOfWeightEntries = document.querySelectorAll('[id^="all_weights_entries-"]').length;

  for (let i = 0; i < numberOfWeightEntries; i++) {
    const deleteButton = document.getElementById(`delete_weight_button___${i}`);
    deleteButton.addEventListener("click", () => {
      document.getElementById(`all_weights_entries-${i}-weights`).remove();
      deleteButton.remove();
    });
  }
}

async function deleteFormulations() {
  await deleteDataAndEmbedTemplateInPlaceholder(FORMULATIONS_MATERIALS_URL, "formulations-table-placeholder");
  document.getElementById("submit").disabled = true;
  document.getElementById("delete_formulations_batches_button").disabled = true;
  // Tooltip needs to be hidden manually to avoid a bug with chrome
  bootstrap.Tooltip.getInstance("#delete_formulations_batches_button").hide()
}

window.addEventListener("load", function () {
  document.getElementById("nav-bar-formulations").setAttribute("class", "nav-link active");
  document
    .getElementById("confirm_materials_and_processes_selection_button")
    .addEventListener("click", confirmSelection);
  document
    .getElementById("weight_constraint")
    .addEventListener("keyup", toggleSelectionConfirmationButtonAfterConstraintChange);
  document.getElementById("weight_constraint").addEventListener("keyup", autocorrectWeightValue);
  document.getElementById("powder_selection").addEventListener("change", toggleBasedOnSelectionAndConstraints);
  document.getElementById("liquid_selection").addEventListener("change", toggleBasedOnSelectionAndConstraints);
  document.getElementById("aggregates_selection").addEventListener("change", toggleBasedOnSelectionAndConstraints);
  document.getElementById("delete_formulations_batches_button").addEventListener("click", deleteFormulations);

  const formulations = document.getElementById("formulations_dataframe");
  if (formulations) {
    document.getElementById("submit").disabled = false;
    document.getElementById("delete_formulations_batches_button").disabled = false;
  }
});
