import {countSelectedOptions, scrollDown, updateProgress} from "./../utils.js";
import { assignEventsToTargetValuesForm} from "./design_targets_values.js";


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
      ".custom_design_target_option_name"
  );
  design_target_options.forEach(function (design_target_option) {
    design_target_option.addEventListener(
        "input",
        handleCustomDesignTargetNaming
    );
  });
}

function handleCustomDesignTargetNaming(event) {
  const custom_design_target_option = event.target.closest("input").nextElementSibling;
  custom_design_target_option.value = event.target.value
  const design_target_options = document.querySelectorAll(".design_target_option")
  let count = countSelectedOptions(design_target_options);
  if (event.target.value){
    if (count < 2){
      custom_design_target_option.disabled = false
    }
  }
  else {
    custom_design_target_option.checked = false
    count = countSelectedOptions(design_target_options);
    if (count < 1){
      document.getElementById("design_targets_submit_button").disabled = true
    }
    if (count < 2){
      design_target_options.forEach(function (design_target_option){
        if (design_target_option.disabled){
          if (!design_target_option.classList.contains('custom_design_target_option'))
            design_target_option.disabled = false
          else {
            const other_custom_design_target_option_name = design_target_option.nextElementSibling
            if (other_custom_design_target_option_name.value){
              design_target_option.disabled = false
            }
          }
        }
      })
    }
    custom_design_target_option.disabled = true
  }
}

export async function handleDesignTargetsSubmission(event) {
  let design_targets = [];
  const design_target_options = document.querySelectorAll(".design_target_option");
  design_target_options.forEach(function (design_target_option) {
    if (design_target_option.checked) {
      design_targets.push({"design_target_name_field": design_target_option.value})
    }
    design_target_option.disabled = true;
  });
  const design_target_options_names = document.querySelectorAll(".custom_design_target_option_name");
  design_target_options_names.forEach(function (design_target_option_name) {
    design_target_option_name.disabled = true
  });
  document.getElementById("additional_design_targets_button").disabled = true;
  document.getElementById("design_targets_submit_button").disabled = true;
  insertSpinnerInPlaceholder(
    "design_targets_values_container",
    true,
    CHATBOT_RESPONSE_SPINNER
  );
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
      "/design_assistant/zero_shot/design_targets",
      "design_targets_values_container",
      design_targets
    );
    assignEventsToTargetValuesForm()
    updateProgress()
    scrollDown()
  }, 1000);
}

export function handleDesignTargetsSelection(event) {
  const design_target_options = document.querySelectorAll(".design_target_option");
  const count = countSelectedOptions(design_target_options);
  const submit_button = document.getElementById("design_targets_submit_button");
  design_target_options.forEach(function (design_target_option) {
    if (count >= 2 && !design_target_option.checked) {
      design_target_option.disabled = true;
    } else {
      if (!design_target_option.classList.contains('custom_design_target_option')){
        design_target_option.disabled = false;
      }
      if (design_target_option.classList.contains('custom_design_target_option')) {
        const custom_design_target_option_input = design_target_option.previousElementSibling
        if (custom_design_target_option_input.value) {
          design_target_option.disabled = false;
        }
      }
    }
  });
  if (count >= 1) {
    submit_button.disabled = false;
  } else {
    submit_button.disabled = true;
  }
}

export function handleAddingCustomDesignTarget() {
  // select html container for all design targets
  const container = document.getElementById("design_target_options_container");
  // create html container for design target option and add bootstrap classes
  const design_target_option_container = document.createElement("div");
  design_target_option_container.classList.add("design_target_option_container", "d-flex", "justify-content-between", "additional_design_target_input");
  // create html inner container for design target option and add bootstrap classes
  const design_target_option_inner_container = document.createElement("div");
  design_target_option_inner_container.classList.add("d-flex", "gap-2")
  // create html input element for design target option
  const design_target_option_checkbox_input = document.createElement("input");
  design_target_option_checkbox_input.classList.add("design_target_option", "custom_design_target_option");
  design_target_option_checkbox_input.type = "checkbox";
  design_target_option_checkbox_input.disabled = true
  design_target_option_checkbox_input.value = "additional design target checkbox";
  design_target_option_checkbox_input.name = "custom_design_target_option"
  // create html input element for name of design target
  const design_target_option_name_input = document.createElement("input");
  design_target_option_name_input.classList.add("custom_design_target_option_name")
  design_target_option_name_input.classList.add("form-control")
  design_target_option_name_input.placeholder = "Required: Name target";
  design_target_option_name_input.name = "custom_design_target_option"
  // add all html elements sequentially to container that wraps all design targets
  design_target_option_inner_container.appendChild(design_target_option_name_input);
  design_target_option_inner_container.appendChild(design_target_option_checkbox_input);
  design_target_option_container.appendChild(design_target_option_inner_container);
  container.appendChild(design_target_option_container);
  // assign events to newly created html elements
  assignInputEventToDesignTargetForm();
  assignClickEventToDesignTargetForm();
}