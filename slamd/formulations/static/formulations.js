window.addEventListener("load", function () {
    if (window.location.pathname.includes('concrete')) {
        document.getElementById("nav-bar-formulations-concrete").setAttribute("class", "nav-link active");
        document.getElementById("nav-bar-formulations-cement").setAttribute("class", "nav-link");
    } else {
        document.getElementById("nav-bar-formulations-concrete").setAttribute("class", "nav-link");
        document.getElementById("nav-bar-formulations-cement").setAttribute("class", "nav-link active");
    }

    document.getElementById("nav-bar-formulations").setAttribute("class", "nav-link active");
});
