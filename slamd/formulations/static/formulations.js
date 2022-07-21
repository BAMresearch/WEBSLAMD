const FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations`

function toggleSelectionConfirmationButton() {
    const material_selection = document.getElementById("material_selection")
    const materials_selected = Array.from(material_selection.options).filter(option => option.selected);

    const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");
    changeSelectionButton.disabled = materials_selected.length === 0
}

async function confirmSelection() {
    removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder")

    const materialsPlaceholder = document.getElementById("material_selection");
    const processesPlaceholder = document.getElementById("process_selection");

    const selectedMaterials = collectSelection(materialsPlaceholder);
    const selectedProcesses = collectSelection(processesPlaceholder);

    const numberOfRequestsFields = selectedMaterials.length + selectedProcesses.length

    const url = `${FORMULATIONS_MATERIALS_URL}/add_min_max_entries/${numberOfRequestsFields}`;
    await fetchEmbedTemplateInPlaceholder(url, "formulations_min_max_placeholder");

    prepareMaterialsMinMaxInputFieldsFromSelection(selectedMaterials);
    prepareProcessMinMaxInputFieldsFromSelection(selectedProcesses, selectedMaterials.length);
    // assignKeyboardEventsToMinMaxForm();
    // assignConfirmBlendingConfigurationEvent();
}

function prepareMaterialsMinMaxInputFieldsFromSelection(selectedMaterials) {
    for (let i = 0; i < selectedMaterials.length; i++) {
        document.getElementById(`all_formulations_min_max_entries-${i}-uuid_field`).value = selectedMaterials[i].uuid;
        document.getElementById(`all_formulations_min_max_entries-${i}-formulations_entry_name`).value = selectedMaterials[i].name;
    }
}

function prepareProcessMinMaxInputFieldsFromSelection(selectedProcesses, materialsLength) {
    for (let i = materialsLength; i < materialsLength + selectedProcesses.length; i++) {
        document.getElementById(`all_formulations_min_max_entries-${i}-uuid_field`).value = selectedProcesses[i - materialsLength].uuid;
        document.getElementById(`all_formulations_min_max_entries-${i}-formulations_entry_name`).value = selectedProcesses[i - materialsLength].name;
    }
}

window.addEventListener("load", function () {
    document.getElementById("confirm_materials_and_processes_selection_button").addEventListener("click", confirmSelection);
    document.getElementById("material_selection").addEventListener("change", toggleSelectionConfirmationButton);
});
