/**
 * Many functions look similar to the ones in blended_materials.js
 * Nevertheless, we choose not to extract common functions as the two use cases are in general not related and the
 * common functions would lead to tight coupling between these separated use cases.
 */
let allRatioFieldsHaveValidInput = false;

function prepareMinMaxInputFieldsFromSelection(selectedMaterials) {
  for (let i = 0; i < selectedMaterials.length; i++) {
    document.getElementById(`all_min_max_entries-${i}-uuid_field`).value = selectedMaterials[i].uuid;
    document.getElementById(`all_min_max_entries-${i}-blended_material_name`).value = selectedMaterials[i].name;
  }
}

function assignKeyboardEventsToMinMaxForm() {
  const independentInputFields = collectInputFields();

  for (const item of independentInputFields) {
    item.min.addEventListener("keyup", () => {
      toggleConfirmBlendingButton(independentInputFields);
    });
    item.max.addEventListener("keyup", () => {
      toggleConfirmBlendingButton(independentInputFields);
    });
    item.increment.addEventListener("keyup", () => {
      correctInputFieldValue(item.increment, 0, 100);
      toggleConfirmBlendingButton(independentInputFields);
    });
  }
}

function toggleConfirmBlendingButton(independentInputFields) {
  const allIncrementsFilled = independentInputFields.filter((item) => item["increment"].value === "").length === 0;
  const allMinFilled = independentInputFields.filter((item) => item["min"].value === "").length === 0;
  const allMaxFilled = independentInputFields.filter((item) => item["max"].value === "").length === 0;
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

  const ratioInputFields = [];
  for (let i = 0; i < numberOfRatioFields; i++) {
    const ratio = document.getElementById(`all_ratio_entries-${i}-ratio`);
    ratioInputFields.push(ratio);
  }
  return ratioInputFields;
}

/**
 * The method extracts all min, max and increment input fields except the last one as the latter will be computed dynamically in terms
 * of all the other min/max values. The number of min items always equals the number of min items. Therefore we can get the
 * total number of rows simply by extracting the tags with id ending on -min.
 */
function collectInputFields() {
  const numberOfRows = document.querySelectorAll('[id$="-min"]').length;

  const inputFields = [];
  for (let i = 0; i < numberOfRows; i++) {
    const min = document.getElementById(`all_min_max_entries-${i}-min`);
    const max = document.getElementById(`all_min_max_entries-${i}-max`);
    const increment = document.getElementById(`all_min_max_entries-${i}-increment`);
    inputFields.push({
      min: min,
      max: max,
      increment: increment,
    });
  }
  return inputFields;
}

function collectMinMaxValuesWithIncrements() {
  const numberOfRows = document.querySelectorAll('[id$="-min"]').length;

  const minMaxValuesWithIncrements = [];
  for (let i = 0; i < numberOfRows; i++) {
    const min = document.getElementById(`all_min_max_entries-${i}-min`);
    const max = document.getElementById(`all_min_max_entries-${i}-max`);
    const increment = document.getElementById(`all_min_max_entries-${i}-increment`);
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
  const sumOfIndependentFields = autocorrectInput(independentMinMaxInputFields, type, currentInputField);

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
 * After adding a new field we need to reassign the ratio events as new input fields must be registered.
 * Note that this functionality requires a certain structure of DOM elements within the ratio-entries div tag.
 * Thus, when changing this function always check the corresponding HTML DOM structure and vice versa.
 */
function assignAddCustomBlendEvent() {
  const ratioEntries = document.getElementById("ratio-entries");
  const button = document.getElementById("add-custom-blend-button");
  enableTooltip(button);

  button.addEventListener("click", () => {
    const numberOfRatioFields = ratioEntries.childElementCount;
    const div = document.createElement("div");
    div.className = "col-3";

    const input = document.createElement("input");
    input.id = `all_ratio_entries-${numberOfRatioFields}-ratio`;
    input.name = `all_ratio_entries-${numberOfRatioFields}-ratio`;
    input.type = "text";
    input.className = "form-control";
    div.appendChild(input);

    ratioEntries.appendChild(div);

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

    const ratioInputFields = collectRatioFields();
    const numberOfIndependentBaseMaterials = document.querySelectorAll('[id$="-min"]').length - 1;

    toggleSubmitButtonBasedOnRatioInput(numberOfIndependentBaseMaterials, ratioInputFields);
    assignKeyboardEventsToRatiosForm();
  });
}

function toggleSubmitButtonBasedOnRatiosAndName() {
  const ratioInputFields = collectRatioFields();
  const numberOfBaseMaterials = document.querySelectorAll('[id$="-min"]').length - 1;
  for (const ratioInput of ratioInputFields) {
    ratioInput.addEventListener("keyup", () => {
      toggleSubmitButtonBasedOnRatioInput(numberOfBaseMaterials, ratioInputFields);
    });
  }
}

function toggleSubmitButtonBasedOnRatioInput(numberOfBaseMaterials, ratioInputFields) {
  const regex = new RegExp("^\\d+([.,]\\d{1,2})*(/\\d+([.,]\\d{1,2})*){" + numberOfBaseMaterials + "}$");
  const nonMatchingInputs = ratioInputFields.map((input) => input.value).filter((value) => !regex.test(value)).length;
  allRatioFieldsHaveValidInput = nonMatchingInputs <= 0;
  document.getElementById("submit").disabled = !(allRatioFieldsHaveValidInput && !nameIsEmpty);
}
