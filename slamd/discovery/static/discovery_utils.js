function getMaxMinValue(maxCheckboxId, minCheckboxId) {
    const maxCheckboxElem = document.getElementById(maxCheckboxId);
    const minCheckboxElem = document.getElementById(minCheckboxId);

    if (maxCheckboxElem.checked) {
        return maxCheckboxElem.value;
    } else if (minCheckboxElem.checked) {
        return minCheckboxElem.value;
    } else {
        throw "Invalid state";
    }
}

function filterUnselectedOptionsAndAssignToSelectElement(options, selectorElementID) {
    let options_not_selected = "";

    for (const option of options) {
        if (!option.selected) {
            options_not_selected += `<option value="${option.value}">${option.value}</option>`;
        }
    }

    document.getElementById(selectorElementID).innerHTML = options_not_selected;
}

function collectSelectedValues(options) {
    const values = [];
    for (const option of options) {
        if (option.selected) {
            values.push(option.value);
        }
    }
    return values;
}

function parseTargetConfigurations(numberTargetProperties) {
    const result = [];
    for (let i = 0; i < numberTargetProperties; ++i) {
        const max_or_min = getMaxMinValue(
            `target_configurations-${i}-max_or_min-0`,
            `target_configurations-${i}-max_or_min-1`
        );
        const weight = document.getElementById(`target_configurations-${i}-weight`).value;
        const threshold = document.getElementById(`target_configurations-${i}-threshold`).value;
        result.push({max_or_min, weight, threshold});
    }
    return result;
}

function parseAPrioriInformationConfigurations(numberAPrioriInformationProperties) {
    const result = [];
    for (let i = 0; i < numberAPrioriInformationProperties; ++i) {
        const max_or_min = getMaxMinValue(
            `a_priori_information_configurations-${i}-max_or_min-0`,
            `a_priori_information_configurations-${i}-max_or_min-1`
        );
        const weight = document.getElementById(`a_priori_information_configurations-${i}-weight`).value;
        const threshold = document.getElementById(`a_priori_information_configurations-${i}-threshold`).value;
        result.push({max_or_min, weight, threshold});
    }
    return result;
}

function createRunExperimentRequest() {
    const materials_data_input = collectSelectedValues(document.getElementById("materials_data_input").options);
    const target_properties = collectSelectedValues(document.getElementById("target_properties").options);
    const a_priori_information = collectSelectedValues(document.getElementById("a_priori_information").options);
    const model = collectSelectedValues(document.getElementById("model").options);
    const curiosity = document.getElementById("curiosity").value;
    const target_configurations = parseTargetConfigurations(target_properties.length);
    const a_priori_information_configurations = parseAPrioriInformationConfigurations(a_priori_information.length);

    return {
        materials_data_input,
        target_properties,
        a_priori_information,
        model: model[0],
        curiosity,
        target_configurations,
        a_priori_information_configurations,
    };
}

function plotJsonDataInPlaceholder(placeholderId) {
    const plotJson = JSON.parse(document.getElementById(placeholderId).textContent);
    removeInnerHtmlFromPlaceholder(placeholderId);
    Plotly.plot(placeholderId, plotJson.data, plotJson.layout, {responsive: true});
}
