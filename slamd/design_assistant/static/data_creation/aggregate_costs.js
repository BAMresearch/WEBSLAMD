import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToCompositionAggregateStep } from './aggregate_composition.js'

export function assignEventsToCostsAggregateStep(){
    const aggregate_cost_button = document.getElementById("aggregate_costs_button")
    if (aggregate_cost_button) {
        aggregate_cost_button.addEventListener('click', handleSubmittingAggregateCosts)
    }
}

function handleSubmittingAggregateCosts(event){
    const aggregate_cost_inputs = document.querySelectorAll(".aggregate_cost_input") 
    const aggregate_name = document.getElementById("aggregate_name_input").value
    const aggregate_cost_CO_2 = aggregate_cost_inputs[0].value
    const aggregate_cost_EUR = aggregate_cost_inputs[1].value
    const aggregate_cost_delivery_time = aggregate_cost_inputs[2].value
    const aggregate_cost_recyclingrate = aggregate_cost_inputs[3].value
    const aggregate = { 'material_type':'Aggregates', 'material_name' : aggregate_name,  "co2_footprint" : aggregate_cost_CO_2, "costs" : aggregate_cost_EUR, "delivery_time" : aggregate_cost_delivery_time, "recyclingrate" : aggregate_cost_recyclingrate }
    aggregate_cost_inputs.forEach((aggregate_cost_input) => {
        aggregate_cost_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "aggregate_composition_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/aggregate",
            "aggregate_composition_container",
            aggregate
        );
        document.getElementById("aggregate_costs_button").disabled = true 
        assignEventsToCompositionAggregateStep()
        updateProgress()
        scrollDown()
    }, 1000);
}