const PROTOCOL = window.location.protocol
const HOST = window.location.host;
const ACTION_BUTTON_DELIMITER = "DELIMITER"

const selectMaterialType = () => {
    const elem = document.getElementById("material_type");

    elem.addEventListener("change", async () => {
        try {
            const url = `${PROTOCOL}//${HOST}/materials/${elem.value.toLowerCase()}`;
            const response = await fetch(url);
            const form = await response.json();
            document.getElementById("template-placeholder").innerHTML = form["template"];
        } catch (error) {
            console.log(error);
        }
    });
}

const collectAdditionalProperties = (newPropIndex) => {
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

const restoreAdditionalProperties = (usersInputs) => {
    for (let i = 0; i < usersInputs.length; i++) {
        document.getElementById(`additional-properties-${i}-name`).value = usersInputs[i].name;
        document.getElementById(`additional-properties-${i}-value`).value = usersInputs[i].value;
    }
}

const addAdditionalProperty = () => {
    const elem = document.getElementById("add_property_button");

    elem.addEventListener("click", async () => {
        // Each additional property form is contained in one single div.
        // We index the additional properties starting from zero.
        const placeholder = document.getElementById("additional-properties-placeholder")
        const newPropIndex = placeholder.childElementCount;

        const usersInputs = collectAdditionalProperties(newPropIndex);

        try {
            const url = `${PROTOCOL}//${HOST}/materials/add_property/${newPropIndex}`;
            const response = await fetch(url);
            const form = await response.json();
            placeholder.innerHTML += form["template"];
        } catch (error) {
            console.log(error);
        }

        restoreAdditionalProperties(usersInputs)
        // Set up delete button
        const deleteButton = document.getElementById(`additional-properties-${newPropIndex}-delete`)
        deleteButton.addEventListener("click", () => {
            // Select the row div element that contains the whole new entry and delete it
            document.getElementById(`additional-properties-${newPropIndex}-row`).remove()
        });
    });
}

/**
 * The input parameter corresponds to the id of the html button element. It is specified in base_materials_table.html
 * For consistency, it is constructed from a part describing the action, here 'delete_base_material_button' and a uuid
 * identifying the corresponding model object. To extract it for calling our API, we use the special delimiter.
 *
 * @param id
 */
async function deleteMaterial(id, material_type, token) {
    if (material_type !== undefined) {
        token = document.getElementById("csrf_token").value
        let uuid = id.split(ACTION_BUTTON_DELIMITER)[1];
        try {
            const url = `${PROTOCOL}//${HOST}/materials/${material_type.toLowerCase()}/${uuid}`;
            const response = await fetch(url, {
                method: "DELETE",
                headers: {
                    'X-CSRF-TOKEN': token
                }
            });
            const form = await response.json();
            document.getElementById("base_materials_table_placeholder").innerHTML = form["template"];
        } catch (error) {
            console.log(error);
        }
    }

}

/**
 * The input parameter corresponds to the id of the html button element. It is specified in base_materials_table.html
 * For consistency, it is constructed from a part describing the action, e.g. 'edit_base_material_button' and a uuid
 * identifying the corresponding model object. To extract it for calling our API, we use the special delimiter.
 *
 * @param id
 */
function editMaterial(id, material_type) {
    console.log("EDIT")
}

window.addEventListener("load", selectMaterialType);
window.addEventListener("load", addAdditionalProperty);
window.addEventListener("load", deleteMaterial);
window.addEventListener("load", editMaterial);
