import { assignClickEventToSubmitButton } from "./utils.js";
import {assignClickEventToPowdersForm, handlePowdersSubmission} from "./powder.js";

export function assignEventsToTargetValuesForm() {
        assignClickEventToSubmitButton("design_targets_values_submit_button", handleDesignTargetsValuesSubmission)
}

function handleDesignTargetsValuesSubmission(){
        const design_target_values_submission = []
        const design_target_values = document.querySelectorAll(".design_target_value");
        const design_target_optimizations = document.querySelectorAll('.design_target_optimization_select')
        const design_target_names = document.querySelectorAll(".design_target_name")
        for (let i = 0; i < design_target_values.length; i++) {
                let design_target_value;
                let design_target_optimization;
                if (design_target_values[i].value == ''){
                        design_target_value = 'No target value'
                        design_target_optimization = 'No optimization'
                }
                else {
                        design_target_value = design_target_values[i].value
                        design_target_optimization = design_target_optimizations[i].value
                }
                design_target_values_submission.push({
                        "design_target_name_field" : design_target_names[i].textContent,
                        "design_target_value_field": design_target_value,
                        "design_target_optimization_field": design_target_optimization
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
        for (let i = 0; i < design_target_values.length; i++) {
                design_target_values[i].disabled = true
                design_target_optimizations[i].disabled = true
        }
        document.getElementById("design_targets_values_submit_button").disabled = true

}


