async function handleTaskSelection(event) {
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

async function handleImportSelection(event) {
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

async function handleMaterialTypeSelection(event) {
  const material_type_selection = event.target.value;
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/material_type",
    "design_targets_container",
    material_type_selection
  );
  assignClickEventToSubmitButton(
    "design_targets_submit_button",
    handleDesignTargetsSubmission
  );
  assignClickEventToDesignTargetForm();
  assignClickEventToSubmitButton(
    "additional_design_targets_button",
    handleAddingDesignTargets
  );
  const material_type_options = document.querySelectorAll(
    ".material_type_field_option"
  );
  material_type_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}

async function handleDesignTargetsSubmission(event) {
  let design_targets = {};
  const design_target_options = document.querySelectorAll(
    ".design_target_option"
  );
  design_target_options.forEach(function (option) {
    if (option.checked) {
      const design_target_value = option
        .closest("div")
        .nextElementSibling.querySelector(".design_target_value");
      design_targets[option.value] = design_target_value.value;
      option.disabled = true;
    }
  });
  console.log(design_targets);
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/design_targets",
    "powders_container",
    design_targets
  );

  assignClickEventToSubmitButton(
    "powders_submit_button",
    handlePowdersSubmission
  );
  assignClickEventToPowdersForm();
  document.getElementById("additional_design_targets_button").disabled = true;
  document.getElementById("design_targets_submit_button").disabled = true;
}

function handleDesignTargetsSelection(event) {
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
  const count = countSelectedOptions(design_target_options);
  const submit_button = document.getElementById("design_targets_submit_button");
  design_target_options.forEach(function (design_target_option) {
    if (count >= 2 && !design_target_option.checked) {
      design_target_option.disabled = true;
    } else {
      design_target_option.disabled = false;
    }
  });
  if (count >= 1) {
    submit_button.disabled = false;
  } else {
    submit_button.disabled = true;
  }
}

async function handlePowdersSubmission() {
  const powders_submission = {};
  const selected_powders = [];
  const powders_options = document.querySelectorAll(".powder_option");
  powders_options.forEach(function (option) {
    if (option.checked) {
      console.log(option);
      selected_powders.push(option.value);
    }
    option.disabled = true;
  });
  powders_submission["selected_powders"] = selected_powders;
  const blend_powder_options = document.querySelectorAll(
    ".blend_powder_option"
  );
  blend_powder_options.forEach(function (option) {
    if (option.checked) {
      powders_submission["blend_powders"] = option.value;
    }
    option.disabled = true;
  });
  if (!powders_submission["blend_powders"]) {
    powders_submission["blend_powders"] = "no";
  }
  console.log(powders_submission);
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/powders",
    "liquids_container",
    powders_submission
  );
  const powders_submit_button = document.getElementById(
    "powders_submit_button"
  );
  powders_submit_button.disabled = true;
  assignClickEventToSubmitButton(
    "submit_liquid_button",
    handleLiquidSubmission
  );
  assignClickEventToSubmitButton(
    "additional_liquid_button",
    handleAddingLiquid
  );
  assignClickEventToLiquidForm();
}

async function handlePowdersSelection() {
  const powders_options = document.querySelectorAll(".powder_option");
  const count = countSelectedOptions(powders_options);
  const blend_powder_options = document.querySelectorAll(
    ".blend_powder_option"
  );
  blend_powder_options.forEach(function (blend_powder_option) {
    if (count >= 2) {
      blend_powder_option.disabled = false;
    } else {
      blend_powder_option.disabled = true;
    }
  });

  document.getElementById("powders_submit_button").disabled = false;
}

function countSelectedOptions(options) {
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
    task_option.addEventListener("click", handleTaskSelection)
  );
}

function assignClickEventToImportForm() {
  const import_options = document.querySelectorAll(".import_selection_option");
  import_options.forEach((import_option) =>
    import_option.addEventListener("click", handleImportSelection)
  );
}

