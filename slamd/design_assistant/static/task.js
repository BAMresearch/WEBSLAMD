const task_options = document.querySelectorAll(".task_field_option");

task_options.forEach((task_option) =>
  task_option.addEventListener("click", handle_task_selection)
);

async function handle_task_selection(event) {
  const task = event.target.value;
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/task",
    "import_selection_container",
    task
  );

  task_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}