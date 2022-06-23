const selectMaterialType = () => {
    const elem = document.getElementById("material_type");

    elem.addEventListener("change", async () => {
        try {
            const response = await fetch(`http://localhost:5001/materials/${elem.value.toLowerCase()}`);
            const form = await response.json();
            document.getElementById("template-placeholder").innerHTML = form["template"];
        } catch (error) {
            console.log(error);
        }
    });
}

function collectAdditionalProperties(newPropIndex) {
    usersInputs = []
    if (newPropIndex > 0) {

        for (let i = 0; i < newPropIndex; i++) {
            let name = document.getElementById(`additional-properties-${i}-name`).value;
            let value = document.getElementById(`additional-properties-${i}-value`).value;
            usersInputs.push({
                name: name,
                value: value
            })
        }
    }
    return usersInputs;
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
            const response = await fetch(`http://localhost:5001/materials/add_property/${newPropIndex}`);
            const form = await response.json();
            placeholder.innerHTML += form["template"];
            for (let i = 0; i < usersInputs.length; i++) {
                document.getElementById(`additional-properties-${i}-name`).value = usersInputs[i].name;
                document.getElementById(`additional-properties-${i}-value`).value = usersInputs[i].value;
            }
        } catch (error) {
            console.log(error);
        }
    });
}

window.addEventListener("load", selectMaterialType);
window.addEventListener("load", addAdditionalProperty);
