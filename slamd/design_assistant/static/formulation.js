import { assignClickEventToSubmitButton } from "./utils.js";

export function assignEventsToFormulation(){
    assignClickEventToSubmitButton("save_formulation_button", handleSavingFormulation)
}

async function handleSavingFormulation(){
    const design_knowledge = document.getElementById("design_knowledge").innerHTML
    const formulation = document.getElementById('formulation').innerHTML
    await postDataAndEmbedTemplateInPlaceholder("/design_assistant/zero_shot/save_formulation", "formulation_container", {"design_knowledge": design_knowledge, "formulation" : formulation});
}