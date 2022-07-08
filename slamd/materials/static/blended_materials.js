const BLENDED_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/blended`

async function fetchEmbedTemplateInPlaceholder(url, placeholderID, append = false) {
    const response = await fetch(url);
    if (response.ok) {
        const form = await response.json();
        if (append) {
            document.getElementById(placeholderID).innerHTML += form["template"];
        } else {
            document.getElementById(placeholderID).innerHTML = form["template"];
        }
    } else {
        const error = await response.text()
        document.write(error)
    }
}

async function selectBaseMaterialType() {
    document.getElementById("base_material_selection").removeEventListener("change", createFieldsForSelectedBaseMaterial)

    const elem = document.getElementById("base_type");
    const url = `${BLENDED_MATERIALS_URL}/${elem.value.toLowerCase()}`;
    await fetchEmbedTemplateInPlaceholder(url, "base-material-selection-placeholder");

    document.getElementById("base_material_selection").addEventListener("change", createFieldsForSelectedBaseMaterial)
}

async function createFieldsForSelectedBaseMaterial() {
    const placeholder = document.getElementById("min-max-placeholder");
    const newPropIndex = placeholder.childElementCount;

    const url = `${BLENDED_MATERIALS_URL}/add_min_max_entry/${newPropIndex}`;
    await fetchEmbedTemplateInPlaceholder(url, "min-max-placeholder", true);
}

window.addEventListener("load", function () {
    document.getElementById("base_type").addEventListener("change", selectBaseMaterialType)
    document.getElementById("base_material_selection").addEventListener("change", createFieldsForSelectedBaseMaterial)
});
