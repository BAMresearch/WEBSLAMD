import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToFormulationStep } from './formulation.js'

export function assignEventsToInformationProcessStep(){
    const process_information_button = document.getElementById("process_information_button")
    if (process_information_button) {
        process_information_button.addEventListener('click', handleSubmittingProcessInformation)
    }
}

function handleSubmittingProcessInformation(event){
    const process_information_inputs = document.querySelectorAll(".process_information_input") 
    const process_cost_inputs = document.querySelectorAll(".process_cost_input")
    const process = { 
        'material_type':'Process', 
        'material_name' : document.getElementById("process_name_input").value,
        "co2_footprint" : process_cost_inputs[0].value,
        "costs" : process_cost_inputs[1].value,
        "delivery_time" : process_cost_inputs[2].value, 
        "duration" : process_information_inputs[0].value, 
        "temperature" : process_information_inputs[1].value, 
        "relative_humidity" : process_information_inputs[2].value, 
    }
    process_information_inputs.forEach((process_information_input) => {
        process_information_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "data_creation_formulation_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/process",
            "data_creation_formulation_container",
            process
        );
        document.getElementById("process_information_button").disabled = true
        assignEventsToFormulationStep()
        updateProgress()
        scrollDown()
    }, 1000);
}