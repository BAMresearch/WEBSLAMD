async function handle_task_selection(event) {
  const task = event.target.value;
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/task",
    "import_selection_container",
    task
  );
  assignClickEventToImportForm();
  const task_options = document.querySelectorAll(".task_field_option");
  task_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}

async function handle_import_selection(event) {
  const import_selection = event.target.value;
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/import_selection",
    "material_type_container",
    import_selection
  );
  assignClickEventToMaterialTypeField();
  const import_options = document.querySelectorAll(".import_selection_option");
  import_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}

async function handle_material_type_selection(event) {
  const material_type_selection = event.target.value;
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/material_type",
    "design_targets_container",
    material_type_selection
  );
  const material_type_options = document.querySelectorAll(
    ".material_type_field_option"
  );
  console.log("test");
  material_type_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}

function assignClickEventToTaskForm() {
  const task_options = document.querySelectorAll(".task_field_option");
  task_options.forEach((task_option) =>
    task_option.addEventListener("click", handle_task_selection)
  );
}

function assignClickEventToImportForm() {
  const import_options = document.querySelectorAll(".import_selection_option");
  import_options.forEach((import_option) =>
    import_option.addEventListener("click", handle_import_selection)
  );
}

function assignClickEventToMaterialTypeField() {
  const material_type_options = document.querySelectorAll(
    ".material_type_field_option"
  );
  material_type_options.forEach((material_type_option) =>
    material_type_option.addEventListener(
      "click",
      handle_material_type_selection
    )
  );
}

window.addEventListener("load", function () {
  assignClickEventToTaskForm();
  assignClickEventToImportForm();
  assignClickEventToMaterialTypeField();
});
