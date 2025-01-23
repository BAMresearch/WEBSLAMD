let nameIsEmpty = true;

/**
 * When changing the base material type, we dynamically replace the multiselect input field. As a consequence, the change event
 * related to choosing from this selection must be reattached to it. Further, for consistency, former min-max fields are reset
 */
async function selectBaseMaterialType(event) {
  removeInnerHtmlFromPlaceholder("min-max-placeholder");
  removeInnerHtmlFromPlaceholder("blending-ratio-placeholder");
  document.getElementById("change-base-material-selection-button").disabled = true;

  const baseType = event.target.value;
  const url = `${BLENDED_MATERIALS_URL}/${baseType.toLowerCase()}`;
  await fetchDataAndEmbedTemplateInPlaceholder(url, "base-material-selection-placeholder");

  document.getElementById("base_material_selection").addEventListener("change", toggleConfirmationButton);
}

async function confirmSelection() {
  removeInnerHtmlFromPlaceholder("min-max-placeholder");
  removeInnerHtmlFromPlaceholder("blending-ratio-placeholder");

  const placeholder = document.getElementById("base_material_selection");

  const selectedMaterials = collectSelection(placeholder);
  const uuids = selectedMaterials.map((material) => material.uuid);

  const type = document.getElementById("base_type").value;

  const url = `${BLENDED_MATERIALS_URL}/add_min_max_entries/${type.toLowerCase()}/${selectedMaterials.length}`;
  insertSpinnerInPlaceholder("min-max-placeholder");
  await postDataAndEmbedTemplateInPlaceholder(url, "min-max-placeholder", uuids);
  removeSpinnerInPlaceholder("min-max-placeholder");

  prepareMinMaxInputFieldsFromSelection(selectedMaterials);
  assignKeyboardEventsToMinMaxForm();
  assignConfirmBlendingConfigurationEvent();
  assignChangeBlendingStrategyEvent();
}

async function assignConfirmBlendingConfigurationEvent() {
  const elem = document.getElementById("confirm-blending-configuration-button");
  enableTooltip(elem);

  elem.addEventListener("click", async () => {
    const minMaxValuesWithIncrements = collectMinMaxValuesWithIncrements();
    const url = `${BLENDED_MATERIALS_URL}/add_ratios`;

    insertSpinnerInPlaceholder("blending-ratio-placeholder");
    await postDataAndEmbedTemplateInPlaceholder(url, "blending-ratio-placeholder", minMaxValuesWithIncrements);
    removeSpinnerInPlaceholder("blending-ratio-placeholder");

    assignKeyboardEventsToRatiosForm(true);
    assignAddCustomBlendEvent();
    assignDeleteCustomBlendEvent();
  });
}

function assignChangeBlendingStrategyEvent(){
  document.getElementById("blending_strategy").addEventListener("change", function() {
    const blending_strategy = this.value
    const labels = document.getElementsByClassName('percentage-label');

    if (blending_strategy === 'Weight-based'){
      for (let label of labels) {
        label.textContent = label.textContent.replace('Vol.-%', 'W.-%');
      }
    }
    else {
      for (let label of labels) {
        label.textContent = label.textContent.replace('W.-%', 'Vol.-%');
      }
    }
  });
}

function toggleConfirmationButton() {
  const count = countSelectedOptionsMultipleSelectField(document.getElementById("base_material_selection"));
  document.getElementById("change-base-material-selection-button").disabled = count < 2;
}

function checkNameIsNotEmpty(event) {
  const blendedMaterialName = event.target.value;
  nameIsEmpty = blendedMaterialName === undefined || blendedMaterialName === "";
  document.getElementById("submit").disabled = nameIsEmpty || !allRatioFieldsHaveValidInput;
}

async function deleteMaterial(id, material_type) {
  deleteMaterialByType(id, material_type, true);
}


window.addEventListener("load", function () {
  document.getElementById("nav-bar-blended").setAttribute("class", "nav-link active");
  document.getElementById("blended_material_name").addEventListener("keyup", checkNameIsNotEmpty);
  document.getElementById("base_type").addEventListener("change", selectBaseMaterialType);
  document.getElementById("base_material_selection").addEventListener("change", toggleConfirmationButton);
});