function assignClickEventToMaterialTypeField() {
  const material_type_options = document.querySelectorAll(
    ".material_type_field_option"
  );
  material_type_options.forEach((material_type_option) =>
    material_type_option.addEventListener("click", handleMaterialTypeSelection)
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
      handleDesignTargetsSelection
    );
  });
}

function assignClickEventToPowdersForm() {
  const powder_options = document.querySelectorAll(".powder_option");
  powder_options.forEach(function (powder_option) {
    powder_option.addEventListener("click", handlePowdersSelection);
  });
}

function assignClickEventToLiquidForm() {
  const liquid_options = document.querySelectorAll(".liquid_option");
  liquid_options.forEach(function (liquid_option) {
    liquid_option.addEventListener("click", handleLiquidSelection);
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

function handleAddingDesignTargets() {
  console.log("working");

  const container = document.getElementById("design_target_options_container");

  const design_target_option_container = document.createElement("div");
  design_target_option_container.classList.add(
    "design_target_option_container",
    "d-flex",
    "justify-content-between",
    "additional_design_target_input"
  );

  const design_target_option_container_2 = document.createElement("div");

  const design_target_option_input_checkbox = document.createElement("input");
  design_target_option_input_checkbox.classList.add("design_target_option");
  design_target_option_input_checkbox.type = "checkbox";
  design_target_option_input_checkbox.value =
    "additional design target checkbox";
  const design_target_option_input = document.createElement("input");

  const design_target_value_container = document.createElement("div");
  const design_target_value_unit = document.createElement("input");
  const design_target_value_input = document.createElement("input");
  design_target_option_input.placeholder = "Name of the design target";
  design_target_value_input.placeholder = "Target value";
  design_target_value_input.type = "number";
  design_target_value_input.disabled = "true";
  design_target_value_input.step = "0.01";
  design_target_value_unit.placeholder = "Unit";

  design_target_value_input.classList.add("design_target_value");

  design_target_value_container.appendChild(design_target_value_unit);
  design_target_value_container.appendChild(design_target_value_input);

  design_target_option_container_2.appendChild(
    design_target_option_input_checkbox
  );
  design_target_option_container_2.appendChild(design_target_option_input);
  design_target_option_container.appendChild(design_target_option_container_2);
  design_target_option_container.appendChild(design_target_value_container);
  container.appendChild(design_target_option_container);

  design_target_option_input.addEventListener("input", function (event) {
    const design_target_option =
      event.target.closest("input").previousElementSibling;

    design_target_option.value = event.target.value.toLowerCase();
    console.log(design_target_option);
  });
  assignClickEventToDesignTargetForm();
  assignInputEventToLiquidForm();
}

async function handleLiquidSubmission() {
  const liquid_options = document.querySelectorAll(".liquid_option");
  let liquid;
  liquid_options.forEach(function (liquid_option) {
    if (liquid_option.checked) {
      liquid = liquid_option.value;
    }
  });
  console.log(liquid);
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/liquid",
    "other_container",
    liquid
  );
}

function handleLiquidSelection(event) {
  const submit_liquid_button = document.getElementById("submit_liquid_button");
  if (event.target.classList.contains("custom_liquid_option")) {
    const custom_liquid_option_name = event.target.nextElementSibling;
    if (custom_liquid_option_name.value) {
      submit_liquid_button.disabled = false;
    }
  } else {
    submit_liquid_button.disabled = false;
  }
}

function handleCustomLiquidNaming(event) {
  const submit_liquid_button = document.getElementById("submit_liquid_button");
  const custom_liquid_option = event.target.previousElementSibling;
  custom_liquid_option.value = event.target.value;
  if (event.target.value && custom_liquid_option.checked) {
    submit_liquid_button.disabled = false;
  } else {
    submit_liquid_button.disabled = true;
  }
}

function assignInputEventToLiquidForm() {
  const custom_liquid_name_fields = document.querySelectorAll(
    ".liquid_option_name"
  );
  custom_liquid_name_fields.forEach(function (custom_liquid_name_field) {
    custom_liquid_name_field.addEventListener(
      "input",
      handleCustomLiquidNaming
    );
  });
}

function handleAddingLiquid() {
  const liquids_container = document.getElementById("liquids_option_container");

  const liquid_container = document.createElement("div");
  const liquid_name_input = document.createElement("input");
  const liquid_option_input = document.createElement("input");
  liquid_option_input.type = "radio";
  liquid_option_input.name = "liquid_option";
  liquid_option_input.classList.add("liquid_option", "custom_liquid_option");
  liquid_name_input.placeholder = "Name of liquid";
  liquid_name_input.classList.add("liquid_option_name");

  liquid_container.appendChild(liquid_option_input);
  liquid_container.appendChild(liquid_name_input);
  liquids_container.appendChild(liquid_container);
  assignClickEventToLiquidForm();
  assignInputEventToLiquidForm();
}
///

function assignClickEventToOtherForm() {
  const other_options = document.querySelectorAll(".other_option");
  other_options.forEach(function (other_option) {
    other_option.addEventListener("click", handleOtherSelection);
  });
}

async function handleOtherSubmission() {
  const other_options = document.querySelectorAll(".other_option");
  let other;
  other_options.forEach(function (other_option) {
    if (other_option.checked) {
      other = other_option.value;
    }
  });
  console.log(other);
  await postDataAndEmbedTemplateInPlaceholder(
    "/design_assistant/other",
    "knowledge_container",
    other
  );
}

function handleOtherSelection(event) {
  const submit_other_button = document.getElementById("submit_other_button");
  if (event.target.classList.contains("custom_other_option")) {
    const custom_other_option_name = event.target.nextElementSibling;
    if (custom_other_option_name.value) {
      submit_other_button.disabled = false;
    }
  } else {
    submit_other_button.disabled = false;
  }
}

function handleCustomOtherNaming(event) {
  const submit_other_button = document.getElementById("submit_other_button");
  const custom_other_option = event.target.previousElementSibling;
  custom_other_option.value = event.target.value;
  if (event.target.value && custom_other_option.checked) {
    submit_other_button.disabled = false;
  } else {
    submit_other_button.disabled = true;
  }
}

function assignInputEventToOtherForm() {
  const custom_other_name_fields =
    document.querySelectorAll(".other_option_name");
  custom_other_name_fields.forEach(function (custom_other_name_field) {
    custom_other_name_field.addEventListener("input", handleCustomOtherNaming);
  });
}

function handleAddingOther() {
  const others_container = document.getElementById("other_option_container");

  const other_container = document.createElement("div");
  const other_name_input = document.createElement("input");
  const other_option_input = document.createElement("input");
  other_option_input.type = "radio";
  other_option_input.name = "other_option";
  other_option_input.classList.add("other_option", "custom_other_option");
  other_name_input.placeholder = "Name of other";
  other_name_input.classList.add("other_option_name");

  other_container.appendChild(other_option_input);
  other_container.appendChild(other_name_input);
  others_container.appendChild(other_container);
  assignClickEventToOtherForm();
  assignInputEventToOtherForm();
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
    handleDesignTargetsSubmission
  );
  assignClickEventToSubmitButton(
    "powders_submit_button",
    handlePowdersSubmission
  );
  assignClickEventToDesignTargetForm();
  assignClickEventToPowdersForm();
  assignClickEventToSubmitButton(
    "additional_design_targets_button",
    handleAddingDesignTargets
  );
  assignClickEventToSubmitButton(
    "submit_liquid_button",
    handleLiquidSubmission
  );
  assignClickEventToSubmitButton("addtional_liquid_button", handleAddingLiquid);
  assignClickEventToLiquidForm();
  assignClickEventToSubmitButton("submit_other_button", handleOtherSubmission);
  assignClickEventToSubmitButton("addtional_other_button", handleAddingOther);
  assignClickEventToOtherForm();
});
