import { assignClickEventToImportForm } from "./import.js";

export function assignClickEventToTaskForm() {
  const task_options = document.querySelectorAll(".task_field_option");
  task_options.forEach((task_option) =>
    task_option.addEventListener("click", handleTaskSelection)
  );
}


export async function handleTaskSelection(event) {
  const task = event.target.value;
  insertSpinnerInPlaceholder(
    "import_selection_container",
    true,
    CHATBOT_RESPONSE_SPINNER
  );
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
      "/design_assistant/task",
      "import_selection_container",
      task
    );
    assignClickEventToImportForm();
  }, 1000);

  const task_options = document.querySelectorAll(".task_field_option");
  task_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}