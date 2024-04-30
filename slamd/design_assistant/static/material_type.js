import {assignClickEventToSubmitButton, scrollDown, updateProgress} from "./utils.js";
import {assignClickEventToDesignTargetForm, handleAddingCustomDesignTarget, handleDesignTargetsSubmission,} from "./zero_shot_learner/design_targets.js";
import { assignEventsToNamePowderStep } from "./data_creation/powder_name.js";


export function assignClickEventToMaterialTypeField() {
  const material_type_choices = document.querySelectorAll(".material_type_field_choice");
  material_type_choices.forEach((material_type_choice) =>
    material_type_choice.addEventListener("click", handleMaterialTypeSelection)
  );
}

function getSelectedTask(){
  let selected_task = ''
  const task_choices = document.querySelectorAll('.task_field_choice')
  task_choices.forEach((task_choice) => {
      if (task_choice.checked) {
        selected_task = task_choice.value
      }
  })
  return selected_task
}

async function handleMaterialTypeSelection(event) {
  let next_step_container_id = ''
  const material_type_selection = event.target.value;
  let selected_task = getSelectedTask()
  if (selected_task === 'data_creation'){
    next_step_container_id = 'powder_name_container'
  } else {
    next_step_container_id = "design_targets_container"
  }
  insertSpinnerInPlaceholder(
    next_step_container_id,
    true,
    CHATBOT_RESPONSE_SPINNER
  );
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
      "/design_assistant/zero_shot/material_type",
      next_step_container_id, 
      material_type_selection
    );
    assignClickEventToSubmitButton("design_targets_submit_button", handleDesignTargetsSubmission);
    assignClickEventToDesignTargetForm();
    assignClickEventToSubmitButton("additional_design_targets_button", handleAddingCustomDesignTarget);
    assignEventsToNamePowderStep()
    updateProgress()
    scrollDown()
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