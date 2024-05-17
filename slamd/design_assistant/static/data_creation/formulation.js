export function assignEventsToFormulationStep(){
    const formulation_name_button = document.getElementById("formulation_button")
    if (formulation_name_button){
        formulation_name_button.addEventListener('click', handleGeneratingFormulation)
    }
}
function handleGeneratingFormulation(event){
    let new_url
    let material_type = document.querySelector(".material_type_field_choice").value.toLowerCase()
    new_url = window.location.href.replace('/design_assistant/', `/materials/formulations/${material_type}`)
    window.location.href = new_url
}
