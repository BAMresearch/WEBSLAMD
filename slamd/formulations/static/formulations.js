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
    const validConstraintConfiguration = weightConstraint !== undefined && weightConstraint !== "";

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
    await postDataAndEmbedTemplateInPlaceholder(url, "formulations_min_max_placeholder", selectedMaterials);

    addListenersToIndependentFields();
    assignConfirmFormulationsConfigurationEvent();
}

async function assignConfirmFormulationsConfigurationEvent() {
    const button = document.getElementById("confirm_formulations_configuration_button");
    enableTooltip(button);

    button.addEventListener("click", async () => {
        const requestData = collectFormulationsMinMaxRequestData();
        const url = `${FORMULATIONS_MATERIALS_URL}/add_weights`;
        await postDataAndEmbedTemplateInPlaceholder(url, "formulations_weights_placeholder", requestData);
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
        await postDataAndEmbedTemplateInPlaceholder(url, "formulations_tables_placeholder", formulationsRequest);
        document.getElementById("submit").disabled = false;
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

async function deleteFormulations() {
    await deleteDataAndEmbedTemplateInPlaceholder(FORMULATIONS_MATERIALS_URL, "formulations_tables_placeholder");
    document.getElementById("submit").disabled = true;
}

window.addEventListener("load", function () {
    document.getElementById("nav-bar-formulations").setAttribute("class", "nav-link active");
    document
        .getElementById("confirm_materials_and_processes_selection_button")
        .addEventListener("click", confirmSelection);
    document
        .getElementById("weight_constraint")
        .addEventListener("change", toggleSelectionConfirmationButtonAfterConstraintChange);
    document.getElementById("weight_constraint").addEventListener("keyup", autocorrectWeightValue);
    document.getElementById("powder_selection").addEventListener("keyup", toggleBasedOnSelectionAndConstraints);
    document.getElementById("liquid_selection").addEventListener("keyup", toggleBasedOnSelectionAndConstraints);
    document.getElementById("aggregates_selection").addEventListener("keyup", toggleBasedOnSelectionAndConstraints);
    document.getElementById("delete_formulations_batches_button").addEventListener("click", deleteFormulations);

    const formulations = document.getElementById("formulations_dataframe");
    if (formulations) {
        document.getElementById("submit").disabled = false;
    }
});
