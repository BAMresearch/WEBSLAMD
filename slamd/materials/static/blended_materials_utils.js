function collectBaseMaterialSelection(placeholder) {
    count = 0
    selectedMaterials = []
    if (placeholder.childElementCount !== 0) {
        let options = placeholder.children;
        for (let i = 0; i < options.length; i++) {
            if (options[i].selected) {
                count++
                selectedMaterials.push({
                    uuid: options[i].value,
                    name: options[i].innerHTML
                })
            }
        }
    }
    return {count, selectedMaterials};
}

function countSelectedBaseMaterials(placeholder) {
    count = 0
    if (placeholder.childElementCount !== 0) {
        let options = placeholder.children;
        for (let i = 0; i < options.length; i++) {
            if (options[i].selected) {
                count++
            }
        }
    }
    return count;
}

function resetConfiguration() {
    let minMaxPlaceholder = document.getElementById("min-max-placeholder");
    let ratioPlaceholder = document.getElementById("blending_ratio_placeholder");
    minMaxPlaceholder.innerHTML = "";
    ratioPlaceholder.innerHTML = "";
}

function prepareMinMaxInputFieldsFromSelection(selectedMaterials) {
    for (let i = 0; i < selectedMaterials.length; i++) {
        document.getElementById(`all_min_max_entries-${i}-uuid_field`).value = selectedMaterials[i].uuid;
        document.getElementById(`all_min_max_entries-${i}-blended_material_name`).value = selectedMaterials[i].name;
        if (i === selectedMaterials.length - 1) {
            document.getElementById(`all_min_max_entries-${i}-increment`).disabled = true;
            document.getElementById(`all_min_max_entries-${i}-max`).disabled = true;
            document.getElementById(`all_min_max_entries-${i}-min`).disabled = true;
        }
    }
}

function toggleConfirmBlendingButton(independentInputFields) {
    let allIncrementsFilled = independentInputFields.filter(item => item['increment'].value === "").length === 0;
    let allMinFilled = independentInputFields.filter(item => item['min'].value === "").length === 0;
    let allMaxFilled = independentInputFields.filter(item => item['max'].value === "").length === 0;
    document.getElementById("confirm_blending_configuration_button").disabled = !(allIncrementsFilled && allMinFilled && allMaxFilled);
}

function assignKeyboardEventsToRatiosForm() {
    let ratioInputFields = collectRatioFields();

    let numberOfIndependentBaseMaterials = document.querySelectorAll('[id$="-min"]').length - 1;
    for (let ratioInput of ratioInputFields) {
        ratioInput.addEventListener("keyup", () => {

            let regex = new RegExp("\^\\d+(/\\d+){" + numberOfIndependentBaseMaterials + "}$");
            let nonMatchingInputs = ratioInputFields
                .map(input => input.value)
                .filter(value => !regex.test(value))
                .length

            document.getElementById("submit").disabled = nonMatchingInputs > 0;
        })
    }
}

function collectRatioFields() {
    const numberOfRatioFields = document.querySelectorAll('[id$="-ratio"]').length;

    let ratioInputFields = []
    for (let i = 0; i < numberOfRatioFields; i++) {
        let ratio = document.getElementById(`all_ratio_entries-${i}-ratio`)
        ratioInputFields.push(ratio)
    }
    return ratioInputFields;
}

function assignKeyboardEventsToMinMaxForm() {
    let {numberOfIndependentRows, independentInputFields} = collectIndependentInputFields();

    for (let item of independentInputFields) {
        item.min.addEventListener("keyup", () => {
            computeDependentValue("min", item.min, independentInputFields, numberOfIndependentRows);
            toggleConfirmBlendingButton(independentInputFields);
        });
        item.max.addEventListener("keyup", () => {
            computeDependentValue("max", item.max, independentInputFields, numberOfIndependentRows);
            toggleConfirmBlendingButton(independentInputFields);
        });
        item.increment.addEventListener("keyup", () => {
            validateIncrementValue(item.increment)
            toggleConfirmBlendingButton(independentInputFields);
        });
    }
}

