/**
 * Many functions look similar to the ones in blended_materials.js
 * Nevertheless, we choose not to extract common functions as the two usecases are in general not related and the
 * common functions would lead to tight coupling between these separated usecases.
 */

const TYPE_UUID_DELIMITER = "|";

function collectFormulationSelection() {
    const powderPlaceholder = document.getElementById("powder_selection");
    const liquidPlaceholder = document.getElementById("liquid_selection");
    const aggregatesPlaceholder = document.getElementById("aggregates_selection");
    const admixturePlaceholder = document.getElementById("admixture_selection");
    const customPlaceholder = document.getElementById("custom_selection");
    const processesPlaceholder = document.getElementById("process_selection");

    const selectedMaterials = [];
    selectedMaterials.push(...collectSelectionForFormulations(powderPlaceholder));
    selectedMaterials.push(...collectSelectionForFormulations(liquidPlaceholder));
    selectedMaterials.push(...collectSelectionForFormulations(aggregatesPlaceholder));
    selectedMaterials.push(...collectSelectionForFormulations(admixturePlaceholder));
    selectedMaterials.push(...collectSelectionForFormulations(customPlaceholder));
    selectedMaterials.push(...collectSelectionForFormulations(processesPlaceholder));
    return selectedMaterials;
}

function collectSelectionForFormulations(placeholder) {
    return Array.from(placeholder.children)
        .filter((option) => option.selected)
        .map((option) => {
            let typeAndUuid = option.value.split("|");
            const type = typeAndUuid[0];
            const uuid = typeAndUuid[1];
            return {
                uuid: uuid,
                type: type,
                name: option.innerHTML,
            };
        });
}

function addListenersToIndependentFields() {
    const independentInputFields = collectInputFields();
    for (let item of independentInputFields) {
        item.min.addEventListener("keyup", () => {
            computeDependentValue("min", item.min, independentInputFields);
            toggleConfirmationFormulationsButtons(independentInputFields);
        });
        item.max.addEventListener("keyup", () => {
            computeDependentValue("max", item.max, independentInputFields);
            toggleConfirmationFormulationsButtons(independentInputFields);
        });
        item.increment.addEventListener("keyup", () => {
            correctInputFieldValue(item.increment, parseFloat(weightConstraint));
            toggleConfirmationFormulationsButtons(independentInputFields);
        });
    }
}

function toggleConfirmationFormulationsButtons(inputFields) {
    let allIncrementsFilled = inputFields.filter((item) => item["increment"].value === "").length === 0;
    let allMinFilled = inputFields.filter((item) => item["min"].value === "").length === 0;
    let allMaxFilled = inputFields.filter((item) => item["max"].value === "").length === 0;
    document.getElementById("confirm_formulations_configuration_button").disabled = !(
        allIncrementsFilled &&
        allMinFilled &&
        allMaxFilled
    );
    document.getElementById("submit").disabled = !(allIncrementsFilled && allMinFilled && allMaxFilled);
}

/**
 * Similar to the logic defined in the corresponding method of blended_materials_utils.js. However, since it is possible
 * to define formulations without weight constraints we internally take this possibility into account.
 */
function collectInputFields(only_independent = true) {
    let numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    if (!only_independent) {
        numberOfIndependentRows += 1;
    }

    let inputFields = [];
    for (let i = 0; i < numberOfIndependentRows; i++) {
        let min = document.getElementById(`materials_min_max_entries-${i}-min`);
        let max = document.getElementById(`materials_min_max_entries-${i}-max`);
        let increment = document.getElementById(`materials_min_max_entries-${i}-increment`);
        inputFields.push({
            min: min,
            max: max,
            increment: increment,
        });
    }
    return inputFields;
}

function collectFormulationsMinMaxRequestData() {
    const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    let rowData = [];
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        let uuid = document.getElementById(`materials_min_max_entries-${i}-uuid_field`);
        let type = document.getElementById(`materials_min_max_entries-${i}-type_field`);
        let min = document.getElementById(`materials_min_max_entries-${i}-min`);
        let max = document.getElementById(`materials_min_max_entries-${i}-max`);
        let increment = document.getElementById(`materials_min_max_entries-${i}-increment`);
        rowData.push({
            uuid: uuid.value,
            type: type.value,
            min: parseFloat(min.value),
            max: parseFloat(max.value),
            increment: parseFloat(increment.value),
        });
    }
    return {
        materials_formulation_configuration: rowData,
        weight_constraint: weightConstraint,
    };
}

// there are two elements for each process, one hidden and one visible. Therefore we divide by 2
function collectProcessesRequestData() {
    const numberOfIndependentRows = document.querySelectorAll('[id^="processes_entries-"]').length / 2 - 1;

    let rowData = [];
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        const typeWithUUID = document.getElementById(`processes_entries-${i}-uuid_field`).value;
        const uuid = typeWithUUID.split(TYPE_UUID_DELIMITER)[1];
        rowData.push({
            uuid: uuid,
        });
    }
    return {
        processes: rowData,
    };
}

function computeDependentValue(inputFieldName, currentInputField, independentMinMaxInputFields) {
    let sumOfIndependentFields = autocorrectInput(independentMinMaxInputFields, inputFieldName, currentInputField);

    const unfilledFields = independentMinMaxInputFields.filter((item) => item[inputFieldName].value === "");
    if (unfilledFields.length === 0) {
        const lastMinItem = document.getElementById(
            `materials_min_max_entries-${independentMinMaxInputFields.length}-${inputFieldName}`
        );
        lastMinItem.value = (weightConstraint - sumOfIndependentFields).toFixed(2);
    }
}

function autocorrectInput(independentMinMaxInputFields, inputFieldName, currentInputField) {
    correctInputFieldValue(currentInputField);

    let sumOfIndependentFields = independentMinMaxInputFields
        .filter((item) => item[inputFieldName].value !== "")
        .map((item) => findWeightOfMaterial(item, inputFieldName))
        .reduce((x, y) => x + y, 0);

    if (sumOfIndependentFields > weightConstraint) {
        currentInputField.value = (weightConstraint - (sumOfIndependentFields - currentInputField.value)).toFixed(2);
        sumOfIndependentFields = weightConstraint;
    }
    return sumOfIndependentFields;
}

function findWeightOfMaterial(item, inputFieldName) {
    return parseFloat(item[inputFieldName].value);
}
