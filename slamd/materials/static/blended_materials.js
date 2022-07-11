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
    }

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
            computeDependentMinValue(item.min, independentMinMaxInputFields, numberOfIndependentRows);
        });
        item.max.addEventListener("keyup", () => {
            computeDependentMaxValue(item.max, independentMinMaxInputFields, numberOfIndependentRows);
        });
    }
}

/**
 * The method extracts all min and max input fields except the last one as the latter will be computed dynamically in terms
 * of all the other min/max values. We number of min items always equals the number of min items. Therefore we can get the
 */
function collectIndependentMaxMinInputFields() {
    let numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

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

function computeDependentMinValue(currentInputField, independentMinMaxInputFields, numberOfIndependentRows) {
    const type = "min"
    const unfilledMinFields = independentMinMaxInputFields.filter(item => item[type].value === "");


    if (currentInputField.value < 0) {
        currentInputField.value = 0;
    }

    let sum = independentMinMaxInputFields
        .filter(item => item[type].value !== "")
        .map(item => parseFloat(item.min.value))
        .reduce((x, y) => x + y);


    if (sum > 100) {
        currentInputField.value = (100 - (sum - currentInputField.value)).toFixed(2)
        sum = 100
    }
    if (unfilledMinFields.length === 0) {
        const lastMinItem = document.getElementById(`all_min_max_entries-${numberOfIndependentRows}-${type}`);
        lastMinItem.value = (100 - sum).toFixed(2)
    }
}

function computeDependentMaxValue(currentInputField, independentMinMaxInputFields, numberOfIndependentRows) {
    const type = "max";
    const unfilledMinFields = independentMinMaxInputFields.filter(item => item[type].value === "");

    if (currentInputField.value < 0) {
        currentInputField.value = 0;
    }

    let sum = independentMinMaxInputFields
        .filter(item => item[type].value !== "")
        .map(item => parseFloat(item.max.value))
        .reduce((x, y) => x + y);

    if (sum > 100) {
        currentInputField.value = (100 - (sum - currentInputField.value)).toFixed(2)
        sum = 100
    }
    if (unfilledMinFields.length === 0) {
        const lastMaxItem = document.getElementById(`all_min_max_entries-${numberOfIndependentRows}-${type}`);
        lastMaxItem.value = (100 - sum).toFixed(2)
    }
}

window.addEventListener("load", function () {
    document.getElementById("base_type").addEventListener("change", selectBaseMaterialType);
});
