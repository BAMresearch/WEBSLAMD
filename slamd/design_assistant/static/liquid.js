import {
  assignClickEventToOtherForm,
  handleOtherSubmission,
  handleAddingOther,
} from "./other.js";
import { assignClickEventToSubmitButton, countSelectedOptions } from "./utils.js";

function assignInputEventToLiquidForm() {
  const custom_liquid_name_field = document.querySelector(".liquid_option_name")
  custom_liquid_name_field.addEventListener("input",handleCustomLiquidNaming);
}

export function assignClickEventToLiquidForm() {
  const liquid_options = document.querySelectorAll(".liquid_option");
  liquid_options.forEach(function (liquid_option) {
    liquid_option.addEventListener("click", handleLiquidSelection);
  });
}

export function handleLiquidSelection(event) {
  const submit_liquid_button = document.getElementById("submit_liquid_button");
  if (event.target.classList.contains("custom_liquid_option")) {
    const custom_liquid_option_name = event.target.nextElementSibling;
    if (custom_liquid_option_name.value) {
      submit_liquid_button.disabled = false;
    } else {
    submit_liquid_button.disabled = true;
    }
  }
  else {
    submit_liquid_button.disabled = false;
  }
}

export async function handleLiquidSubmission() {
  const submit_liquid_button = document.getElementById("submit_liquid_button");
  submit_liquid_button.disabled = "true";
  const additional_liquid_button = document.getElementById(
    "additional_liquid_button"
  );
  additional_liquid_button.disabled = "true";
  const liquid_options = document.querySelectorAll(".liquid_option");
  let liquid;
  liquid_options.forEach(function (liquid_option) {
    if (liquid_option.checked) {
      liquid = liquid_option.value;
    }
    liquid_option.disabled = "true";
  });
  insertSpinnerInPlaceholder("other_container", true, CHATBOT_RESPONSE_SPINNER);
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
      "/design_assistant/zero_shot/liquid",
      "other_container",
      liquid
    );
    assignClickEventToSubmitButton(
      "submit_other_button",
      handleOtherSubmission
    );
    assignClickEventToSubmitButton(
      "additional_other_button",
      handleAddingOther
    );
    assignClickEventToOtherForm();
  }, 1000);
}

function handleCustomLiquidNaming(event) {
  const submit_liquid_button = document.getElementById("submit_liquid_button");
  const liquid_options = document.querySelectorAll('.liquid_option')
  const custom_liquid_option = event.target.previousElementSibling;
  const count = countSelectedOptions(liquid_options)
  custom_liquid_option.value = event.target.value;
  console.log(custom_liquid_option.checked)
  if (custom_liquid_option.checked) {
    if (event.target.value){
      submit_liquid_button.disabled = false
    }
    else {
      submit_liquid_button.disabled = true
    }
  }
}

export function handleAddingLiquid() {

    const liquids_container = document.getElementById("liquids_option_container");
    const liquid_container = document.createElement("div");
    const liquid_option_input = document.createElement("input");
    const liquid_name_input = document.createElement("input");
    liquid_container.classList.add("d-flex", "gap-2")
    liquid_option_input.type = "radio";
    liquid_option_input.name = "liquid_option";
    liquid_option_input.classList.add("liquid_option", "custom_liquid_option");
    liquid_name_input.classList.add("form-control", "w-25")
    liquid_name_input.placeholder = "Name of liquid";
    liquid_name_input.classList.add("liquid_option_name");
    liquid_container.appendChild(liquid_option_input);
    liquid_container.appendChild(liquid_name_input);
    liquids_container.appendChild(liquid_container);
    assignClickEventToLiquidForm();
    assignInputEventToLiquidForm();
    document.getElementById("additional_liquid_button").disabled = true
}
