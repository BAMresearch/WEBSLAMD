import {assignClickEventToOtherForm, handleOtherSubmission, handleAddingOther} from "./other.js";
import {assignClickEventToSubmitButton, countSelectedOptions, scrollDown, updateProgress} from "./../utils.js";


function assignInputEventToLiquidForm() {
    const custom_liquid_name_field = document.querySelector(".liquid_option_name")
    custom_liquid_name_field.addEventListener("input", handleCustomLiquidNaming);
}

export function assignClickEventToLiquidForm() {
    const liquid_options = document.querySelectorAll(".liquid_option");
    liquid_options.forEach(function (liquid_option) {
        liquid_option.addEventListener("click", handleLiquidSelection);
    });
}

export function handleLiquidSelection(event) {
    const submit_liquid_button = document.getElementById("submit_liquid_button");
    const selected_liquid_options = document.querySelectorAll(".liquid_option")
    const count = countSelectedOptions(selected_liquid_options)
    if (count == 0){
        submit_liquid_button.disabled = true;
    } else {
        if (event.target.classList.contains("custom_liquid_option")) {
            const custom_liquid_option_name = event.target.previousElementSibling;
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
}

export async function handleLiquidSubmission() {
    let selected_liquids = []
    const liquid_options = document.querySelectorAll(".liquid_option");
    liquid_options.forEach(function (liquid_option) {
        if (liquid_option.checked) {
            selected_liquids.push(liquid_option.value);
            liquid_option.previousElementSibling.disabled = true
        }
        liquid_option.disabled = true
    });
    document.getElementById("additional_liquid_button").disabled = true;
    document.getElementById("submit_liquid_button").disabled = true;
    insertSpinnerInPlaceholder("other_container", true, CHATBOT_RESPONSE_SPINNER);
    setTimeout(async function handleSubmission() {
        await postDataAndEmbedTemplateInPlaceholder(
            "/design_assistant/zero_shot/liquid",
            "other_container",
            selected_liquids
        );
        assignClickEventToSubmitButton("submit_other_button", handleOtherSubmission);
        assignClickEventToSubmitButton("additional_other_button", handleAddingOther);
        assignClickEventToOtherForm();
        updateProgress()
        scrollDown()
    }, 1000);
}

function handleCustomLiquidNaming(event) {
    const submit_liquid_button = document.getElementById("submit_liquid_button");
    const liquid_options = document.querySelectorAll('.liquid_option')
    const custom_liquid_option = event.target.nextElementSibling;
    const count = countSelectedOptions(liquid_options)
    custom_liquid_option.value = event.target.value;
    if (custom_liquid_option.checked) {
        if (event.target.value) {
            submit_liquid_button.disabled = false
        } else {
            submit_liquid_button.disabled = true
        }
    }
}

export function handleAddingLiquid() {
    const liquids_container = document.getElementById("liquids_option_container");
    const custom_liquid_container = document.createElement("div");
    const custom_liquid_option_input = document.createElement("input");
    const custom_liquid_name_input = document.createElement("input");
    custom_liquid_container.classList.add("d-flex", "gap-2", "justify-content-between")
    custom_liquid_option_input.type = "checkbox";
    custom_liquid_option_input.name = "custom_liquid_option";
    custom_liquid_option_input.classList.add("liquid_option", "custom_liquid_option");
    custom_liquid_name_input.classList.add("w-auto", "form-control")
    custom_liquid_name_input.placeholder = "Name of liquid";
    custom_liquid_name_input.classList.add("liquid_option_name");
    custom_liquid_name_input.name = 'custom_liquid_name'
    custom_liquid_container.appendChild(custom_liquid_name_input);
    custom_liquid_container.appendChild(custom_liquid_option_input);
    liquids_container.appendChild(custom_liquid_container);
    assignClickEventToLiquidForm();
    assignInputEventToLiquidForm();
    document.getElementById("additional_liquid_button").disabled = true
}