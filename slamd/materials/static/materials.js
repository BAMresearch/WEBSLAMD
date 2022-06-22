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

const addAdditionalProperty = () => {
    const elem = document.getElementById("add_property_button");

    elem.addEventListener("click", async () => {
        try {
            const response = await fetch("http://localhost:5001/materials/add_property");
            const form = await response.json();
            document.getElementById("additional-properties-placeholder").innerHTML += form["template"];
        } catch (error) {
            console.log(error);
        }
    });
}

window.addEventListener("load", selectMaterialType);
window.addEventListener("load", addAdditionalProperty);
