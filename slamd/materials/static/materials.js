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
            const url = `${protocol}//${host}/materials/add_property/${newPropIndex}`;
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

function deleteMaterial(id){
    console.log(id)
}

window.addEventListener("load", selectMaterialType);
window.addEventListener("load", addAdditionalProperty);
window.addEventListener("load", deleteMaterial);
