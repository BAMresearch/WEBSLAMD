import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToNameProcessStep } from './process_name.js'

export function assignEventsToCostsAdmixtureStep(){
    const admixture_cost_button = document.getElementById("admixture_costs_button")
    if (admixture_cost_button) {
        admixture_cost_button.addEventListener('click', handleSubmittingAdmixtureCosts)
    }
}

function handleSubmittingAdmixtureCosts(event){
    const admixture_cost_inputs = document.querySelectorAll(".admixture_cost_input") 
    const admixture_name = document.getElementById("admixture_name_input").value
    const admixture_cost_CO_2 = admixture_cost_inputs[0].value
    const admixture_cost_EUR = admixture_cost_inputs[1].value
    const admixture_cost_delivery_time = admixture_cost_inputs[2].value
    const admixture_cost_recyclingrate = admixture_cost_inputs[3].value
    const admixture = { 'material_type':'Admixture', 'material_name' : admixture_name,  "co2_footprint" : admixture_cost_CO_2, "costs" : admixture_cost_EUR, "delivery_time" : admixture_cost_delivery_time, "recyclingrate" : admixture_cost_recyclingrate }
    admixture_cost_inputs.forEach((admixture_cost_input) => {
        admixture_cost_input.disabled = true
    })
    insertSpinnerInPlaceholder(
        "process_name_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/admixture",
            "process_name_container",
            admixture
        );
        document.getElementById("admixture_costs_button").disabled = true 
        assignEventsToNameProcessStep()
        updateProgress()
        scrollDown()
    }, 1000);
}