const BLENDED_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/blended`

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
        assignKeyboardEventsToRatiosForm();
        assignAddCustomBlendEvent();
    })
}

function toggleConfirmationButton() {
    const placeholder = document.getElementById("base_material_selection");
    const count = countSelectedBaseMaterials(placeholder);
    document.getElementById("change_base_material_selection_button").disabled = count < 2;
}

/**
 * The input parameter corresponds to the id of the html button element. It is specified in blended_materials_table.html
 * For consistency, it is constructed from a part describing the action, here 'delete_material_button' and a uuid
 * identifying the corresponding model object. To extract it for calling our API, we use the special delimiter.
 *
 * @param id
 * @param material_type
 * @param token
 */
async function deleteBlendedMaterial(id, material_type, token) {
    token = document.getElementById("csrf_token").value
    let uuid = id.split(ACTION_BUTTON_DELIMITER)[1];
    try {
        const url = `${BLENDED_MATERIALS_URL}/${material_type.toLowerCase()}/${uuid}`;
        const response = await fetch(url, {
            method: "DELETE",
            headers: {
                'X-CSRF-TOKEN': token
            }
        });
        const form = await response.json();
        document.getElementById("materials_table_placeholder").innerHTML = form["template"];
    } catch (error) {
        console.log(error);
    }
}

window.addEventListener("load", function () {
    document.getElementById("base_type").addEventListener("change", selectBaseMaterialType);
    document.getElementById("base_material_selection").addEventListener("change", toggleConfirmationButton);
});
