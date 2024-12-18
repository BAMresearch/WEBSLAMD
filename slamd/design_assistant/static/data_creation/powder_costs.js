import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToOxideCompositionPowderStep } from './powder_oxide_composition.js'

export function assignEventsToCostsPowderStep(){
    const powder_cost_button = document.getElementById("powder_costs_button")
    if (powder_cost_button) {
        powder_cost_button.addEventListener('click', handleSubmittingPowderCosts)
    }
}

function handleSubmittingPowderCosts(event){
    const powder_cost_inputs = document.querySelectorAll(".powder_cost_input") 
    const powder_name = document.getElementById("powder_name_input").value
    const powder_cost_CO_2 = powder_cost_inputs[0].value
    const powder_cost_EUR = powder_cost_inputs[1].value
    const powder_cost_delivery_time = powder_cost_inputs[2].value
    const powder_cost_recyclingrate = powder_cost_inputs[3].value
    const powder = { 'material_type':'Powder', 'material_name' : powder_name,  "co2_footprint" : powder_cost_CO_2, "costs" : powder_cost_EUR, "delivery_time" : powder_cost_delivery_time, "recyclingrate" : powder_cost_recyclingrate }
    powder_cost_inputs.forEach((powder_cost_input) => {
        powder_cost_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "powder_oxide_composition_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/powder",
            "powder_oxide_composition_container",
            powder
        );
        document.getElementById("powder_costs_button").disabled = true 
        assignEventsToOxideCompositionPowderStep()
        updateProgress()
        scrollDown()
    }, 1000);
}