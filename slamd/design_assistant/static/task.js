import {assignClickEventToMaterialTypeField} from "./material_type.js";

export function assignClickEventToTaskForm() {
    const task_options = document.querySelectorAll(".task_field_option");
    task_options.forEach((task_option) =>
        task_option.addEventListener("click", handleTaskSelection)
    );
}

// TODO: remove token logic and move it to knowledge creation and recipe proposal
export async function handleTaskSelection(event) {
    const task = event.target.value;
    const token = document.getElementById("token_form-token").value
    insertSpinnerInPlaceholder(
        "material_type_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/task",
            "material_type_container",
            {"task": task, "token": token}
        );
        assignClickEventToMaterialTypeField();
    }, 1000);

    const task_options = document.querySelectorAll(".task_field_option");
    task_options.forEach(function (other_option) {
        if (other_option !== this) {
            other_option.disabled = true;
        }
    });
}