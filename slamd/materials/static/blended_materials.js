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
    elem = document.getElementById("confirm_blending_configuration_button");

    elem.addEventListener("click", () => {
        const numberOfIndependentRows = document.querySelectorAll('[id$="-min"]').length - 1;

        let minMaxValuesWithIncrements = []
        for (let i = 0; i <= numberOfIndependentRows; i++) {
            let min = document.getElementById(`all_min_max_entries-${i}-min`)
            let max = document.getElementById(`all_min_max_entries-${i}-max`)
            let increment = document.getElementById(`all_min_max_entries-${i}-increment`)
            minMaxValuesWithIncrements.push({
                idx: i,
                min: min,
                max: max,
                increment: increment
            })
        }
        createRatios(minMaxValuesWithIncrements);

    })

}

function createRatios(minMaxValuesWithIncrements) {

    let allValues = []
    for (let i = 0; i < minMaxValuesWithIncrements.length - 1; i++) {
        let valuesForGivenMaterial = [];
        let current = parseFloat(minMaxValuesWithIncrements[i].min.value)
        let max = parseFloat(minMaxValuesWithIncrements[i].max.value)
        let increment = parseFloat(minMaxValuesWithIncrements[i].increment.value)
        while (current <= max) {
            valuesForGivenMaterial.push(current)
            current += increment
        }
        allValues.push(valuesForGivenMaterial)
    }
    let blending_ratios = document.getElementById("blending_ratio_placeholder")
    if (allValues.length === 1) {
        for (let item of allValues[0]) {
            const remainder = 100 - item
            blending_ratios.innerHTML += `${item}/${remainder} `
        }
    } else {
        const cartesian =
            (...a) => a.reduce((a, b) => a.flatMap(d => b.map(e => [d, e].flat())));


        let result = cartesian(allValues[0], allValues[1])


        for (let ratio of cartesian(allValues)) {
            blending_ratios.innerHTML += ratio + "\n"
        }
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
            computeDependentValue("min", item.min, independentMinMaxInputFields, numberOfIndependentRows);
        });
        item.max.addEventListener("keyup", () => {
            computeDependentValue("max", item.max, independentMinMaxInputFields, numberOfIndependentRows);
        });
    }
}

/**
 * The method extracts all min and max input fields except the last one as the latter will be computed dynamically in terms
 * of all the other min/max values. We number of min items always equals the number of min items. Therefore we can get the
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
