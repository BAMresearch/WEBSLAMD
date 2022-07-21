function toggleSelectionConfirmationButton() {
    const material_selection = document.getElementById("material_selection")
    const materials_selected = Array.from(material_selection.options).filter(option => option.selected);

    const selected_processes = document.getElementById("process_selection")
    const processes_selected = Array.from(selected_processes.options).filter(option => option.selected);

    const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");
    changeSelectionButton.disabled = !(materials_selected.length > 0 && processes_selected > 0);
}

function selectMaterialsAndProcesses() {
    console.log("")
}

window.addEventListener("load", function () {
    document.getElementById("confirm_materials_and_processes_selection_button").addEventListener("click", selectMaterialsAndProcesses);
    document.getElementById("material_selection").addEventListener("change", toggleSelectionConfirmationButton);
    document.getElementById("process_selection").addEventListener("change", toggleSelectionConfirmationButton);
});
