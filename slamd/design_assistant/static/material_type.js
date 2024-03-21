import { assignClickEventToSubmitButton } from "./utils.js";
import {assignClickEventToDesignTargetForm, handleAddingCustomDesignTarget, handleDesignTargetsSubmission,} from "./design_targets.js";


export function assignClickEventToMaterialTypeField() {
  const material_type_choices = document.querySelectorAll(".material_type_field_choice");
  material_type_choices.forEach((material_type_choice) =>
    material_type_choice.addEventListener("click", handleMaterialTypeSelection)
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
    assignClickEventToSubmitButton("design_targets_submit_button", handleDesignTargetsSubmission);
    assignClickEventToDesignTargetForm();
    assignClickEventToSubmitButton("additional_design_targets_button", handleAddingCustomDesignTarget);
  }, 1000);
  const material_type_choices = document.querySelectorAll(
    ".material_type_field_choice"
  );
  material_type_choices.forEach(function (other_choice) {
    if (other_choice !== this) {
      other_choice.disabled = true;
    }
  });
}