/**
 * Many functions look similar to the ones in blended_materials.js
 * Nevertheless, we choose not to extract common functions as the two use cases are in general not related and the
 * common functions would lead to tight coupling between these separated use cases.
 */
let allRatioFieldsHaveValidInput = false;

function countSelectedBaseMaterials(placeholder) {
  let count = 0;
  if (placeholder.childElementCount !== 0) {
    return Array.from(placeholder.children).filter((option) => option.selected).length;
  }
  return count;
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

function assignKeyboardEventsToMinMaxForm() {
  let independentInputFields = collectIndependentInputFields();

  for (let item of independentInputFields) {
    item.min.addEventListener("keyup", () => {
      computeDependentValue("min", item.min, independentInputFields);
      toggleConfirmBlendingButton(independentInputFields);
    });
    item.max.addEventListener("keyup", () => {
      computeDependentValue("max", item.max, independentInputFields);
      toggleConfirmBlendingButton(independentInputFields);
    });
    item.increment.addEventListener("keyup", () => {
      correctInputFieldValue(item.increment, 0, 100);
      toggleConfirmBlendingButton(independentInputFields);
    });
  }
}

function toggleConfirmBlendingButton(independentInputFields) {
  let allIncrementsFilled = independentInputFields.filter((item) => item["increment"].value === "").length === 0;
  let allMinFilled = independentInputFields.filter((item) => item["min"].value === "").length === 0;
  let allMaxFilled = independentInputFields.filter((item) => item["max"].value === "").length === 0;
  document.getElementById("confirm-blending-configuration-button").disabled = !(
    allIncrementsFilled &&
    allMinFilled &&
    allMaxFilled
  );
}

function assignKeyboardEventsToRatiosForm(initialCreationOfForm = false) {
  if (initialCreationOfForm) {
    allRatioFieldsHaveValidInput = true;
    document.getElementById("submit").disabled = nameIsEmpty;
  }

  toggleSubmitButtonBasedOnRatiosAndName();
}

function collectRatioFields() {
  const numberOfRatioFields = document.querySelectorAll('[id$="-ratio"]').length;

  let ratioInputFields = [];
  for (let i = 0; i < numberOfRatioFields; i++) {
    let ratio = document.getElementById(`all_ratio_entries-${i}-ratio`);
    ratioInputFields.push(ratio);
  }
  return ratioInputFields;
}

/**
 * The method extracts all min, max and increment input fields except the last one as the latter will be computed dynamically in terms
 * of all the other min/max values. The number of min items always equals the number of min items. Therefore we can get the
 * total number of rows simply by extracting the tags with id ending on -min.
 */
function collectIndependentInputFields() {
  const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

  let independentInputFields = [];
  for (let i = 0; i < numberOfIndependentRows; i++) {
    let min = document.getElementById(`all_min_max_entries-${i}-min`);
    let max = document.getElementById(`all_min_max_entries-${i}-max`);
    let increment = document.getElementById(`all_min_max_entries-${i}-increment`);
    independentInputFields.push({
      min: min,
      max: max,
      increment: increment,
    });
  }
  return independentInputFields;
}

function collectMinMaxValuesWithIncrements() {
  const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

  let minMaxValuesWithIncrements = [];
  for (let i = 0; i <= numberOfIndependentRows; i++) {
    let min = document.getElementById(`all_min_max_entries-${i}-min`);
    let max = document.getElementById(`all_min_max_entries-${i}-max`);
    let increment = document.getElementById(`all_min_max_entries-${i}-increment`);
    minMaxValuesWithIncrements.push({
      idx: i,
      min: parseFloat(min.value),
      max: parseFloat(max.value),
      increment: parseFloat(increment.value),
    });
  }
  return minMaxValuesWithIncrements;
}

function computeDependentValue(type, currentInputField, independentMinMaxInputFields) {
  let sumOfIndependentFields = autocorrectInput(independentMinMaxInputFields, type, currentInputField);

  const unfilledFields = independentMinMaxInputFields.filter((item) => item[type].value === "");
  if (unfilledFields.length === 0) {
    const lastMinItem = document.getElementById(`all_min_max_entries-${independentMinMaxInputFields.length}-${type}`);
    lastMinItem.value = (100 - sumOfIndependentFields).toFixed(2);
  }
}

function autocorrectInput(independentMinMaxInputFields, type, currentInputField) {
  correctInputFieldValue(currentInputField, 0);

  let sumOfIndependentFields = independentMinMaxInputFields
    .filter((item) => item[type].value !== "")
    .map((item) => parseFloat(item[type].value))
    .reduce((x, y) => x + y, 0);

  if (sumOfIndependentFields > 100) {
    currentInputField.value = (100 - (sumOfIndependentFields - currentInputField.value)).toFixed(2);
    sumOfIndependentFields = 100;
  }
  return sumOfIndependentFields;
}

/**
 * After adding a new field we need to reassign the ratio events as new input fields must be registered. Note that this functionality
 * requires a certain structure of DOM elements within the blending-ratio-placeholder. Thus, when changing this function always
 * check the corresponding HTML DOM structure and vice versa.
 */
function assignAddCustomBlendEvent() {
  const placeholder = document.getElementById("blending-ratio-placeholder");
  const button = document.getElementById("add-custom-blend-button");
  enableTooltip(button);

  button.addEventListener("click", () => {
    const numberOfRatioFields = document.querySelectorAll('[id$="-ratio"]').length - 1;
    let div = document.createElement("div");
    div.className = "col-md-3";

    let input = document.createElement("input");
    input.id = `all_ratio_entries-${numberOfRatioFields + 1}-ratio`;
    input.name = `all_ratio_entries-${numberOfRatioFields + 1}-ratio`;
    input.type = "text";
    input.className = "form-control";
    div.appendChild(input);

    placeholder.insertBefore(div, button);

    allRatioFieldsHaveValidInput = false;
    document.getElementById("submit").disabled = true;
    assignKeyboardEventsToRatiosForm();
  });
}

function assignDeleteCustomBlendEvent() {
  const button = document.getElementById("delete-custom-blend-button");
  enableTooltip(button);

  button.addEventListener("click", () => {
    const numberOfRatioFields = document.querySelectorAll('[id$="-ratio"]').length - 1;
    const elem = document.getElementById(`all_ratio_entries-${numberOfRatioFields}-ratio`);
    elem.parentElement.remove();

    let ratioInputFields = collectRatioFields();
    let numberOfIndependentBaseMaterials = document.querySelectorAll('[id$="-min"]').length - 1;

    toggleSubmitButtonBasedOnRatioInput(numberOfIndependentBaseMaterials, ratioInputFields);
    assignKeyboardEventsToRatiosForm();
  });
}

function toggleSubmitButtonBasedOnRatiosAndName() {
  let ratioInputFields = collectRatioFields();
  let numberOfIndependentBaseMaterials = document.querySelectorAll('[id$="-min"]').length - 1;
  for (let ratioInput of ratioInputFields) {
    ratioInput.addEventListener("keyup", () => {
      toggleSubmitButtonBasedOnRatioInput(numberOfIndependentBaseMaterials, ratioInputFields);
    });
  }
}

function toggleSubmitButtonBasedOnRatioInput(numberOfIndependentBaseMaterials, ratioInputFields) {
  let regex = new RegExp("^\\d+([.,]\\d{1,2})*(/\\d+([.,]\\d{1,2})*){" + numberOfIndependentBaseMaterials + "}$");
  let nonMatchingInputs = ratioInputFields.map((input) => input.value).filter((value) => !regex.test(value)).length;
  allRatioFieldsHaveValidInput = nonMatchingInputs <= 0;
  document.getElementById("submit").disabled = !(allRatioFieldsHaveValidInput && !nameIsEmpty);
}
