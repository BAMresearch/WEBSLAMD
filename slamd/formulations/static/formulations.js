const FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations`
let withConstraint = false
let weigthConstraint = ""

function toggleSelectionConfirmationButtonAfterMaterialSelection() {
    toggleBasedOnSelectionAndConstraints();
}

function toggleBasedOnSelectionAndConstraints() {
    const powder_selection = document.getElementById("powder_selection");
    const materials_selected = Array.from(powder_selection.options).filter(option => option.selected);

    const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");

    const validConstraintConfiguration = withConstraint && (weigthConstraint !== undefined && weigthConstraint !== "");
    if (!withConstraint) {
        changeSelectionButton.disabled = materials_selected.length === 0;
    } else {
        changeSelectionButton.disabled = materials_selected.length === 0 || !validConstraintConfiguration;
    }
}

function toggleSelectionConfirmationButtonAfterConstraintChange() {
    let weightConstraintInput = document.getElementById("weigth_constraint");

    fixInputValue(weightConstraintInput)

    weigthConstraint = weightConstraintInput.value;
    toggleBasedOnSelectionAndConstraints();
}

function toggleWeigthConstraintInput() {
    const with_constraint = document.getElementById("with_constraint")
    withConstraint = with_constraint.checked;
    if (withConstraint) {
        document.getElementById("weigth_constraint").disabled = false
    } else {
        document.getElementById("weigth_constraint").disabled = true
        document.getElementById("weigth_constraint").value = ""
    }
    document.getElementById("change_materials_and_processes_selection_button").disabled = true;
}

async function confirmSelection() {
    removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder")
    removeInnerHtmlFromPlaceholder("formulations_weights_placeholder")
    document.getElementById("submit").disabled = true
    weigthConstraint = document.getElementById("weigth_constraint").value

    const materialsPlaceholder = document.getElementById("powder_selection");
    const processesPlaceholder = document.getElementById("process_selection");

    const selectedMaterials = collectSelectionForFormulations(materialsPlaceholder);
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
        document.getElementById("submit").disabled = false
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

function prepareMaterialsMinMaxInputFieldsFromSelection(selectedMaterials) {
    for (let i = 0; i < selectedMaterials.length; i++) {
        document.getElementById(`materials_min_max_entries-${i}-uuid_field`).value = selectedMaterials[i].uuid;
        document.getElementById(`materials_min_max_entries-${i}-type_field`).value = selectedMaterials[i].type;
        document.getElementById(`materials_min_max_entries-${i}-materials_entry_name`).value = selectedMaterials[i].name;
        if (withConstraint) {
            if (i === selectedMaterials.length - 1) {
                document.getElementById(`materials_min_max_entries-${i}-increment`).disabled = true;
                document.getElementById(`materials_min_max_entries-${i}-max`).disabled = true;
                document.getElementById(`materials_min_max_entries-${i}-min`).disabled = true;
            }
        }
    }
    if (selectedMaterials.length === 1) {
        document.getElementById("materials_min_max_entries-0-min").value = weigthConstraint
        document.getElementById("materials_min_max_entries-0-max").value = weigthConstraint
        if (withConstraint) {
            document.getElementById("confirm_formulations_configuration_button").disabled = false
        }
    }
}

function prepareProcessMinMaxInputFieldsFromSelection(selectedProcesses) {
    for (let i = 0; i < selectedProcesses.length; i++) {
        document.getElementById(`processes_entries-${i}-uuid_field`).value = selectedProcesses[i].uuid;
        document.getElementById(`processes_entries-${i}-process_name`).value = selectedProcesses[i].name;
    }
}

window.addEventListener("load", function () {
    document.getElementById("confirm_materials_and_processes_selection_button").addEventListener("click", confirmSelection);
    document.getElementById("powder_selection").addEventListener("change", toggleSelectionConfirmationButtonAfterMaterialSelection);
    document.getElementById("with_constraint").addEventListener("change", toggleWeigthConstraintInput);
    document.getElementById("weigth_constraint").addEventListener("change", toggleSelectionConfirmationButtonAfterConstraintChange);
});
