/**
 * Many functions look similar to the ones in blended_materials.js
 * Nevertheless, we choose not to extract common functions as the two usecases are in general not related and the
 * common functions would lead to tight coupling between these separated usecases.
 */

function collectAllSelectedMaterials() {
    const powderPlaceholder = document.getElementById("powder_selection");
    const liquidPlaceholder = document.getElementById("liquid_selection");
    const aggregatesPlaceholder = document.getElementById("aggregates_selection");
    const admixturePlaceholder = document.getElementById("admixture_selection");
    const customPlaceholder = document.getElementById("custom_selection");

    const selectedMaterials = []
    selectedMaterials.push(...collectSelectionForFormulations(powderPlaceholder))
    selectedMaterials.push(...collectSelectionForFormulations(liquidPlaceholder))
    selectedMaterials.push(...collectSelectionForFormulations(aggregatesPlaceholder))
    selectedMaterials.push(...collectSelectionForFormulations(admixturePlaceholder))
    selectedMaterials.push(...collectSelectionForFormulations(customPlaceholder))
    return selectedMaterials;
}

function collectSelectionForFormulations(placeholder) {
    return Array.from(placeholder.children)
        .filter(option => option.selected)
        .filter(option => option.innerHTML !== "")
        .map(option => {
            let typeAndUuid = option.value.split('|');
            const type = typeAndUuid[0]
            const uuid = typeAndUuid[1]
            return {
                uuid: uuid,
                type: type,
                name: option.innerHTML
            }
        });
}

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
            toggleConfirmationFormulationsButtons(inputFields);
        });
        item.max.addEventListener("keyup", () => {
            computeDependentValue("max", item.max, inputFields);
            toggleConfirmationFormulationsButtons(inputFields);
        });
        item.increment.addEventListener("keyup", () => {
            validateIncrementValue(item.increment)
            toggleConfirmationFormulationsButtons(inputFields);
        });
    }
}

function addListenersToAllFields() {
    const inputFields = collectInputFields(false);
    for (let item of inputFields) {
        item.min.addEventListener("keyup", () => {
            fixInputValue(item.min);
            toggleConfirmationFormulationsButtons(inputFields);
        });
        item.max.addEventListener("keyup", () => {
            fixInputValue(item.max);
            toggleConfirmationFormulationsButtons(inputFields);
        });
        item.increment.addEventListener("keyup", () => {
            fixInputValue(item.increment);
            toggleConfirmationFormulationsButtons(inputFields);
        });
    }
}

function toggleConfirmationFormulationsButtons(inputFields) {
    let allIncrementsFilled = inputFields.filter(item => item['increment'].value === "").length === 0;
    let allMinFilled = inputFields.filter(item => item['min'].value === "").length === 0;
    let allMaxFilled = inputFields.filter(item => item['max'].value === "").length === 0;
    document.getElementById("confirm_formulations_configuration_button").disabled = !(allIncrementsFilled && allMinFilled && allMaxFilled);
    document.getElementById("submit").disabled = !(allIncrementsFilled && allMinFilled && allMaxFilled);
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

function collectFormulationsMinMaxRequestData() {
    const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    let rowData = []
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        let uuid = document.getElementById(`materials_min_max_entries-${i}-uuid_field`)
        let type = document.getElementById(`materials_min_max_entries-${i}-type_field`)
        let min = document.getElementById(`materials_min_max_entries-${i}-min`)
        let max = document.getElementById(`materials_min_max_entries-${i}-max`)
        let increment = document.getElementById(`materials_min_max_entries-${i}-increment`)
        rowData.push({
            uuid: uuid.value,
            type: type.value,
            min: parseFloat(min.value),
            max: parseFloat(max.value),
            increment: parseFloat(increment.value)
        })
    }
    return {
        materials_formulation_configuration: rowData,
        weight_constraint: weigthConstraint
    }
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

    if (parseFloat(increment.value) < 0) {
        increment.value = 0;
    }

    if (parseFloat(increment.value) > parseFloat(weigthConstraint)) {
        increment.value = weigthConstraint;
    }
}

function prepareMaterialsMinMaxInputFieldsFromSelection(selectedMaterials) {
    for (let i = 0; i < selectedMaterials.length; i++) {
        document.getElementById(`materials_min_max_entries-${i}-uuid_field`).value = selectedMaterials[i].uuid;
        document.getElementById(`materials_min_max_entries-${i}-type_field`).value = selectedMaterials[i].type;
        document.getElementById(`materials_min_max_entries-${i}-materials_entry_name`).value = selectedMaterials[i].name;
        if (withConstraint) {
            if (i === selectedMaterials.length - 1) {
                document.getElementById(`materials_min_max_entries-${i}-increment`).disabled = true;
                document.getElementById(`materials_min_max_entries-${i}-max`).disabled = true;
                document.getElementById(`materials_min_max_entries-${i}-min`).disabled = true;
            }
        }
    }
    if (selectedMaterials.length === 1) {
        document.getElementById("materials_min_max_entries-0-min").value = weigthConstraint
        document.getElementById("materials_min_max_entries-0-max").value = weigthConstraint
        if (withConstraint) {
            document.getElementById("confirm_formulations_configuration_button").disabled = false
        }
    }
}

function prepareProcessMinMaxInputFieldsFromSelection(selectedProcesses) {
    for (let i = 0; i < selectedProcesses.length; i++) {
        document.getElementById(`processes_entries-${i}-uuid_field`).value = selectedProcesses[i].uuid;
        document.getElementById(`processes_entries-${i}-process_name`).value = selectedProcesses[i].name;
    }
}
