const FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations`
let withConstraint = false
let weigthConstraint = ""

function toggleBasedOnSelectionAndConstraints() {
    const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");

    const validConstraintConfiguration = withConstraint && (weigthConstraint !== undefined && weigthConstraint !== "");
    if (withConstraint) {
        changeSelectionButton.disabled = !validConstraintConfiguration;
    }
}

function toggleSelectionConfirmationButtonAfterConstraintChange() {
    weigthConstraint = document.getElementById("weigth_constraint").value;
    toggleBasedOnSelectionAndConstraints();
}

function autocorrectWeightValue(){
    let weightConstraintInput = document.getElementById("weigth_constraint");

    fixInputValue(weightConstraintInput)
}

function toggleWeigthConstraintInput() {
    const with_constraint = document.getElementById("with_constraint")
    removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder")
    removeInnerHtmlFromPlaceholder("formulations_weights_placeholder")

    withConstraint = with_constraint.checked;
    if (withConstraint) {
        document.getElementById("weigth_constraint").disabled = false
        document.getElementById("change_materials_and_processes_selection_button").disabled = true;
    } else {
        document.getElementById("weigth_constraint").disabled = true
        document.getElementById("weigth_constraint").value = ""
        document.getElementById("change_materials_and_processes_selection_button").disabled = false;
    }
}

async function confirmSelection() {
    removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder")
    removeInnerHtmlFromPlaceholder("formulations_weights_placeholder")
    document.getElementById("submit").disabled = true
    weigthConstraint = document.getElementById("weigth_constraint").value

    const selectedMaterials = collectAllSelectedMaterials();

    const processesPlaceholder = document.getElementById("process_selection");
    const selectedProcesses = collectSelection(processesPlaceholder);

    const url = `${FORMULATIONS_MATERIALS_URL}/add_min_max_entries/${selectedMaterials.length}/${selectedProcesses.length}`;
    await fetchEmbedTemplateInPlaceholder(url, "formulations_min_max_placeholder");

    prepareMaterialsMinMaxInputFieldsFromSelection(selectedMaterials);
    prepareProcessMinMaxInputFieldsFromSelection(selectedProcesses)
    assignKeyboardEventsToFormulationsMinMaxForm();
    assignConfirmFormulationsConfigurationEvent();
}

async function assignConfirmFormulationsConfigurationEvent() {
    const elem = document.getElementById("confirm_formulations_configuration_button");

    elem.addEventListener("click", async () => {
        const requestData = collectFormulationsMinMaxRequestData();
        const url = `${FORMULATIONS_MATERIALS_URL}/add_weights`;
        await postDataAndEmbedTemplateInPlaceholder(url, "formulations_weights_placeholder", requestData)
        assignDeleteWeightEvent();
        assignCreateFormulationsBatchEvent()
    })
}

function assignCreateFormulationsBatchEvent(){
    document.getElementById("create_formulations_batch_button").addEventListener("click", async () => {

        const materialsRequestData = collectFormulationsMinMaxRequestData();
        const processesRequestData = collectProcessesRequestData();

        const formulationsRequest = {
            materials_request_data: materialsRequestData,
            processes_request_data: processesRequestData
        }

        const url = `${FORMULATIONS_MATERIALS_URL}/create_formulations_batch`;
        await postDataAndEmbedTemplateInPlaceholder(url, "dataframe_placeholder", formulationsRequest)
    })
}

function assignDeleteWeightEvent() {
    let numberOfWeightEntries = document.querySelectorAll('[id^="all_weights_entries-"]').length;

    for (let i = 0; i < numberOfWeightEntries; i++) {
        let deleteButton = document.getElementById(`delete_weight_button___${i}`);
        deleteButton.addEventListener("click", () => {
            document.getElementById(`all_weights_entries-${i}-weights`).remove()
            deleteButton.remove();
        })
    }
}

window.addEventListener("load", function () {
    document.getElementById("change_materials_and_processes_selection_button").disabled = false;
    document.getElementById("confirm_materials_and_processes_selection_button").addEventListener("click", confirmSelection);
    document.getElementById("with_constraint").addEventListener("change", toggleWeigthConstraintInput);
    document.getElementById("weigth_constraint").addEventListener("change", toggleSelectionConfirmationButtonAfterConstraintChange);
    document.getElementById("weigth_constraint").addEventListener("keyup", autocorrectWeightValue);
});
