import {scrollDown, updateProgress, assignClickEventToSubmitButton} from "./../utils.js";
import { assignEventsToFormulation } from "./formulation.js";

export function assignEventsToDesignKnowledgeForm() {
    assignClickEventToSubmitButton("generate_design_knowledge_button", handleGeneratingDesignKnowledge)
    assignClickEventToSubmitButton("generate_formulation_button", handleGeneratingFormulation)
}

async function handleGeneratingDesignKnowledge(){
    insertSpinnerInPlaceholder("bot_message_spinner", true, CHATBOT_RESPONSE_SPINNER);
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/zero_shot/generate_design_knowledge",
            "design_knowledge",
            {"token": document.getElementById("token_form-token").value}
        );
        removeSpinnerInPlaceholder("bot_message_spinner", CHATBOT_RESPONSE_SPINNER)
        document.getElementById("bot_message_container_design_knowledge").classList.remove('d-none')
        scrollDown()
    }, 1000);
    document.getElementById("generate_formulation_button").disabled = false
}

async function handleGeneratingFormulation(){
    const design_knowledge = document.getElementById("design_knowledge").innerHTML
    const formulation_chat_message_container = document.getElementById("formulation_chat_message_container")
    if (!formulation_chat_message_container) {
        insertSpinnerInPlaceholder("formulation_container", true, CHATBOT_RESPONSE_SPINNER);
    }
    else {
        insertSpinnerInPlaceholder("formulation", false, CHATBOT_RESPONSE_SPINNER);
    }
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/zero_shot/generate_formulation",
            "formulation_container",
            {"design_knowledge" : design_knowledge ,"token": document.getElementById("token_form-token").value}
        );
        removeSpinnerInPlaceholder("formulation_container", CHATBOT_RESPONSE_SPINNER)
        updateProgress()
        scrollDown()
        assignEventsToFormulation()
    }, 1000);
}