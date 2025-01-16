import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToNameAggregateStep } from './aggregate_name.js'

export function assignEventsToOxideCompositionLiquidStep(){
    const liquid_oxide_composition_button = document.getElementById("liquid_oxide_composition_button")
    if (liquid_oxide_composition_button) {
        liquid_oxide_composition_button.addEventListener('click', handleSubmittingLiquidOxideComposition)
    }
}

function handleSubmittingLiquidOxideComposition(event){
    const liquid_oxide_composition_inputs = document.querySelectorAll(".liquid_oxide_composition_input") 
    const liquid_cost_inputs = document.querySelectorAll(".liquid_cost_input")
    const liquid = { 
        'material_type':'Liquid', 
        'material_name' : document.getElementById("liquid_name_input").value,
        "co2_footprint" : liquid_cost_inputs[0].value,
        "costs" : liquid_cost_inputs[1].value,
        "delivery_time" : liquid_cost_inputs[2].value,
        "recyclingrate" : liquid_cost_inputs[3].value,
        "h2_o" : liquid_oxide_composition_inputs[0].value, 
        "h2_o_mol" : liquid_oxide_composition_inputs[1].value, 
        "na_o_h" : liquid_oxide_composition_inputs[2].value, 
        "na_o_h_mol" : liquid_oxide_composition_inputs[3].value,
        "na2_si_o3" : liquid_oxide_composition_inputs[4].value,
        "na2_si_o3_mol" : liquid_oxide_composition_inputs[5].value 
    }
    liquid_oxide_composition_inputs.forEach((liquid_oxide_composition_input) => {
        liquid_oxide_composition_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "aggregate_name_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/liquid",
            "aggregate_name_container",
            liquid
        );
        document.getElementById("liquid_oxide_composition_button").disabled = true
        assignEventsToNameAggregateStep()
        updateProgress()
        scrollDown()
    }, 1000);
}