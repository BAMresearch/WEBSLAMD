import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToOxideCompositionLiquidStep } from './liquid_oxide_composition.js'


export function assignEventsToCostsLiquidStep(){
    const liquid_cost_button = document.getElementById("liquid_costs_button")
    if (liquid_cost_button) {
        liquid_cost_button.addEventListener('click', handleSubmittingLiquidCosts)
    }
}

function handleSubmittingLiquidCosts(event){
    const liquid_cost_inputs = document.querySelectorAll(".liquid_cost_input") 
    const liquid_name = document.getElementById("liquid_name_input").value
    const liquid_cost_CO_2 = liquid_cost_inputs[0].value
    const liquid_cost_EUR = liquid_cost_inputs[1].value
    const liquid_cost_delivery_time = liquid_cost_inputs[2].value
    const liquid_cost_recyclingrate = liquid_cost_inputs[3].value
    const liquid = { 'material_type':'Liquid', 'material_name' : liquid_name,  "co2_footprint" : liquid_cost_CO_2, "costs" : liquid_cost_EUR, "delivery_time" : liquid_cost_delivery_time, "recyclingrate" : liquid_cost_recyclingrate }
    liquid_cost_inputs.forEach((liquid_cost_input) => {
        liquid_cost_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "liquid_oxide_composition_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/liquid",
            "liquid_oxide_composition_container",
            liquid
        );
        document.getElementById("liquid_costs_button").disabled = true 
        assignEventsToOxideCompositionLiquidStep()
        updateProgress()
        scrollDown()
    }, 1000);
}