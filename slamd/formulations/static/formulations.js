function autocorrectWeightValue() {
    const weightConstraintInput = document.getElementById("weight_constraint");
    correctInputFieldValue(weightConstraintInput, 0);
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
});
