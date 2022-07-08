const BLENDED_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/blended`

let allSelectedOptions = []

/**
 * When changing the base material type, we dynamically replace the multiselect input field. As a consequence, the change event
 * related to choosing from this selection must be reattached to it.
 */
async function selectBaseMaterialType() {
    document.getElementById("confirm_selection_for_blending_button").removeEventListener("click", confirmSelection)

    const elem = document.getElementById("base_type");
    const url = `${BLENDED_MATERIALS_URL}/${elem.value.toLowerCase()}`;
    await fetchEmbedTemplateInPlaceholder(url, "base-material-selection-placeholder");

    document.getElementById("confirm_selection_for_blending_button").addEventListener("click", confirmSelection)
}

async function confirmSelection() {
    document.getElementById("min-max-placeholder").innerHTML = ""

    count = 0
    selectedMaterials = []
    const placeholder = document.getElementById("base_material_selection")
    if (placeholder.childElementCount !== 0) {
        let options = placeholder.children;
        for (let i = 0; i < options.length; i++) {
            if (options[i].selected) {
                count++
                selectedMaterials.push({
                    uuid: options[i].value,
                    name: options[i].innerHTML
                })
            }
        }
    }

    const url = `${BLENDED_MATERIALS_URL}/add_min_max_entries/${count}`;
    await fetchEmbedTemplateInPlaceholder(url, "min-max-placeholder", true);

    if (placeholder.childElementCount !== 0) {
        for (let i = 0; i < selectedMaterials.length; i++) {
            document.getElementById(`all_min_max_entries-${i}-uuid_field`).value = selectedMaterials[i].uuid;
            document.getElementById(`all_min_max_entries-${i}-blended_material_name`).value = selectedMaterials[i].name;
        }
    }

}

window.addEventListener("load", function () {
    document.getElementById("base_type").addEventListener("change", selectBaseMaterialType)
    document.getElementById("confirm_selection_for_blending_button").addEventListener("click", confirmSelection)
});
