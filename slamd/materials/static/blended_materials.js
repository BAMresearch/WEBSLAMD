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

async function createFieldsForSelectedBaseMaterial(event) {
    const placeholder = document.getElementById("min-max-placeholder")
    let userInputs = [];
    if (placeholder.childElementCount !== 0) {
        userInputs = collectSelectedMaterials(event);
    }

    for (let option of allSelectedOptions) {
        console.log(option.innerHTML)
    }
    let selectedIndex = event.target.options.selectedIndex;
    let clicked_material = event.target.options[selectedIndex];


    const url = `${BLENDED_MATERIALS_URL}/add_min_max_entry/${selectedIndex}`;
    await fetchEmbedTemplateInPlaceholder(url, "min-max-placeholder", true);

    document.getElementById(`min-max-properties-${selectedIndex}-name`).value = clicked_material.innerHTML;

    if (userInputs.length !== 0) {
        restoreAdditionalProperties(userInputs)
    }
}

async function confirmSelection() {
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

function collectSelectedMaterials(event) {
    usersInputs = [];

    let options = event.target.options;
    for (let i = 0; i < options.length; i++) {
        if (options[i].selected && i !== options.selectedIndex) {
            let name = document.getElementById(`min-max-properties-${i}-name`).value;

            usersInputs.push({
                name: name
            });
        }
    }
    return usersInputs;
}

function restoreAdditionalProperties(usersInputs) {
    for (let i = 0; i < usersInputs.length; i++) {
        document.getElementById(`min-max-properties-${i}-name`).value = usersInputs[i].name;
    }
}

window.addEventListener("load", function () {
    document.getElementById("base_type").addEventListener("change", selectBaseMaterialType)
    // document.getElementById("base_material_selection").addEventListener("change", createFieldsForSelectedBaseMaterial)
    document.getElementById("confirm_selection_for_blending_button").addEventListener("click", confirmSelection)
});
