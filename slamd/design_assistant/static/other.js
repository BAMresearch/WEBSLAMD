import {
  assignInputEventToCommentForm,
  handleCommentSubmission,
} from "./comment.js";
import { assignClickEventToSubmitButton } from "./utils.js";

export function assignClickEventToOtherForm() {
  const other_options = document.querySelectorAll(".other_option");
  other_options.forEach(function (other_option) {
    other_option.addEventListener("click", handleOtherSelection);
  });
}

export async function handleOtherSubmission() {
  const submit_other_button = document.getElementById("submit_other_button");
  submit_other_button.disabled = "true";
  const additional_other_button = document.getElementById(
    "additional_other_button"
  );
  additional_other_button.disabled = "true";
  const other_options = document.querySelectorAll(".other_option");
  let other;
  other_options.forEach(function (other_option) {
    if (other_option.checked) {
      other = other_option.value;
    }
    other_option.disabled = "true";
  });
  insertSpinnerInPlaceholder(
    "knowledge_container",
    true,
    CHATBOT_RESPONSE_SPINNER
  );
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
      "/design_assistant/other",
      "knowledge_container",
      other
    );
    assignInputEventToCommentForm();
    assignClickEventToSubmitButton(
      "submit_comment_button",
      handleCommentSubmission
    );
  }, 1000);
}

export function handleOtherSelection(event) {
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

export function handleAddingOther() {
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
