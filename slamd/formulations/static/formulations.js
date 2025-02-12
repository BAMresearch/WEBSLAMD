function autocorrectWeightValue() {
    const weightConstraintInput = document.getElementById("weight_constraint");
    correctInputFieldValue(weightConstraintInput, 0);
}

function updateConstraintLabel(){
    const constraintLabel = document.getElementById("constraint_input_label")
    const constraintValue = document.getElementById("weight_constraint")
    if (this.value === 'Weight') {
        constraintLabel.textContent = constraintLabel.textContent.replace('Volume (m³)', 'Weight (kg)')
        constraintValue.value = 2400.0
    } else {
        constraintLabel.textContent = constraintLabel.textContent.replace('Weight (kg)', 'Volume (m³)')
        constraintValue.value = 1.0
    }
}

window.addEventListener("load", function () {
    document.getElementById("weight_constraint").addEventListener("keyup", autocorrectWeightValue);

    if (window.location.pathname.includes('concrete')) {
        document.getElementById("nav-bar-formulations-concrete").setAttribute("class", "nav-link active");
        document.getElementById("nav-bar-formulations-binder").setAttribute("class", "nav-link");
    } else {
        document.getElementById("nav-bar-formulations-concrete").setAttribute("class", "nav-link");
        document.getElementById("nav-bar-formulations-binder").setAttribute("class", "nav-link active");
    }

    document.getElementById("nav-bar-formulations").setAttribute("class", "nav-link active");
    document.getElementById("constraint_selection").addEventListener("change", updateConstraintLabel)
});
