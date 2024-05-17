export function assignEventsToFormulationStep(){
    const formulation_name_button = document.getElementById("formulation_button")
    if (formulation_name_button){
        formulation_name_button.addEventListener('click', handleGeneratingFormulation)
    }
}
function handleGeneratingFormulation(event){
    let new_url
    let material_type_selection
    const material_types = document.querySelectorAll(".material_type_field_choice")
    material_types.forEach((material_type) => {
        if (material_type.checked){
            material_type_selection = material_type.value.toLowerCase()
        }
    });
    new_url = window.location.href.replace('/design_assistant/', `/materials/formulations/${material_type_selection}`)
    window.location.href = new_url
}
