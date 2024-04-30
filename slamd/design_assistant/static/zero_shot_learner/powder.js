import {assignClickEventToSubmitButton, scrollDown, updateProgress, countSelectedOptions} from "./../utils.js";
import {assignClickEventToLiquidForm, handleLiquidSubmission, handleAddingLiquid,} from "./liquid.js";


export function assignClickEventToPowdersForm() {
    const powder_options = document.querySelectorAll(".powder_option");
    powder_options.forEach(function (powder_option) {
        powder_option.addEventListener("click", handlePowdersSelection);
    });
    const blend_powder_options = document.querySelectorAll(".blend_powder_option");
    blend_powder_options.forEach(function (blend_powder_option) {
        blend_powder_option.addEventListener("click", handleBlendPowdersSelection);
    });
}

export async function handlePowdersSubmission() {
    const powders_submission = {};
    const selected_powders = [];
    const powders_options = document.querySelectorAll(".powder_option");
    powders_options.forEach(function (option) {
        if (option.checked) {
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
    document.getElementById("powders_submit_button").disabled = true;
    insertSpinnerInPlaceholder(
        "liquids_container",
        true,
        CHATBOT_RESPONSE_SPINNER
    );
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/zero_shot/powders",
            "liquids_container",
            powders_submission
        );
        assignClickEventToSubmitButton("submit_liquid_button", handleLiquidSubmission);
        assignClickEventToSubmitButton("additional_liquid_button", handleAddingLiquid);
        assignClickEventToLiquidForm();
        updateProgress()
        scrollDown()
    }, 1000);
}

function handlePowdersSelection() {
    const powders_options = document.querySelectorAll(".powder_option");
    const count = countSelectedOptions(powders_options);
    const blend_powder_options = document.querySelectorAll(".blend_powder_option");
    blend_powder_options.forEach(function (blend_powder_option) {
        if (count >= 2) {
            blend_powder_option.disabled = false;
            document.getElementById("powders_submit_button").disabled = true;
            document.querySelector('[id*="blend_powders_field-1"]').checked = false;
        } else if (count == 1) {
            document.getElementById("powders_submit_button").disabled = false;
            document.querySelector('[id*="blend_powders_field-1"]').checked = true;
            blend_powder_option.disabled = true;
        } else {
            blend_powder_option.disabled = true;
            document.getElementById("powders_submit_button").disabled = true;
        }
    });
    powders_options.forEach(function (powder_option) {
        if (!powder_option.checked){
            if (count == 2){
                powder_option.disabled = true
            } else if (count < 2){
                powder_option.disabled = false
            }
        } 
    })
}

function handleBlendPowdersSelection() {
    document.getElementById("powders_submit_button").disabled = false;
}
