const selectMaterialType = () => {
    const elem = document.getElementById('material_type');

    elem.addEventListener("change", async () => {
        try {
            const response = await fetch(`http://localhost:5001/materials/${elem.value.toLowerCase()}`);
            const form = await response.json();
            document.getElementById("template-placeholder").innerHTML = form['template'];
        } catch (error) {
            console.log(error)
        }
    }
    )
}

const addProperty = () => {
    const elem = document.getElementById("add_property_button");
    const name = document.getElementById("additional_properties-0-name");
    const value = document.getElementById("additional_properties-0-value");

    elem.addEventListener("click", async () => {
        try {
            const response = await fetch("http://localhost:5001/materials/add_property", {
                method: "POST", headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },

                //make sure to serialize your JSON body
                body: JSON.stringify({
                    name: name.value,
                    value: value.value
                })
            });
        } catch (error) {
            console.log(error)
        }
    }
    )


}

window.addEventListener("load", selectMaterialType)
window.addEventListener("load", addProperty)
