import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToNameAdmixtureStep } from './admixture_name.js'

export function assignEventsToCompositionAggregateStep(){
    const aggregate_composition_button = document.getElementById("aggregate_composition_button")
    if (aggregate_composition_button) {
        aggregate_composition_button.addEventListener('click', handleSubmittingAggregateComposition)
    }
}

function handleSubmittingAggregateComposition(event){
    const aggregate_composition_inputs = document.querySelectorAll(".aggregate_composition_input") 
    const aggregate_cost_inputs = document.querySelectorAll(".aggregate_cost_input")
    console.log(aggregate_composition_inputs)
    const aggregate = { 
        'material_type':'Aggregates', 
        'material_name' : document.getElementById("aggregate_name_input").value,
        "co2_footprint" : aggregate_cost_inputs[0].value,
        "costs" : aggregate_cost_inputs[1].value,
        "delivery_time" : aggregate_cost_inputs[2].value,
        "recyclingrate" : aggregate_cost_inputs[3].value,
        "fine_aggregates" : aggregate_composition_inputs[0].value, 
        "coarse_aggregates" : aggregate_composition_inputs[1].value,
        "fineness_modulus" : aggregate_composition_inputs[3].value,
        "water_absorption" : aggregate_composition_inputs[4].value
    }
    aggregate_composition_inputs.forEach((aggregate_composition_input) => {
        aggregate_composition_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "admixture_name_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/aggregate",
            "admixture_name_container",
            aggregate
        );
        document.getElementById("aggregate_composition_button").disabled = true
        assignEventsToNameAdmixtureStep()
        updateProgress()
        scrollDown()
    }, 1000);
}