import {assignClickEventToSubmitButton, countSelectedOptions, scrollDown, updateProgress} from "./../utils.js";
import { assignClickEventToPowdersForm, handlePowdersSubmission } from "./powder.js";


export function assignClickEventToDesignTargetForm() {
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

function assignInputEventToDesignTargetForm() {
  const design_target_options = document.querySelectorAll(
      ".design_target_option"
  );
  design_target_options.forEach(function (design_target_option) {
    design_target_option.addEventListener(
        "input",
        handleDesignTargetsSelection
    );
  });
}

export async function handleDesignTargetsSubmission(event) {
  let design_targets = {};
  const design_target_options = document.querySelectorAll(".design_target_option");
  design_target_options.forEach(function (option) {
    if (option.checked) {
      const design_target_value = option
        .closest("div")
        .nextElementSibling.querySelector(".design_target_value");
      design_targets[option.value] = design_target_value.value;
    }
    option.disabled = true;
  });
  document.getElementById("additional_design_targets_button").disabled = true;
  document.getElementById("design_targets_submit_button").disabled = true;
  insertSpinnerInPlaceholder(
    "powders_container",
    true,
    CHATBOT_RESPONSE_SPINNER
  );
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
      "/design_assistant/zero_shot/design_targets",
      "powders_container",
      design_targets
    );
    assignClickEventToSubmitButton("powders_submit_button", handlePowdersSubmission);
    assignClickEventToPowdersForm();
    updateProgress()
    scrollDown()
  }, 1000);
}

export function handleDesignTargetsSelection(event) {
  const design_target_value = event.target.closest("div").nextElementSibling.querySelector(".design_target_value");
  if (design_target_value.disabled) {
    design_target_value.disabled = false;
    design_target_value.focus();
  } else {
    design_target_value.disabled = true;
    design_target_value.value = "";
  }
  const design_target_options = document.querySelectorAll(".design_target_option");
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

export function handleAddingDesignTargets() {
  const container = document.getElementById("design_target_options_container");
  const design_target_option_container = document.createElement("div");
  const design_target_option_inner_container = document.createElement("div");
  const design_target_option_input_checkbox = document.createElement("input");
  const design_target_option_input = document.createElement("input");
  const design_target_value_container = document.createElement("div");
  const design_target_value_unit = document.createElement("input");
  const design_target_value_input = document.createElement("input");
  design_target_option_container.classList.add("design_target_option_container", "d-flex", "justify-content-between", "additional_design_target_input");
  design_target_option_inner_container.classList.add("d-flex", "gap-2")
  design_target_option_input_checkbox.classList.add("design_target_option");
  design_target_option_input_checkbox.type = "checkbox";
  design_target_option_input_checkbox.disabled = true
  design_target_option_input_checkbox.value = "additional design target checkbox";
  design_target_option_input.classList.add("form-control")
  design_target_option_input.placeholder = "Name of the design target";
  design_target_value_input.placeholder = "Target value";
  design_target_value_input.type = "number";
  design_target_value_input.disabled = true;
  design_target_value_input.step = "0.01";
  design_target_value_unit.placeholder = "Unit";
  design_target_value_unit.classList.add("form-control")
  design_target_value_input.classList.add("design_target_value", "form-control");
  design_target_value_container.classList.add("d-flex", 'gap-2')
  design_target_value_container.appendChild(design_target_value_unit);
  design_target_value_container.appendChild(design_target_value_input);
  design_target_option_inner_container.appendChild(design_target_option_input_checkbox);
  design_target_option_inner_container.appendChild(design_target_option_input);
  design_target_option_container.appendChild(design_target_option_inner_container);
  design_target_option_container.appendChild(design_target_value_container);
  container.appendChild(design_target_option_container);
  design_target_option_input.addEventListener("input", function (event) {
    const design_target_option = event.target.closest("input").previousElementSibling;
    design_target_option.value = event.target.value.toLowerCase();
  });
  assignClickEventToDesignTargetForm();
}