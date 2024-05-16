import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToCostsAggregateStep } from './aggregate_costs.js'

export function assignEventsToNameAggregateStep(){
    const aggregate_name_input = document.getElementById("aggregate_name_input")
    if (aggregate_name_input){
        aggregate_name_input.addEventListener('input', handleNamingAggregate)
    }
    const aggregate_name_button = document.getElementById("aggregate_name_button")
    if (aggregate_name_button){
        aggregate_name_button.addEventListener('click', handleSubmittingAggregateName)
    }
}

function handleNamingAggregate(event){
    if (event.target.value){
        document.getElementById("aggregate_name_button").disabled = false
    }
    else {
        document.getElementById("aggregate_name_button").disabled = true
    }
}

function handleSubmittingAggregateName(event){
    document.getElementById("aggregate_name_input").disabled = true
    document.getElementById("aggregate_name_button").disabled = true
    const aggregate_name = document.getElementById("aggregate_name_input").value
    const aggregate = { 'material_type':'Aggregates', 'material_name' : aggregate_name }
    insertSpinnerInPlaceholder(
        "aggregate_costs_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/aggregate",
            "aggregate_costs_container",
            aggregate
        );
        assignEventsToCostsAggregateStep()
        updateProgress()
        scrollDown()
    }, 1000);
}
