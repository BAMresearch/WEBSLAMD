import { updateProgress, scrollDown } from '../utils.js'

export function assignEventsToStructuralCompositionPowderStep(){
    const powder_structural_composition_button = document.getElementById("powder_structural_composition_button")
    if (powder_structural_composition_button) {
        powder_structural_composition_button.addEventListener('click', handleSubmittingPowderStructuralComposition)
    }
}

function handleSubmittingPowderStructuralComposition(event){
    const powder_structural_composition_inputs = document.querySelectorAll(".powder_oxide_composition_input")
    const powder_structural_composition_fine = powder_structural_composition_inputs[0].value
    const powder_structural_composition_gravity = powder_structural_composition_inputs[1].value
    const powder_oxide_composition_inputs = document.querySelectorAll(".powder_oxide_composition_input")
    const powder_oxide_composition_ca_o = powder_oxide_composition_inputs[0].value
    const powder_oxide_composition_al2_o3 = powder_oxide_composition_inputs[1].value
    const powder_oxide_composition_si_o2 = powder_oxide_composition_inputs[2].value
    const powder_oxide_composition_fe3_o2 = powder_oxide_composition_inputs[3].value
    const powder_cost_inputs = document.querySelectorAll(".powder_cost_input") 
    const powder_name = document.getElementById("powder_name_input").value
    const powder_cost_CO_2 = powder_cost_inputs[0].value
    const powder_cost_EUR = powder_cost_inputs[1].value
    const powder_cost_delivery_time = powder_cost_inputs[2].value
    const powder = { 'material_type':'Powder', 'material_name' : powder_name,  "co2_footprint" : powder_cost_CO_2, "costs" : powder_cost_EUR, "delivery_time" : powder_cost_delivery_time, "fe3_o2" : powder_oxide_composition_fe3_o2, "si_o2" : powder_oxide_composition_si_o2, "al2_o3" : powder_oxide_composition_al2_o3, "ca_o" : powder_oxide_composition_ca_o, "fine" : powder_structural_composition_fine, "gravity" : powder_structural_composition_gravity}
    powder_structural_composition_inputs.forEach((powder_structural_composition_input) => {
        powder_structural_composition_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "liquid_name_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/powder",
            "liquid_name_container",
            powder
        );
        document.getElementById("powder_structural_composition_button").disabled = true 
        updateProgress()
        scrollDown()
    }, 1000);
}