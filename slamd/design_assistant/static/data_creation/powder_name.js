import { updateProgress, scrollDown }from '../utils.js'
import { assignEventsToCostsPowderStep } from './powder_costs.js'

export function assignEventsToNamePowderStep(){
    const powder_name_input = document.getElementById("powder_name_input")
    if (powder_name_input){
        powder_name_input.addEventListener('input', handleNamingPowder)
    }
    const powder_name_button = document.getElementById("powder_name_button")
    if (powder_name_button){
        powder_name_button.addEventListener('click', handleSubmittingPowderName)
    }
}

function handleNamingPowder(event){
    if (event.target.value){
        document.getElementById("powder_name_button").disabled = false
    }
    else {
        document.getElementById("powder_name_button").disabled = true
    }
}

function handleSubmittingPowderName(event){
    document.getElementById("powder_name_input").disabled = true
    document.getElementById("powder_name_button").disabled = true
    const powder_name = document.getElementById("powder_name_input").value
    const powder = { 'material_type':'Powder', 'material_name' : powder_name }
    insertSpinnerInPlaceholder(
        "powder_costs_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/powder",
            "powder_costs_container",
            powder
        );
        assignEventsToCostsPowderStep()
        updateProgress()
        scrollDown()
    }, 1000);
}
