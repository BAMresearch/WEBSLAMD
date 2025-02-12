const CONCRETE_FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations/concrete`;
let concreteWeightConstraint = "";
let materialsSpecificGravity = {}

/**
 * Despite the fact that some functions in binder.js and concrete.js look rather similar, we choose not to
 * extract too many common methods as the internal logic for the two cases might diverge. In order not to create
 * too much coupling between usecase which are different we explicitly prefer duplicating some parts of the code here.
 */
function toggleBasedOnSelectionAndConstraints() {
    const powderPlaceholder = document.getElementById("powder_selection");
    const liquidPlaceholder = document.getElementById("liquid_selection");
    const aggregatesPlaceholder = document.getElementById("aggregates_selection");
    concreteWeightConstraint = document.getElementById("weight_constraint").value;


    const powderSelected = atLeastOneItemIsSelected(powderPlaceholder);
    const liquidSelected = atLeastOneItemIsSelected(liquidPlaceholder);
    const aggregatesSelected = atLeastOneItemIsSelected(aggregatesPlaceholder);

    const validSelectionConfiguration = powderSelected && liquidSelected && aggregatesSelected;
    const validConstraintConfiguration = concreteWeightConstraint !== undefined && concreteWeightConstraint !== "" &&
        concreteWeightConstraint > 0;

    const changeSelectionButton = document.getElementById("change_materials_and_processes_selection_button");
    changeSelectionButton.disabled = !(validSelectionConfiguration && validConstraintConfiguration);
}

function toggleSelectionConfirmationButtonAfterConstraintChange() {
    concreteWeightConstraint = document.getElementById("weight_constraint").value;
    toggleBasedOnSelectionAndConstraints();
}

async function confirmSelection() {
    removeInnerHtmlFromPlaceholder("formulations_min_max_placeholder");
    removeInnerHtmlFromPlaceholder("formulations_weights_placeholder");
    document.getElementById("submit").disabled = true;
    concreteWeightConstraint = document.getElementById("weight_constraint").value;
    const selectedMaterials = collectBuildingMaterialFormulationSelection();
    const selectedConstraintType = document.getElementById("constraint_selection").value;
    const url = `${CONCRETE_FORMULATIONS_MATERIALS_URL}/add_min_max_entries`;

    body = {
        "selectedMaterials" : selectedMaterials,
        "selectedConstraintType" : selectedConstraintType
    }

    insertSpinnerInPlaceholder("formulations_min_max_placeholder");
    await postDataAndEmbedTemplateInPlaceholder(url, "formulations_min_max_placeholder", body);
    removeSpinnerInPlaceholder("formulations_min_max_placeholder");

    addListenersToIndependentFields(CONCRETE);
    assignConfirmFormulationsConfigurationEvent();
    getSpecificGravityOfMaterials();
}

async function assignConfirmFormulationsConfigurationEvent() {
    const button = document.getElementById("confirm_formulations_configuration_button");
    enableTooltip(button);

    button.addEventListener("click", async () => {
        const requestData = collectFormulationsMinMaxRequestData(CONCRETE);
        const url = `${CONCRETE_FORMULATIONS_MATERIALS_URL}/create_formulations_batch`;
        const token = document.getElementById("csrf_token").value;
        const constraintType = document.getElementById('constraint_selection')
        const processesRequestData = collectProcessesRequestData();
        requestData['selectedConstraintType'] = constraintType.value
        requestData['processesRequestData'] = processesRequestData
        requestData['samplingSize'] = 1
        console.log(requestData)
        let response = await fetch(url, {
            method: "POST",
            headers: {
                "X-CSRF-TOKEN": token,
            },
            body: JSON.stringify(requestData),
        });

        response = await response.json()
        console.log(response)
        // insertSpinnerInPlaceholder("formulations_weights_placeholder");
        // await postDataAndEmbedTemplateInPlaceholder(url, "formulations_weights_placeholder", requestData);
        // removeSpinnerInPlaceholder("formulations_weights_placeholder");
        // assignKeyboardEventsToWeightForm(true);
        // assignDeleteWeightEvent();
        // assignCreateFormulationsBatchEvent(`${CONCRETE_FORMULATIONS_MATERIALS_URL}/create_formulations_batch`);
    });
}


async function getSpecificGravityOfMaterials(){
    const materialsUuidDict = buildMaterialsUuidDict();
    const token = document.getElementById("csrf_token").value;
    const url = `${CONCRETE_FORMULATIONS_MATERIALS_URL}/get_specific_gravity`
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRF-TOKEN": token,
        },
        body: JSON.stringify(materialsUuidDict),
    });

    materialsSpecificGravity = await response.json()
}

function buildMaterialsUuidDict(){
    let materialsDict = {};
    document.querySelectorAll('.row.g-3.mb-3.align-items-end').forEach(row => {
        let uuidField = row.previousElementSibling?.querySelector('.uuid-field');
        let materialField = row.querySelector('[name$="materials_entry_name"]');

        if (uuidField && materialField) {
            let uuid = uuidField.value.trim();
            let materialName = materialField.value.trim();

            if (uuid && materialName) {

                let categoryMatch = materialName.match(/^([\w\s]+)\s*\(/);
                let category = categoryMatch ? categoryMatch[1].trim() : materialName;

                if (category === 'W/C Ratio'){
                    category = 'Liquid'
                }
                if (category === 'Powders'){
                    category = 'Powder'
                }
                if (category === 'Admixtures'){
                    category = 'Admixture'
                }
                if (category === 'Air Pore Content'){
                    return
                }
                if (!materialsDict[category]) {
                    materialsDict[category] = [];
                }
                uuid.split(',').forEach(singleUuid => {
                    materialsDict[category].push(singleUuid.trim());
                });
            }
        }
    });
    return materialsDict
}

async function deleteFormulations() {
    await deleteDataAndEmbedTemplateInPlaceholder(CONCRETE_FORMULATIONS_MATERIALS_URL, "formulations-table-placeholder");
    document.getElementById("submit").disabled = true;
    document.getElementById("delete_formulations_batches_button").disabled = true;
    // Tooltip needs to be hidden manually to avoid a bug with chrome
    bootstrap.Tooltip.getInstance("#delete_formulations_batches_button").hide()
}

window.addEventListener("load", function () {
    document.getElementById("confirm_materials_and_processes_selection_button").addEventListener("click", confirmSelection);
    document.getElementById("weight_constraint").addEventListener("keyup", toggleSelectionConfirmationButtonAfterConstraintChange);
    document.getElementById("powder_selection").addEventListener("change", toggleBasedOnSelectionAndConstraints);
    document.getElementById("liquid_selection").addEventListener("change", toggleBasedOnSelectionAndConstraints);
    document.getElementById("aggregates_selection").addEventListener("change", toggleBasedOnSelectionAndConstraints);
    document.getElementById("delete_formulations_batches_button").addEventListener("click", deleteFormulations);

    const formulations = document.getElementById("formulations_dataframe");
    if (formulations) {
        document.getElementById("submit").disabled = false;
        document.getElementById("delete_formulations_batches_button").disabled = false;
    }
});
