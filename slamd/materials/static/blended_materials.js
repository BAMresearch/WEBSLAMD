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
    }
    else {
        const error = await response.text()
        document.write(error)
    }
}

function selectBaseMaterialType() {
    const elem = document.getElementById("base_type");

    elem.addEventListener("change", () => {
        const url = `${BLENDED_MATERIALS_URL}/${elem.value.toLowerCase()}`;
        fetchEmbedTemplateInPlaceholder(url, "base-material-selection-placeholder");
    });
}

function createFieldsForSelectedBaseMaterial() {
    const elem = document.getElementById("base_material_selection")

    elem.addEventListener("change", () => {
        document.getElementById("ratios-placeholder").innerHTML += "<p> html </p>";
        })
}

window.addEventListener("load", selectBaseMaterialType);
window.addEventListener("load", createFieldsForSelectedBaseMaterial);