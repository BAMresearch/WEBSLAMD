import {assignClickEventToSubmitButton, scrollDown, updateProgress} from "./../utils.js";

export function assignEventsToFormulation() {
    assignClickEventToSubmitButton("save_formulation_button", handleSavingFormulation)
}

async function handleSavingFormulation() {
    const design_knowledge = document.getElementById("design_knowledge").innerHTML
    const formulation = document.getElementById('formulation').innerHTML
    await postDataAndEmbedTemplateInPlaceholder("/design_assistant/zero_shot/save_formulation", "formulation_container", {
        "design_knowledge": design_knowledge,
        "formulation": formulation
    });
    updateProgress()
    scrollDown()
    document.getElementById("generate_design_knowledge_button").disabled = true
    document.getElementById("generate_formulation_button").disabled = true
    document.getElementById("design_knowledge").disabled = true
    document.getElementById("formulation_saved_message").classList.remove('d-none')
    document.getElementById("formulation_saved_message").classList.add('d-flex')
}