/**
 * The method extracts all min, max and increment input fields except the last one as the latter will be computed dynamically in terms
 * of all the other min/max values. The number of min items always equals the number of min items. Therefore we can get the
 * total number of rows simply by extracting the tags with id ending on -min.
 */
function collectIndependentInputFields() {
    const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    let independentInputFields = []
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        if (i !== numberOfIndependentRows) {
            let min = document.getElementById(`all_min_max_entries-${i}-min`)
            let max = document.getElementById(`all_min_max_entries-${i}-max`)
            let increment = document.getElementById(`all_min_max_entries-${i}-increment`)
            independentInputFields.push({
                min: min,
                max: max,
                increment: increment
            })
        }
    }
    return {numberOfIndependentRows, independentInputFields};
}

function createMinMaxValuesWithIncrements() {
    const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    let minMaxValuesWithIncrements = []
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        let min = document.getElementById(`all_min_max_entries-${i}-min`)
        let max = document.getElementById(`all_min_max_entries-${i}-max`)
        let increment = document.getElementById(`all_min_max_entries-${i}-increment`)
        minMaxValuesWithIncrements.push({
            idx: i,
            min: parseFloat(min.value),
            max: parseFloat(max.value),
            increment: parseFloat(increment.value)
        })
    }
    return minMaxValuesWithIncrements;
}

function computeDependentValue(type, currentInputField, independentMinMaxInputFields, numberOfIndependentRows) {
    const unfilledMinFields = independentMinMaxInputFields.filter(item => item[type].value === "");

    const moreThanTwoDigitsDotSeperated = /^\d*\.\d{3,}$/;
    const moreThanTwoDigitsColonSeperated = /^\d*\\,\d{3,}$/;

    if (moreThanTwoDigitsDotSeperated.test(currentInputField.value) || moreThanTwoDigitsColonSeperated.test(currentInputField.value)) {
        currentInputField.value = parseFloat(currentInputField.value).toFixed(2);
    }

    if (currentInputField.value < 0) {
        currentInputField.value = 0;
    }

    let sum = independentMinMaxInputFields
        .filter(item => item[type].value !== "")
        .map(item => parseFloat(item[type].value))
        .reduce((x, y) => x + y, 0);

    if (sum > 100) {
        currentInputField.value = (100 - (sum - currentInputField.value)).toFixed(2)
        sum = 100
    }
    if (unfilledMinFields.length === 0) {
        const lastMinItem = document.getElementById(`all_min_max_entries-${numberOfIndependentRows}-${type}`);
        lastMinItem.value = (100 - sum).toFixed(2)
    }
}

function validateIncrementValue(increment) {
    const moreThanTwoDigitsDotSeperated = /^\d*\.\d{3,}$/;
    const moreThanTwoDigitsColonSeperated = /^\d*\\,\d{3,}$/;

    if (moreThanTwoDigitsDotSeperated.test(increment.value) || moreThanTwoDigitsColonSeperated.test(increment.value)) {
        increment.value = parseFloat(increment.value).toFixed(2);
    }

    if (increment.value < 0) {
        increment.value = 0;
    }
    if (increment.value > 100) {
        increment.value = 100;
    }
}

/**
 * After adding a new field we need to reassign the ratio events as new input fields must be registered
 */
function assignAddCustomBlendEvent() {
    const placeholder = document.getElementById("blending_ratio_placeholder");

    document.getElementById("add_custom_blend_button").addEventListener("click", () => {
        const numberOfRatioFields = document.querySelectorAll('[id$="-ratio"]').length;
        let div = document.createElement("div");
        div.className = "col-md-3"

        let input = document.createElement("input");
        input.id = `all_ratio_entries-${numberOfRatioFields}-ratio`;
        input.name = `all_ratio_entries-${numberOfRatioFields}-ratio`;
        input.type = "text";
        input.className = "form-control";
        div.appendChild(input);

        const button = document.getElementById("add_custom_blend_button");
        placeholder.insertBefore(div, button);

        document.getElementById("submit").disabled = true;
        assignKeyboardEventsToRatiosForm()
    })
}
