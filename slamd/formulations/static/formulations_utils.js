/**
 * Many functions look similar to the ones in blended_materials.js
 * Nevertheless, we choose not to extract common functions as the two use cases are in general not related and the
 * common functions would lead to tight coupling between these separated use cases.
 */

const CONCRETE = "CONCRETE";
const BINDER = "BINDER";
const MAX_COMBINATIONS_THRESHOLD = 10000;

function collectBuildingMaterialFormulationSelection() {
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
            const typeAndUuid = option.value.split("|");
            const type = typeAndUuid[0];
            const uuid = typeAndUuid[1];
            return {
                uuid: uuid,
                type: type,
                name: option.innerHTML,
            };
        });
}

function addListenersToIndependentFields(context) {
    const independentInputFields = collectInputFields();
    for (const item of independentInputFields) {
        item.min.addEventListener("keyup", () => {
            // computeDependentValue("min", item.min, independentInputFields, context);
            toggleConfirmationFormulationsButtons(independentInputFields);
        });
        document.getElementById(item.min.id).setAttribute("title", "");

        item.max.addEventListener("keyup", () => {
            // computeDependentValue("max", item.max, independentInputFields, context);
            toggleConfirmationFormulationsButtons(independentInputFields);
        });
        document.getElementById(item.max.id).setAttribute("title", "");

        item.increment.addEventListener("keyup", () => {
            const constraint = context === CONCRETE ? concreteWeightConstraint : binderWeightConstraint
            // correctInputFieldValue(item.increment, 0, parseFloat(constraint));
            toggleConfirmationFormulationsButtons(independentInputFields);
        });
    }
}

function toggleConfirmationFormulationsButtons(inputFields) {
    const allIncrementsFilled = inputFields.filter(item => item.increment.value === "").length === 0;
    const allMinFilled = inputFields.filter(item => item.min.value === "").length === 0;
    const allMaxFilled = inputFields.filter(item => item.max.value === "").length === 0;
    document.getElementById("create_formulations_batch_button").disabled = !(
        allIncrementsFilled &&
        allMinFilled &&
        allMaxFilled
    );
}

/**
 * Similar to the logic defined in the corresponding method of blended_materials_utils.js. However, since it is possible
 * to define formulations without weight constraints we internally take this possibility into account.
 */
function collectInputFields(only_independent = true) {
    let numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 2;

    if (!only_independent) {
        numberOfIndependentRows += 1;
    }

    const inputFields = [];
    for (let i = 0; i < numberOfIndependentRows; i++) {
        const type = document.getElementById(`materials_min_max_entries-${i}-type_field`);
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

function collectFormulationsMinMaxRequestData(context) {
    const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    const rowData = [];
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        const uuid = document.getElementById(`materials_min_max_entries-${i}-uuid_field`);
        const type = document.getElementById(`materials_min_max_entries-${i}-type_field`);
        const min = document.getElementById(`materials_min_max_entries-${i}-min`);
        const max = document.getElementById(`materials_min_max_entries-${i}-max`);
        const increment = document.getElementById(`materials_min_max_entries-${i}-increment`);
        rowData.push({
            uuid: uuid.value,
            type: type.value,
            min: parseFloat(min.value),
            max: parseFloat(max.value),
            increment: parseFloat(increment.value),
        });
    }

    // Add air pore content entry if value exists, inserting it second to last (for WeightInputPreprocessor)
    const airPoreContent = document.getElementById('air_pore_content');
    if (airPoreContent && airPoreContent.value) {
        const airPoreValue = parseFloat(airPoreContent.value);
        const airPoreEntry = {
            uuid: 'Air-Pore-Content-1',
            type: 'Air Pore Content',
            min: airPoreValue,
            max: airPoreValue,
            increment: 0
        };
        rowData.splice(rowData.length - 1, 0, airPoreEntry);
    }

    const constraint = context === CONCRETE ? concreteWeightConstraint : binderWeightConstraint;
    return {
        materials_request_data: {
            min_max_data: rowData
        },
        constraint: constraint,
    };
}

// there are two elements for each process, one hidden and one visible. Therefore we divide by 2
function collectProcessesRequestData() {
    const numberProcessRows = document.querySelectorAll('[id^="process_entries-"]').length / 2;

    const rowData = [];
    for (let i = 0; i < numberProcessRows; i++) {
        const uuid = document.getElementById(`process_entries-${i}-uuid_field`).value;
        rowData.push({
            uuid: uuid,
        });
    }
    return {
        processes: rowData,
    };
}

function calculateUuidCombinationsCount(rowData) {
    let uuidCombinationsCount = 1;
    for (const row of rowData) {
        const uuidList = row.uuid ? row.uuid.split(',') : [];
        uuidCombinationsCount *= uuidList.length > 0 ? uuidList.length : 1;
    }
    return uuidCombinationsCount;
}

function calculateCombinationsCount(rowData) {
    let combinationsCount = 1;
    for (const row of rowData) {
        if (row.min != null && row.max != null && row.increment != null && !isNaN(row.min) && !isNaN(row.max) && !isNaN(row.increment) && row.increment > 0) {
            const range = (row.max - row.min) / row.increment + 1;
            combinationsCount *= range;
        }
    }
    return combinationsCount;
}
