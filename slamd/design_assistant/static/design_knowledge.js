export function assignEventsToDesignKnowledge() {
    assignClickEventToGenerateDesignKnowledgeButton()
    assignClickEventToEditButton()
    assignClickEventToSaveButton()
    assignClickEventToContinueButton()
}



export function assignClickEventToGenerateDesignKnowledgeButton(){
    const generate_design_knowledge_button = document.getElementById("generate_design_knowledge_button")
    generate_design_knowledge_button.addEventListener('click', async function () {
        insertSpinnerInPlaceholder(
            "llm_response",
            false,
            CHATBOT_RESPONSE_SPINNER
        );
        setTimeout(async function handleSubmission() {
            await fetchDataAndEmbedTemplateInPlaceholder('/design_assistant/zero_shot/generate_design_knowledge', 'llm_response')
            // document.getElementById("llm_response_container").classList.remove('d-none')
        }, 1000);

        const edit_design_knowledge_button = document.getElementById("edit_design_knowledge_button")
        edit_design_knowledge_button.classList.remove('d-none')
        document.getElementById("continue_design_knowledge_button").disabled = false
    })
}

export function assignClickEventToEditButton(){
    const edit_design_knowledge_button = document.getElementById("edit_design_knowledge_button")
    edit_design_knowledge_button.addEventListener('click', function () {
        document.getElementById("generate_design_knowledge_button").disabled = true
        document.getElementById("continue_design_knowledge_button").disabled = true
        document.getElementById("llm_response").classList.add('d-none')
        document.getElementById("llm_response_editable").value = document.getElementById("llm_response").innerHTML
        document.getElementById("llm_response_editable").classList.remove('d-none')
        document.getElementById("edit_design_knowledge_button").classList.add('d-none')
        document.getElementById("save_design_knowledge_button").classList.remove('d-none')

    });
}

export function assignClickEventToSaveButton(){
    const save_design_knowledge_button = document.getElementById("save_design_knowledge_button")
    save_design_knowledge_button.addEventListener('click', function () {
        document.getElementById("llm_response").innerHTML = document.getElementById("llm_response_editable").value
        document.getElementById("llm_response_editable").classList.add('d-none')
        document.getElementById("llm_response").classList.remove('d-none')
        document.getElementById("edit_design_knowledge_button").classList.remove('d-none')
        document.getElementById("save_design_knowledge_button").classList.add('d-none')
        document.getElementById("continue_design_knowledge_button").disabled = false
        document.getElementById("generate_design_knowledge_button").disabled = false
    });
}

export function assignClickEventToContinueButton(){
    const continue_design_knowledge_button = document.getElementById("continue_design_knowledge_button")
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
        }, 1000);
    });
}


