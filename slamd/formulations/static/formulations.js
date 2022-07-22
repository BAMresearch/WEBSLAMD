const FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations`
let withConstraint = false
let weigthConstraint = undefined


function toggleSelectionConfirmationButton() {
    const material_selection = document.getElementById("material_selection")
    const materials_selected = Array.from(material_selection.options).filter(option => option.selected);

    const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");
    changeSelectionButton.disabled = materials_selected.length === 0
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

}

async function confirmSelection() {
    removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder")
    weigthConstraint = document.getElementById("weigth_constraint").value

    const materialsPlaceholder = document.getElementById("material_selection");
    const processesPlaceholder = document.getElementById("process_selection");

    const selectedMaterials = collectSelection(materialsPlaceholder);
    const selectedProcesses = collectSelection(processesPlaceholder);

    const url = `${FORMULATIONS_MATERIALS_URL}/add_min_max_entries/${selectedMaterials.length}/${selectedProcesses.length}`;
    await fetchEmbedTemplateInPlaceholder(url, "formulations_min_max_placeholder");

    prepareMaterialsMinMaxInputFieldsFromSelection(selectedMaterials);
    assignKeyboardEventsToFormulationsMinMaxForm();
}

function prepareMaterialsMinMaxInputFieldsFromSelection(selectedMaterials) {
    for (let i = 0; i < selectedMaterials.length; i++) {
        document.getElementById(`materials_min_max_entries-${i}-uuid_field`).value = selectedMaterials[i].uuid;
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

window.addEventListener("load", function () {
    document.getElementById("confirm_materials_and_processes_selection_button").addEventListener("click", confirmSelection);
    document.getElementById("material_selection").addEventListener("change", toggleSelectionConfirmationButton);
    document.getElementById("with_constraint").addEventListener("change", toggleWeigthConstraintInput);
});
