import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToNameLiquidStep } from './liquid_name.js'

export function assignEventsToStructuralCompositionPowderStep(){
    const powder_structural_composition_button = document.getElementById("powder_structural_composition_button")
    if (powder_structural_composition_button) {
        powder_structural_composition_button.addEventListener('click', handleSubmittingPowderStructuralComposition)
    }
}

function handleSubmittingPowderStructuralComposition(event){
    const powder_cost_inputs = document.querySelectorAll(".powder_cost_input") 
    const powder_oxide_composition_inputs = document.querySelectorAll(".powder_oxide_composition_input")
    const powder_structural_composition_inputs = document.querySelectorAll(".powder_structural_composition_input")
    const powder = { 
        'material_type':'Powder', 
        'material_name' : document.getElementById("powder_name_input").value,
        "co2_footprint" : powder_cost_inputs[0].value,
        "costs" : powder_cost_inputs[1].value,
        "delivery_time" : powder_cost_inputs[2].value,
        "recyclingrate" : powder_cost_inputs[3].value,
        "ca_o" : powder_oxide_composition_inputs[0].value, 
        "al2_o3" : powder_oxide_composition_inputs[1].value, 
        "si_o2" : powder_oxide_composition_inputs[2].value, 
        "fe3_o2" : powder_oxide_composition_inputs[3].value,
        "fine" : powder_structural_composition_inputs[0].value,
    }
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
        assignEventsToNameLiquidStep()
        updateProgress()
        scrollDown()
    }, 1000);
}