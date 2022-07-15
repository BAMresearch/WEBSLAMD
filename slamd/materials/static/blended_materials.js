const BLENDED_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/blended`

let nameIsEmpty = true;

/**
 * When changing the base material type, we dynamically replace the multiselect input field. As a consequence, the change event
 * related to choosing from this selection must be reattached to it. Further, for consistency, former min-max fields are reset
 */
async function selectBaseMaterialType() {
    removeInnerHtmlFromPlaceholder("min-max-placeholder")
    removeInnerHtmlFromPlaceholder("blending_ratio_placeholder")
    document.getElementById("change_base_material_selection_button").disabled = true;

    const elem = document.getElementById("base_type");
    const url = `${BLENDED_MATERIALS_URL}/${elem.value.toLowerCase()}`;
    await fetchEmbedTemplateInPlaceholder(url, "base-material-selection-placeholder");

    document.getElementById("base_material_selection").addEventListener("change", toggleConfirmationButton);
}

async function confirmSelection() {
    removeInnerHtmlFromPlaceholder("min-max-placeholder")
    removeInnerHtmlFromPlaceholder("blending_ratio_placeholder")

    const placeholder = document.getElementById("base_material_selection");

    const selectedMaterials = collectBaseMaterialSelection(placeholder);

    const url = `${BLENDED_MATERIALS_URL}/add_min_max_entries/${selectedMaterials.length}`;
    await fetchEmbedTemplateInPlaceholder(url, "min-max-placeholder", true);

    prepareMinMaxInputFieldsFromSelection(selectedMaterials);
    assignKeyboardEventsToMinMaxForm();
    assignConfirmBlendingConfigurationEvent();
}

async function assignConfirmBlendingConfigurationEvent() {
    const elem = document.getElementById("confirm_blending_configuration_button");

    elem.addEventListener("click", async () => {
        const minMaxValuesWithIncrements = createMinMaxValuesWithIncrements();
        const url = `${BLENDED_MATERIALS_URL}/add_ratios`;
        await postDataAndEmbedTemplateInPlaceholder(url, "blending_ratio_placeholder", minMaxValuesWithIncrements)
        assignKeyboardEventsToRatiosForm(true);
        assignAddCustomBlendEvent();
    })
}

function toggleConfirmationButton() {
    const placeholder = document.getElementById("base_material_selection");
    const count = countSelectedBaseMaterials(placeholder);
    document.getElementById("change_base_material_selection_button").disabled = count < 2;
}

function checkNameIsNotEmpty() {
    let nameField = document.getElementById("blended_material_name");
    nameIsEmpty = nameField.value === undefined || nameField.value === ""
    document.getElementById("submit").disabled = nameIsEmpty || !allRatioFieldsHaveValidInput;
}

window.addEventListener("load", function () {
    document.getElementById("base_type").addEventListener("change", selectBaseMaterialType);
    document.getElementById("base_material_selection").addEventListener("change", toggleConfirmationButton);
    document.getElementById("blended_material_name").addEventListener("change", checkNameIsNotEmpty);
});
