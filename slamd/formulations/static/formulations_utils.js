/**
 * Many functions look similar to the ones in blended_materials.js
 * Nevertheless, we choose not to extract common functions as the two usecases are in general not related and the
 * common functions would lead to tight coupling between these separated usecases.
 */
function assignKeyboardEventsToFormulationsMinMaxForm() {
    if (withConstraint) {
        addListenersToIndependentFields();
    } else {
        addListenersToAllFields();
    }
}

function addListenersToIndependentFields() {
    const inputFields = collectInputFields();
    for (let item of inputFields) {
        item.min.addEventListener("keyup", () => {
            computeDependentValue("min", item.min, inputFields);
            toggleConfirmFormulationsBlendingButton(inputFields);
        });
        item.max.addEventListener("keyup", () => {
            computeDependentValue("max", item.max, inputFields);
            toggleConfirmFormulationsBlendingButton(inputFields);
        });
        item.increment.addEventListener("keyup", () => {
            validateIncrementValue(item.increment)
            toggleConfirmFormulationsBlendingButton(inputFields);
        });
    }
}

function addListenersToAllFields() {
    const inputFields = collectInputFields(false);
    for (let item of inputFields) {
        item.min.addEventListener("keyup", () => {
            fixInputValue(item.min);
            toggleConfirmFormulationsBlendingButton(inputFields);
        });
        item.max.addEventListener("keyup", () => {
            fixInputValue(item.max);
            toggleConfirmFormulationsBlendingButton(inputFields);
        });
        item.increment.addEventListener("keyup", () => {
            fixInputValue(item.increment);
            toggleConfirmFormulationsBlendingButton(inputFields);
        });
    }
}

function toggleConfirmFormulationsBlendingButton(inputFields) {
    let allIncrementsFilled = inputFields.filter(item => item['increment'].value === "").length === 0;
    let allMinFilled = inputFields.filter(item => item['min'].value === "").length === 0;
    let allMaxFilled = inputFields.filter(item => item['max'].value === "").length === 0;
    document.getElementById("confirm_formulations_configuration_button").disabled = !(allIncrementsFilled && allMinFilled && allMaxFilled);
}

function assignKeyboardEventsToRatiosForm(initialCreationOfForm = false) {
    if (initialCreationOfForm) {
        allRatioFieldsHaveValidInput = true;
        document.getElementById("submit").disabled = nameIsEmpty;
    }

    toggleSubmitButtonBasedOnRatiosAndName();
}

/**
 * Similar to the logic defined in the corresponding method of blended_materials_utils.js. However, since it is possible
 * to define formulations without weigth constraints we internally take this possibility into account.
 */
function collectInputFields(only_independent = true) {
    let numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    if (!only_independent) {
        numberOfIndependentRows += 1;
    }

    let inputFields = []
    for (let i = 0; i < numberOfIndependentRows; i++) {
        let min = document.getElementById(`materials_min_max_entries-${i}-min`)
        let max = document.getElementById(`materials_min_max_entries-${i}-max`)
        let increment = document.getElementById(`materials_min_max_entries-${i}-increment`)
        inputFields.push({
            min: min,
            max: max,
            increment: increment
        })
    }
    return inputFields;
}

function collectFormulationsMinMaxValuesWithIncrements() {
    const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    let minMaxValuesWithIncrements = []
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        let min = document.getElementById(`materials_min_max_entries-${i}-min`)
        let max = document.getElementById(`materials_min_max_entries-${i}-max`)
        let increment = document.getElementById(`materials_min_max_entries-${i}-increment`)
        minMaxValuesWithIncrements.push({
            idx: i,
            min: parseFloat(min.value),
            max: parseFloat(max.value),
            increment: parseFloat(increment.value)
        })
    }
    return minMaxValuesWithIncrements;
}

function computeDependentValue(type, currentInputField, independentMinMaxInputFields) {
    let sumOfIndependentFields = autocorrectInput(independentMinMaxInputFields, type, currentInputField);

    const unfilledFields = independentMinMaxInputFields.filter(item => item[type].value === "");
    if (unfilledFields.length === 0) {
        const lastMinItem = document.getElementById(`materials_min_max_entries-${independentMinMaxInputFields.length}-${type}`);
        lastMinItem.value = (weigthConstraint - sumOfIndependentFields).toFixed(2)
    }
}

function autocorrectInput(independentMinMaxInputFields, type, currentInputField) {
    fixInputValue(currentInputField);

    let sumOfIndependentFields = independentMinMaxInputFields
        .filter(item => item[type].value !== "")
        .map(item => parseFloat(item[type].value))
        .reduce((x, y) => x + y, 0);

    if (sumOfIndependentFields > weigthConstraint) {
        currentInputField.value = (weigthConstraint - (sumOfIndependentFields - currentInputField.value)).toFixed(2)
        sumOfIndependentFields = weigthConstraint
    }
    return sumOfIndependentFields;
}

function validateIncrementValue(increment) {
    if (MORE_THAN_TWO_DECIMAL_PLACES.test(increment.value)) {
        increment.value = parseFloat(increment.value).toFixed(2);
    }

    if (increment.value > weigthConstraint) {
        increment.value = weigthConstraint;
    }
}
