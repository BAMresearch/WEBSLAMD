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

function assignConfirmBlendingConfigurationEvent() {
    const elem = document.getElementById("confirm_blending_configuration_button");
    const token = document.getElementById("csrf_token").value

    elem.addEventListener("click", async () => {
        const minMaxValuesWithIncrements = createMinMaxValuesWithIncrements();
        try {
            const url = `${BLENDED_MATERIALS_URL}/add_ratios`;
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    'X-CSRF-TOKEN': token
                },
                body: JSON.stringify(minMaxValuesWithIncrements)
            });
            const form = await response.json();
            document.getElementById("blending_ratio_placeholder").innerHTML = form["template"];

        } catch (error) {
            console.log(error);
        }
        assignKeyboardEventsToRatiosForm();
        assignAddCustomBlendEvent()

    })

}

function toggleConfirmationButton() {
    const placeholder = document.getElementById("base_material_selection");
    const count = countSelectedBaseMaterials(placeholder);
    document.getElementById("change_base_material_selection_button").disabled = count < 2;
}

window.addEventListener("load", function () {
    document.getElementById("base_type").addEventListener("change", selectBaseMaterialType);
    document.getElementById("base_material_selection").addEventListener("change", toggleConfirmationButton);
});
