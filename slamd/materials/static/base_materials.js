const PROTOCOL = window.location.protocol
const HOST = window.location.host;
const ACTION_BUTTON_DELIMITER = "___"
const WARNING_MAX_ADDITIONAL_PROPERTIES = "<p class=\"text-warning\">You may define up to 10 additional properties</p>";
const MAX_ADDITIONAL_PROPERTIES = 10;

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

function selectMaterialType() {
    const elem = document.getElementById("material_type");

    elem.addEventListener("change", () => {
        const url = `${PROTOCOL}//${HOST}/materials/base/${elem.value.toLowerCase()}`;
        fetchEmbedTemplateInPlaceholder(url, "template-placeholder");
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
        if (newPropIndex === MAX_ADDITIONAL_PROPERTIES) {
            placeholder.innerHTML += WARNING_MAX_ADDITIONAL_PROPERTIES;
            return;
        }

        const usersInputs = collectAdditionalProperties(newPropIndex);

        const url = `${PROTOCOL}//${HOST}/materials/base/add_property/${newPropIndex}`;
        fetchEmbedTemplateInPlaceholder(url, "additional-properties-placeholder", true);
        restoreAdditionalProperties(usersInputs);
    });
}

function deleteAdditionalProperty() {
    const elem = document.getElementById("delete-property-button");

    elem.addEventListener("click", () => {
        const placeholder = document.getElementById("additional-properties-placeholder");
        const newPropIndex = placeholder.childElementCount;

        // Remove the warning for the max number of properties
        if (newPropIndex === MAX_ADDITIONAL_PROPERTIES + 1) {
            placeholder.innerHTML = placeholder.innerHTML.replace(WARNING_MAX_ADDITIONAL_PROPERTIES, "");
            document.getElementById(`additional-properties-${newPropIndex - 2}-row`).remove();
            return;
        }

        // Select the row div element that contains the last entry and delete it
        if (newPropIndex > 0) {
            document.getElementById(`additional-properties-${newPropIndex - 1}-row`).remove();
        }
    });
}

/**
 * The input parameter corresponds to the id of the html button element. It is specified in base_materials_table.html
 * For consistency, it is constructed from a part describing the action, here 'delete_material_button' and a uuid
 * identifying the corresponding model object. To extract it for calling our API, we use the special delimiter.
 *
 * @param id
 */
async function deleteMaterial(id, material_type, token) {
    if (material_type) {
        token = document.getElementById("csrf_token").value
        let uuid = id.split(ACTION_BUTTON_DELIMITER)[1];
        try {
            const url = `${PROTOCOL}//${HOST}/materials/base/${material_type.toLowerCase()}/${uuid}`;
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

}

/**
 * The input parameter corresponds to the id of the html button element. It is specified in base_materials_table.html
 * For consistency, it is constructed from a part describing the action, e.g. 'edit_material_button' and a uuid
 * identifying the corresponding model object. To extract it for calling our API, we use the special delimiter.
 *
 * @param id
 */
function editMaterial(id, material_type) {
    console.log("EDIT")
}

window.addEventListener("load", selectMaterialType);
window.addEventListener("load", addAdditionalProperty);
window.addEventListener("load", deleteAdditionalProperty);
window.addEventListener("load", deleteMaterial);
window.addEventListener("load", editMaterial);
