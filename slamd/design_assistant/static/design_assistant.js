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
  assignClickEventToSubmitButton(
    "design_targets_submit_button",
    handle_design_targets_submission
  );
  assignClickEventToDesignTargetForm();
  const material_type_options = document.querySelectorAll(
    ".material_type_field_option"
  );
  material_type_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}

async function handle_design_targets_submission(event) {
  let design_targets = {};
  const design_target_options = document.querySelectorAll(
    ".design_target_option"
  );
  design_target_options.forEach(function (option) {
    if (option.checked) {
      const design_target_value = option
        .closest("div")
        .nextElementSibling.querySelector(".design_target_value");
      design_targets[design_target_value.name] = design_target_value.value;
    }
  });

  //   await postDataAndEmbedTemplateInPlaceholder(
  //     "/design_assistant/design_targets",
  //     "design_targets_container",
  //     design_targets
  //   );
  console.log(design_targets);
  const token = document.getElementById("csrf_token").value;
  await fetch("/design_assistant/design_targets", {
    method: "POST",
    headers: {
      "X-CSRF-TOKEN": token,
    },
    body: JSON.stringify(design_targets),
  });
}

function handle_design_targets_selection(event) {
  const design_target_value = event.target
    .closest("div")
    .nextElementSibling.querySelector(".design_target_value");
  if (design_target_value.disabled) {
    design_target_value.disabled = false;
    design_target_value.focus();
  } else {
    design_target_value.disabled = true;
    design_target_value.value = "";
  }
  const design_target_options = document.querySelectorAll(
    ".design_target_option"
  );
  const count = count_selected_options(design_target_options);
  design_target_options.forEach(function (design_target_option) {
    if (count >= 2 && !design_target_option.checked) {
      design_target_option.disabled = true;
    } else {
      design_target_option.disabled = false;
    }
  });
}

function count_selected_options(options) {
  let count = 0;
  options.forEach(function (option) {
    if (option.checked) {
      ++count;
    }
  });
  return count;
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

function assignClickEventToSubmitButton(button_id, handle_function) {
  const submit_button = document.getElementById(button_id);
  if (submit_button) {
    submit_button.addEventListener("click", handle_function);
  }
}

function assignClickEventToDesignTargetForm() {
  const design_target_options = document.querySelectorAll(
    ".design_target_option"
  );
  design_target_options.forEach(function (design_target_option) {
    design_target_option.addEventListener(
      "click",
      handle_design_targets_selection
    );
  });
}

async function handleDeleteDesignAssistantSession() {
  const token = document.getElementById("csrf_token").value;
  const response = await fetch("/design_assistant/delete_session", {
    method: "POST",
    headers: {
      "X-CSRF-TOKEN": token,
    },
  });
  if (response.ok) {
    window.location.reload();
  } else {
    const error = await response.text();
    document.write(error);
  }
}

window.addEventListener("load", function () {
  assignClickEventToSubmitButton(
    "delete_session_button",
    handleDeleteDesignAssistantSession
  );
  assignClickEventToTaskForm();
  assignClickEventToImportForm();
  assignClickEventToMaterialTypeField();
  assignClickEventToSubmitButton(
    "design_targets_submit_button",
    handle_design_targets_submission
  );
  assignClickEventToDesignTargetForm();
});