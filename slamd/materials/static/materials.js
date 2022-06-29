const protocol = window.location.protocol
const host = window.location.host;
const warningMaxNumberProperties = "<p class=\"text-warning\">You may define up to 10 additional properties</p>";
const maxNumberProperties = 10;

async function fetchEmbedTemplateInPlaceholder(url, placeholderID) {
    try {
        const response = await fetch(url);
        const form = await response.json();
        document.getElementById(placeholderID).innerHTML = form["template"];
    } catch (error) {
        console.log(error);
    }
}

function selectMaterialType() {
    const elem = document.getElementById("material_type");

    elem.addEventListener("change", () => {
        const url = `${protocol}//${host}/materials/${elem.value.toLowerCase()}`;
        fetchEmbedTemplateInPlaceholder(url, "template-placeholder");
    });
}

function showAllMaterialsForType() {
    const elem = document.getElementById("show_all_materials_for_type_dropdown");

    elem.addEventListener("change", () => {
        const url = `${protocol}//${host}/materials/all/${elem.value.toLowerCase()}`;
        fetchEmbedTemplateInPlaceholder(url, "base_materials_table_placeholder");
    });
}

function collectAdditionalProperties(newPropIndex) {
    usersInputs = [];
    if (newPropIndex <= 0) {
        return usersInputs;
    }

    for (let i = 0; i < newPropIndex; i++) {
        let name = document.getElementById(`additional-properties-${i}-name`).value;
        let value = document.getElementById(`additional-properties-${i}-value`).value;
        usersInputs.push({
            name: name,
            value: value
        });
    }
    return usersInputs;
}

function restoreAdditionalProperties(usersInputs) {
    for (let i = 0; i < usersInputs.length; i++) {
        document.getElementById(`additional-properties-${i}-name`).value = usersInputs[i].name;
        document.getElementById(`additional-properties-${i}-value`).value = usersInputs[i].value;
    }
}

function addAdditionalProperty() {
    const elem = document.getElementById("add-property-button");

    elem.addEventListener("click", () => {
        // Each additional property form is contained in one single div.
        // We index the additional properties starting from zero.
        const placeholder = document.getElementById("additional-properties-placeholder")
        const newPropIndex = placeholder.childElementCount;

        // Handle max number of properties and show a warning
        if (newPropIndex === maxNumberProperties) {
            placeholder.innerHTML += warningMaxNumberProperties;
            return;
        }

        const usersInputs = collectAdditionalProperties(newPropIndex);

        const url = `${protocol}//${host}/materials/add_property/${newPropIndex}`;
        fetchEmbedTemplateInPlaceholder(url, "additional-properties-placeholder");
        restoreAdditionalProperties(usersInputs);
    });
}

function deleteAdditionalProperty() {
    const elem = document.getElementById("delete-property-button");

    elem.addEventListener("click", () => {
        const placeholder = document.getElementById("additional-properties-placeholder");
        const newPropIndex = placeholder.childElementCount;

        // Remove the warning for the max number of properties
        if (newPropIndex === maxNumberProperties + 1) {
            placeholder.innerHTML = placeholder.innerHTML.replace(warningMaxNumberProperties, "");
            document.getElementById(`additional-properties-${newPropIndex - 2}-row`).remove();
            return;
        }

        // Select the row div element that contains the last entry and delete it
        if (newPropIndex > 0) {
            document.getElementById(`additional-properties-${newPropIndex - 1}-row`).remove();
        }
    });
}

window.addEventListener("load", selectMaterialType);
window.addEventListener("load", showAllMaterialsForType);
window.addEventListener("load", addAdditionalProperty);
window.addEventListener("load", deleteAdditionalProperty);
