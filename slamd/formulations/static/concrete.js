const CONCRETE_FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations/concrete`;
let concreteWeightConstraint = "";
let materialsSpecificGravity = {}

/**
 * Despite the fact that some functions in binder.js and concrete.js look rather similar, we choose not to
 * extract too many common methods as the internal logic for the two cases might diverge. In order not to create
 * too much coupling between usecase which are different we explicitly prefer duplicating some parts of the code here.
 */
function toggleBasedOnSelectionAndConstraints() {
    const powderPlaceholder = document.getElementById("powder_selection");
    const liquidPlaceholder = document.getElementById("liquid_selection");
    const aggregatesPlaceholder = document.getElementById("aggregates_selection");
    concreteWeightConstraint = document.getElementById("constraint").value;


    const powderSelected = atLeastOneItemIsSelected(powderPlaceholder);
    const liquidSelected = atLeastOneItemIsSelected(liquidPlaceholder);
    const aggregatesSelected = atLeastOneItemIsSelected(aggregatesPlaceholder);

    const validSelectionConfiguration = powderSelected && liquidSelected && aggregatesSelected;
    const validConstraintConfiguration = concreteWeightConstraint !== undefined && concreteWeightConstraint !== "" &&
        concreteWeightConstraint > 0;

    const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");
    changeSelectionButton.disabled = !(validSelectionConfiguration && validConstraintConfiguration);
}

function toggleSelectionConfirmationButtonAfterConstraintChange() {
    concreteWeightConstraint = document.getElementById("constraint").value;
    toggleBasedOnSelectionAndConstraints();
}

async function confirmSelection() {
    removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder");
    removeInnerHtmlFromPlaceholder("formulations_weights_placeholder");
    document.getElementById("submit").disabled = true;
    concreteWeightConstraint = document.getElementById("constraint").value;
    const selectedMaterials = collectBuildingMaterialFormulationSelection();
    const selectedConstraintType = document.getElementById("constraint_selection").value;
    const url = `${CONCRETE_FORMULATIONS_MATERIALS_URL}/add_min_max_entries`;

    body = {
        "selected_materials" : selectedMaterials,
        "selected_constraint_type" : selectedConstraintType
    }

    insertSpinnerInPlaceholder("formulations_min_max_placeholder");
    await postDataAndEmbedTemplateInPlaceholder(url, "formulations_min_max_placeholder", body);
    removeSpinnerInPlaceholder("formulations_min_max_placeholder");

    addListenersToIndependentFields(CONCRETE);
    assignConfirmFormulationsConfigurationEvent();
}

async function assignConfirmFormulationsConfigurationEvent() {
    const button = document.getElementById("create_formulations_batch_button");
    enableTooltip(button);

    button.addEventListener("click", async () => {
        const requestData = collectFormulationsMinMaxRequestData(CONCRETE);
        const url = `${CONCRETE_FORMULATIONS_MATERIALS_URL}/create_formulations_batch`;
        const token = document.getElementById("csrf_token").value;
        const constraintType = document.getElementById('constraint_selection')
        const processesRequestData = collectProcessesRequestData();
        requestData['selected_constraint_type'] = constraintType.value
        requestData['processes_request_data'] = processesRequestData
        requestData['sampling_size'] = 1

        insertSpinnerInPlaceholder("formulations-table-placeholder");
        await postDataAndEmbedTemplateInPlaceholder(url, "formulations-table-placeholder", requestData);
        removeSpinnerInPlaceholder("formulations-table-placeholder");

        document.getElementById("submit").disabled = false;
        document.getElementById("delete_formulations_batches_button").disabled = false;
    });
}



async function deleteFormulations() {
    await deleteDataAndEmbedTemplateInPlaceholder(CONCRETE_FORMULATIONS_MATERIALS_URL, "formulations-table-placeholder");
    document.getElementById("submit").disabled = true;
    document.getElementById("delete_formulations_batches_button").disabled = true;
    // Tooltip needs to be hidden manually to avoid a bug with chrome
    bootstrap.Tooltip.getInstance("#delete_formulations_batches_button").hide()
}

window.addEventListener("load", function () {
    document.getElementById("confirm_materials_and_processes_selection_button").addEventListener("click", confirmSelection);
    document.getElementById("constraint").addEventListener("keyup", toggleSelectionConfirmationButtonAfterConstraintChange);
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
