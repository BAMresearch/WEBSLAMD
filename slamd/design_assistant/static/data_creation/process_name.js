import { updateProgress, scrollDown }from '../utils.js'
import { assignEventsToCostsProcessStep } from './process_costs.js'

export function assignEventsToNameProcessStep(){
    const process_name_input = document.getElementById("process_name_input")
    if (process_name_input){
        process_name_input.addEventListener('input', handleNamingProcess)
    }
    const process_name_button = document.getElementById("process_name_button")
    if (process_name_button){
        process_name_button.addEventListener('click', handleSubmittingProcessName)
    }
}

function handleNamingProcess(event){
    if (event.target.value){
        document.getElementById("process_name_button").disabled = false
    }
    else {
        document.getElementById("process_name_button").disabled = true
    }
}

function handleSubmittingProcessName(event){
    document.getElementById("process_name_input").disabled = true
    document.getElementById("process_name_button").disabled = true
    const process_name = document.getElementById("process_name_input").value
    const process = { 'material_type':'process', 'material_name' : process_name }
    insertSpinnerInPlaceholder(
        "process_costs_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/process",
            "process_costs_container",
            process
        );
        assignEventsToCostsProcessStep()
        updateProgress()
        scrollDown()
    }, 1000);
}
