/**
 * Many functions look similar to the ones in blended_materials.js
 * Nevertheless, we choose not to extract common functions as the two use cases are in general not related and the
 * common functions would lead to tight coupling between these separated use cases.
 */

let allWeightFieldsHaveValidInput = false;
const LIQUID_HTML_ID_INCLUDES = "-1-";

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

function addListenersToIndependentFields() {
  const independentInputFields = collectInputFields();
  for (const item of independentInputFields) {
    item.min.addEventListener("keyup", () => {
      computeDependentValue("min", item.min, independentInputFields);
      toggleConfirmationFormulationsButtons(independentInputFields);
    });
    document.getElementById(item.min.id).setAttribute("title", "");

    item.max.addEventListener("keyup", () => {
      computeDependentValue("max", item.max, independentInputFields);
      toggleConfirmationFormulationsButtons(independentInputFields);
    });
    document.getElementById(item.max.id).setAttribute("title", "");

    item.increment.addEventListener("keyup", () => {
      correctInputFieldValue(item.increment, 0, parseFloat(weightConstraint));
      toggleConfirmationFormulationsButtons(independentInputFields);
    });
  }
}

function toggleConfirmationFormulationsButtons(inputFields) {
  const allIncrementsFilled = inputFields.filter((item) => item["increment"].value === "").length === 0;
  const allMinFilled = inputFields.filter((item) => item["min"].value === "").length === 0;
  const allMaxFilled = inputFields.filter((item) => item["max"].value === "").length === 0;
  document.getElementById("confirm_formulations_configuration_button").disabled = !(
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
  let numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

  if (!only_independent) {
    numberOfIndependentRows += 1;
  }

  const inputFields = [];
  for (let i = 0; i < numberOfIndependentRows; i++) {
    const min = document.getElementById(`materials_min_max_entries-${i}-min`);
    const max = document.getElementById(`materials_min_max_entries-${i}-max`);
    const increment = document.getElementById(`materials_min_max_entries-${i}-increment`);
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
  return {
    materials_formulation_configuration: rowData,
    weight_constraint: weightConstraint,
  };
}

// there are two elements for each process, one hidden and one visible. Therefore we divide by 2
function collectProcessesRequestData() {
  const numberOfIndependentRows = document.querySelectorAll('[id^="non_editable_entries-"]').length / 2;

  const rowData = [];
  for (let i = 0; i < numberOfIndependentRows; i++) {
    const uuid = document.getElementById(`non_editable_entries-${i}-uuid_field`).value;
    rowData.push({
      uuid: uuid,
    });
  }
  return {
    processes: rowData,
  };
}

function collectMaterialRequestData() {
  const numberOfMaterialsRows = document.querySelectorAll('[id$="-min"]').length - 1;

  const rowData = [];
  for (let i = 0; i <= numberOfMaterialsRows; i++) {
    const uuids = document.getElementById(`materials_min_max_entries-${i}-uuid_field`);
    const type = document.getElementById(`materials_min_max_entries-${i}-type_field`);
    rowData.push({
      uuids: uuids.value,
      type: type.value,
    });
  }
  return {
    materials_formulation_configuration: rowData,
  };
}

function collectWeights() {
  const weightFields = document.querySelectorAll('[id^="all_weights_entries-"]');

  const weightData = [];
  for (const weightField of weightFields) {
    weightData.push(weightField.value);
  }
  return {
    all_weights: weightData,
  };
}

function computeDependentValue(inputFieldName, currentInputField, independentMinMaxInputFields) {
  const sumOfIndependentFields = autocorrectInput(independentMinMaxInputFields, inputFieldName, currentInputField);

  const unfilledFields = independentMinMaxInputFields.filter((item) => item[inputFieldName].value === "");
  if (unfilledFields.length === 0) {
    const lastMinItem = document.getElementById(
      `materials_min_max_entries-${independentMinMaxInputFields.length}-${inputFieldName}`
    );
    lastMinItem.value = (weightConstraint - sumOfIndependentFields).toFixed(2);
  }
}

function autocorrectInput(independentMinMaxInputFields, inputFieldName, currentInputField) {
  correctInputFieldValue(currentInputField, 0);

  // Empty values => NaN; all others are parsed to float
  let independentFieldValues = independentMinMaxInputFields.map((item) => parseFloat(item[inputFieldName].value));

  // Multiply the liquid value (second in array/index 1) with the powder value (first in array/index 0)
  // Since liquid is given as a ratio of powder
  // The + casts to a number, because toFixed returns strings...
  independentFieldValues[1] = +(independentFieldValues[0] * independentFieldValues[1]).toFixed(2);

  let sumOfIndependentFields = independentFieldValues
    .filter((item) => !Number.isNaN(item))
    .reduce((x, y) => x + y, 0);

  if (sumOfIndependentFields > weightConstraint) {
    if (currentInputField.id.includes(LIQUID_HTML_ID_INCLUDES)) {
      // liquids need to be updated with a ratio instead of a total
      currentInputField.value = (
          (weightConstraint - (sumOfIndependentFields - independentFieldValues[1])) / independentFieldValues[0]
      ).toFixed(2);
    } else {
      currentInputField.value = (weightConstraint - (sumOfIndependentFields - currentInputField.value)).toFixed(2);
    }
    sumOfIndependentFields = weightConstraint;
  }
  return sumOfIndependentFields;
}

function assignKeyboardEventsToWeightForm(initialCreationOfForm = false) {
  if (initialCreationOfForm) {
    allWeightFieldsHaveValidInput = true;
  }

  toggleSubmitButtonBasedOnWeights();
}

function toggleSubmitButtonBasedOnWeights() {
  const weightFields = collectWeightFields();
  const numberOfMaterials = document.querySelectorAll('[id$="-min"]').length - 1;
  for (const weightInput of weightFields) {
    weightInput.addEventListener("keyup", () => {
      toggleSubmitButtonBasedOnWeightInput(numberOfMaterials, weightFields);
    });
  }
}

function collectWeightFields() {
  const numberOfWeightFields = document.querySelectorAll('[id$="-weights"]').length;

  const weightFields = [];
  for (let i = 0; i < numberOfWeightFields; i++) {
    const weights = document.getElementById(`all_weights_entries-${i}-weights`);
    weightFields.push(weights);
  }
  return weightFields;
}

function toggleSubmitButtonBasedOnWeightInput(numberOfMaterials, weightFields) {
  const regex = new RegExp("^\\d+([.,]\\d{1,2})*(/\\d+([.,]\\d{1,2})*){" + numberOfMaterials + "}$");
  const nonMatchingInputs = weightFields.map((input) => input.value).filter((value) => !regex.test(value)).length;
  allWeightFieldsHaveValidInput = nonMatchingInputs <= 0;
  document.getElementById("create_formulations_batch_button").disabled = !allWeightFieldsHaveValidInput;
}
