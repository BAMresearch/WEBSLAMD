const BLENDED_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/blended`

/**
 * When changing the base material type, we dynamically replace the multiselect input field. As a consequence, the change event
 * related to choosing from this selection must be reattached to it. Further, for consistency, former min-max fields are reset
 */
async function selectBaseMaterialType() {
    document.getElementById("min-max-placeholder").innerHTML = "";

    const elem = document.getElementById("base_type");
    const url = `${BLENDED_MATERIALS_URL}/${elem.value.toLowerCase()}`;
    await fetchEmbedTemplateInPlaceholder(url, "base-material-selection-placeholder");
}

async function confirmSelection() {
    let minMaxPlaceholder = document.getElementById("min-max-placeholder");
    minMaxPlaceholder.innerHTML = "";

    const placeholder = document.getElementById("base_material_selection");

    const {count, selectedMaterials} = collectBaseMaterialSelection(placeholder);

    const url = `${BLENDED_MATERIALS_URL}/add_min_max_entries/${count}`;
    await fetchEmbedTemplateInPlaceholder(url, "min-max-placeholder", true);

    if (placeholder.childElementCount !== 0) {
        prefillMinMaxNamesFromSelection(selectedMaterials);
        assignKeyboardEventsToMinMaxInputFields();
        assignConfirmBlendingConfigurationEvent();
    }
}

function assignConfirmBlendingConfigurationEvent() {
    const elem = document.getElementById("confirm_blending_configuration_button");
    const token = document.getElementById("csrf_token").value

    elem.addEventListener("click", async () => {
        const minMaxValuesWithIncrements = createMinMaxValuesWithIncrements();
        try {
            const url = `${BLENDED_MATERIALS_URL}/add_ratios`;
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    'X-CSRF-TOKEN': token
                },
                body: JSON.stringify(minMaxValuesWithIncrements)
            });
            const form = await response.json();
            document.getElementById("blending_ratio_placeholder").innerHTML = form["template"];
        } catch (error) {
            console.log(error);
        }

    })

}

function createMinMaxValuesWithIncrements() {
    const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    let minMaxValuesWithIncrements = []
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        let min = document.getElementById(`all_min_max_entries-${i}-min`)
        let max = document.getElementById(`all_min_max_entries-${i}-max`)
        let increment = document.getElementById(`all_min_max_entries-${i}-increment`)
        minMaxValuesWithIncrements.push({
            idx: i,
            min: parseFloat(min.value),
            max: parseFloat(max.value),
            increment: parseFloat(increment.value)
        })
    }
    return minMaxValuesWithIncrements;
}

function collectBaseMaterialSelection(placeholder) {
    count = 0
    selectedMaterials = []
    if (placeholder.childElementCount !== 0) {
        let options = placeholder.children;
        for (let i = 0; i < options.length; i++) {
            if (options[i].selected) {
                count++
                selectedMaterials.push({
                    uuid: options[i].value,
                    name: options[i].innerHTML
                })
            }
        }
    }
    return {count, selectedMaterials};
}

function prefillMinMaxNamesFromSelection(selectedMaterials) {
    for (let i = 0; i < selectedMaterials.length; i++) {
        document.getElementById(`all_min_max_entries-${i}-uuid_field`).value = selectedMaterials[i].uuid;
        document.getElementById(`all_min_max_entries-${i}-blended_material_name`).value = selectedMaterials[i].name;
    }
}

function assignKeyboardEventsToMinMaxInputFields() {
    let {numberOfIndependentRows, independentMinMaxInputFields} = collectIndependentMaxMinInputFields();

    for (let item of independentMinMaxInputFields) {
        item.min.addEventListener("keyup", () => {
            computeDependentValue("min", item.min, independentMinMaxInputFields, numberOfIndependentRows);
        });
        item.max.addEventListener("keyup", () => {
            computeDependentValue("max", item.max, independentMinMaxInputFields, numberOfIndependentRows);
        });
    }
}

/**
 * The method extracts all min and max input fields except the last one as the latter will be computed dynamically in terms
 * of all the other min/max values. The number of min items always equals the number of min items. Therefore we can get the
 * total number of rows simply by extracting the tags with id ending on -min.
 */
function collectIndependentMaxMinInputFields() {
    const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

    let independentMinMaxInputFields = []
    for (let i = 0; i <= numberOfIndependentRows; i++) {
        if (i !== numberOfIndependentRows) {
            let min = document.getElementById(`all_min_max_entries-${i}-min`)
            let max = document.getElementById(`all_min_max_entries-${i}-max`)
            independentMinMaxInputFields.push({
                min: min,
                max: max
            })
        }
    }
    return {numberOfIndependentRows, independentMinMaxInputFields};
}

function computeDependentValue(type, currentInputField, independentMinMaxInputFields, numberOfIndependentRows) {
    const unfilledMinFields = independentMinMaxInputFields.filter(item => item[type].value === "");

    const moreThanTwoDigitsDotSeperated = /^\d*\.\d{3,}$/;
    const moreThanTwoDigitsColonSeperated = /^\d*\\,\d{3,}$/;

    if (moreThanTwoDigitsDotSeperated.test(currentInputField.value) || moreThanTwoDigitsColonSeperated.test(currentInputField.value)) {
        currentInputField.value = parseFloat(currentInputField.value).toFixed(2);
    }

    if (currentInputField.value < 0) {
        currentInputField.value = 0;
    }

    let sum = independentMinMaxInputFields
        .filter(item => item[type].value !== "")
        .map(item => parseFloat(item[type].value))
        .reduce((x, y) => x + y, 0);

    if (sum > 100) {
        currentInputField.value = (100 - (sum - currentInputField.value)).toFixed(2)
        sum = 100
    }
    if (unfilledMinFields.length === 0) {
        const lastMinItem = document.getElementById(`all_min_max_entries-${numberOfIndependentRows}-${type}`);
        lastMinItem.value = (100 - sum).toFixed(2)
    }
}

window.addEventListener("load", function () {
    document.getElementById("base_type").addEventListener("change", selectBaseMaterialType);
});
