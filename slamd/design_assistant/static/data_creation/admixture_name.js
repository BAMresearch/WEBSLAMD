import { updateProgress, scrollDown }from '../utils.js'
import { assignEventsToCostsAdmixtureStep } from './admixture_costs.js'

export function assignEventsToNameAdmixtureStep(){
    const admixture_name_input = document.getElementById("admixture_name_input")
    if (admixture_name_input){
        admixture_name_input.addEventListener('input', handleNamingAdmixture)
    }
    const admixture_name_button = document.getElementById("admixture_name_button")
    if (admixture_name_button){
        admixture_name_button.addEventListener('click', handleSubmittingAdmixtureName)
    }
}

function handleNamingAdmixture(event){
    if (event.target.value){
        document.getElementById("admixture_name_button").disabled = false
    }
    else {
        document.getElementById("admixture_name_button").disabled = true
    }
}

function handleSubmittingAdmixtureName(event){
    document.getElementById("admixture_name_input").disabled = true
    document.getElementById("admixture_name_button").disabled = true
    const admixture_name = document.getElementById("admixture_name_input").value
    const admixture = { 'material_type':'Admixture', 'material_name' : admixture_name }
    insertSpinnerInPlaceholder(
        "admixture_costs_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/admixture",
            "admixture_costs_container",
            admixture
        );
        assignEventsToCostsAdmixtureStep()
        updateProgress()
        scrollDown()
    }, 1000);
}
