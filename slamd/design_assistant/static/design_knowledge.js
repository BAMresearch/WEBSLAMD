export function assignEventsToDesignKnowledge() {
    assignClickEventToGenerateDesignKnowledgeButton()
    assignClickEventToContinueButton()
}

export function assignClickEventToGenerateDesignKnowledgeButton(){
    const generate_design_knowledge_button = document.getElementById("generate_design_knowledge_button")
    if (generate_design_knowledge_button){
        generate_design_knowledge_button.addEventListener('click', async function () {
            insertSpinnerInPlaceholder(
                "llm_response_container",
                true,
                CHATBOT_RESPONSE_SPINNER
            );
            setTimeout(async function handleSubmission() {
                await fetchDataAndEmbedTemplateInPlaceholder('/design_assistant/zero_shot/generate_design_knowledge', 'llm_response')
                removeSpinnerInPlaceholder("llm_response_container", CHATBOT_RESPONSE_SPINNER)
                document.getElementById("llm_response").classList.remove('d-none')
            }, 1000);
            document.getElementById("continue_design_knowledge_button").disabled = false
            document.getElementById("llm_response").disabled = false

        })
    }
}

export function assignClickEventToContinueButton(){
    const continue_design_knowledge_button = document.getElementById("continue_design_knowledge_button")
    if (continue_design_knowledge_button) {
        continue_design_knowledge_button.addEventListener('click', function () {
            const design_knowledge = document.getElementById("llm_response").innerHTML
            insertSpinnerInPlaceholder(
                "prompt_container",
                true,
                CHATBOT_RESPONSE_SPINNER
            );
            setTimeout(async function handleSubmission() {
                await postDataAndEmbedTemplateInPlaceholder(
                    "/design_assistant/zero_shot/generate_prompt",
                    "prompt_container",
                    design_knowledge
                );
                document.getElementById("continue_design_knowledge_button").disabled = true
                document.getElementById("generate_design_knowledge_button").disabled = true
                document.getElementById("llm_response").disabled = true
            }, 1000);
        });
    }
}


