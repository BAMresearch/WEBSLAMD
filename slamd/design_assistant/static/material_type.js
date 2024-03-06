import { assignClickEventToSubmitButton } from "./utils.js";
import {
  assignClickEventToDesignTargetForm,
  handleAddingDesignTargets,
  handleDesignTargetsSubmission,
} from "./target.js";

export function assignClickEventToMaterialTypeField() {
  const material_type_options = document.querySelectorAll(
    ".material_type_field_option"
  );
  material_type_options.forEach((material_type_option) =>
    material_type_option.addEventListener("click", handleMaterialTypeSelection)
  );
}

async function handleMaterialTypeSelection(event) {
  const material_type_selection = event.target.value;
  insertSpinnerInPlaceholder(
    "design_targets_container",
    true,
    CHATBOT_RESPONSE_SPINNER
  );
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
      "/design_assistant/zero_shot/material_type",
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
  }, 1000);
  const material_type_options = document.querySelectorAll(
    ".material_type_field_option"
  );
  material_type_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}
