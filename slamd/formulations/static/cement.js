const CEMENT_FORMULATIONS_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/formulations/cement`;
let cementWeightConstraint = "";


window.addEventListener("load", function () {
    document.getElementById("submit").disabled = false;
    document.getElementById("delete_formulations_batches_button").disabled = false;
});
