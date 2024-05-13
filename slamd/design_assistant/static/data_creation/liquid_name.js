import { updateProgress, scrollDown } from '../utils.js'
import { assignEventsToCostsLiquidStep } from './liquid_costs.js'

export function assignEventsToNameLiquidStep(){
    const liquid_name_input = document.getElementById("liquid_name_input")
    if (liquid_name_input){
        liquid_name_input.addEventListener('input', handleNamingLiquid)
    }
    const liquid_name_button = document.getElementById("liquid_name_button")
    if (liquid_name_button){
        liquid_name_button.addEventListener('click', handleSubmittingLiquidName)
    }
}

function handleNamingLiquid(event){
    if (event.target.value){
        document.getElementById("liquid_name_button").disabled = false
    }
    else {
        document.getElementById("liquid_name_button").disabled = true
    }
}

function handleSubmittingLiquidName(event){
    document.getElementById("liquid_name_input").disabled = true
    document.getElementById("liquid_name_button").disabled = true
    const liquid_name = document.getElementById("liquid_name_input").value
    const liquid = { 'material_type':'Liquid', 'material_name' : liquid_name }
    insertSpinnerInPlaceholder(
        "liquid_costs_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/new_project/liquid",
            "liquid_costs_container",
            liquid
        );
        assignEventsToCostsLiquidStep()
        updateProgress()
        scrollDown()
    }, 1000);
}
