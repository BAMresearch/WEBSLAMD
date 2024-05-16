import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToInformationProcessStep } from './process_information.js'


export function assignEventsToCostsProcessStep(){
    const process_cost_button = document.getElementById("process_costs_button")
    if (process_cost_button) {
        process_cost_button.addEventListener('click', handleSubmittingProcessCosts)
    }
}

function handleSubmittingProcessCosts(event){
    const process_cost_inputs = document.querySelectorAll(".process_cost_input") 
    const process_name = document.getElementById("process_name_input").value
    const process_cost_CO_2 = process_cost_inputs[0].value
    const process_cost_EUR = process_cost_inputs[1].value
    const process_cost_delivery_time = process_cost_inputs[2].value
    const process = { 'material_type':'Process', 'material_name' : process_name,  "co2_footprint" : process_cost_CO_2, "costs" : process_cost_EUR, "delivery_time" : process_cost_delivery_time }
    process_cost_inputs.forEach((process_cost_input) => {
        process_cost_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "process_information_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/process",
            "process_information_container",
            process
        );
        document.getElementById("process_costs_button").disabled = true 
        assignEventsToInformationProcessStep()
        updateProgress()
        scrollDown()
    }, 1000);
}