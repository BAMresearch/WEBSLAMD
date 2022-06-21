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
    const elem = document.getElementById('add_button');

    elem.addEventListener("click", async () => {
            try {
                const response = await fetch(`http://localhost:5001/materials/add_property`);
            } catch (error) {
                console.log(error)
            }
        }
    )


}

window.addEventListener("load", selectMaterialType)
window.addEventListener("load", addProperty)
