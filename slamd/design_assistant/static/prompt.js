import { assignClickEventToSubmitButton } from "./utils.js";

function handleGeneratePrompt() {
    document.getElementById("prompt_inner_container").classList.remove('d-none')
    insertSpinnerInPlaceholder("prompt_inner_container", true, CHATBOT_RESPONSE_SPINNER);
    setTimeout(async function handleSubmission() {
                await fetchDataAndEmbedTemplateInPlaceholder(
                    "/design_assistant/zero_shot/generate_prompt",
                    "prompt_inner_container",
                );
                // document.getElementById("generate_prompt_button").disabled = true
            }, 1000);
}

function handleContinue(){
    console.log('continue...')
}

export function assignEventsToPromptForm(){
    assignClickEventToSubmitButton("generate_prompt_button", handleGeneratePrompt)
    assignClickEventToSubmitButton("continue_prompt_button", handleContinue)
}