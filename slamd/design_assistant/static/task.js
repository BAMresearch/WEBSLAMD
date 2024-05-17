export function assignClickEventToTaskForm() {
    const task_choices = document.querySelectorAll(".task_field_choice");
    task_choices.forEach((task_choice) =>
        task_choice.addEventListener("click", handleTaskSelection)
    );
}
export async function handleTaskSelection(event) {
    const task = event.target.value;
    insertSpinnerInPlaceholder(
        "material_type_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/task",
            "material_type_container",
            task
        );
        window.location.reload();
    }, 1000);

    const task_choices = document.querySelectorAll(".task_field_choice");
    task_choices.forEach(function (other_choice) {
        if (other_choice !== this) {
            other_choice.disabled = true;
        }
    });
}