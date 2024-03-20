import { assignClickEventToSubmitButton } from "./utils.js";
import {assignClickEventToPowdersForm, handlePowdersSubmission} from "./powder.js";

export function assignEventsToTargetValuesForm() {
        assignClickEventToSubmitButton("design_targets_values_submit_button", handleDesignTargetsValuesSubmission)
}

function handleDesignTargetsValuesSubmission(){
        const design_target_values_submission = []
        const design_target_values = document.querySelectorAll(".design_target_value");
        const design_target_units = document.querySelectorAll(".design_target_unit")
        const design_target_bound = document.querySelectorAll('.design_target_bound_select')
        const design_target_names = document.querySelectorAll(".design_target_name")
        for (let i = 0; i < design_target_values.length; i++) {
                design_target_values_submission.push({
                        "design_target_name_field" : design_target_names[i].textContent.toLowerCase(),
                        "design_target_value_field": Number(design_target_values[i].value),
                        "design_target_unit_field": design_target_units[i].value,
                        "design_target_bound_field": design_target_bound[i].value
                });
        }
        setTimeout(async function handleSubmission() {
                await postDataAndEmbedTemplateInPlaceholder(
                    "/design_assistant/zero_shot/design_targets_values",
                    "powders_container",
                    design_target_values_submission
                );
                assignClickEventToSubmitButton("powders_submit_button", handlePowdersSubmission);
                assignClickEventToPowdersForm();
        }, 1000)
        document.getElementById("design_targets_values_submit_button").disabled = true
}


