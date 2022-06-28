const protocol = window.location.protocol
const host = window.location.host;

const selectMaterialType = () => {
    const elem = document.getElementById("material_type");

    elem.addEventListener("change", async () => {
        try {
            const url = `${protocol}//${host}/materials/${elem.value.toLowerCase()}`;
            const response = await fetch(url);
            const form = await response.json();
            document.getElementById("template-placeholder").innerHTML = form["template"];
        } catch (error) {
            console.log(error);
        }
    });
}

const showAllMaterialsForType = () => {
    const elem = document.getElementById("show_all_materials_for_type_dropdown");

    elem.addEventListener("change", async () => {
        try {
            const url = `${protocol}//${host}/materials/all/${elem.value.toLowerCase()}`;
            const response = await fetch(url);
            const form = await response.json();
            document.getElementById("base_materials_table_placeholder").innerHTML = form["template"];
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
    const elem = document.getElementById("add-property-button");

    elem.addEventListener("click", async () => {
        // Each additional property form is contained in one single div.
        // We index the additional properties starting from zero.
        const placeholder = document.getElementById("additional-properties-placeholder")
        const newPropIndex = placeholder.childElementCount;

        const usersInputs = collectAdditionalProperties(newPropIndex);

        try {
            const url = `${protocol}//${host}/materials/add_property/${newPropIndex}`;
            const response = await fetch(url);
            const form = await response.json();
            placeholder.innerHTML += form["template"];
        } catch (error) {
            console.log(error);
        }

        restoreAdditionalProperties(usersInputs);
    });
}

const deleteAdditionalProperty = () => {
    const elem = document.getElementById("delete-property-button");

    elem.addEventListener("click", () => {
        const placeholder = document.getElementById("additional-properties-placeholder");
        const newPropIndex = placeholder.childElementCount;
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
