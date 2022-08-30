const TARGET_BASE_URL = `${window.location.protocol}//${window.location.host}/materials/discovery`;

async function addTarget() {
    const targetName = document.getElementById("target_value").value;
    const dataset = document.getElementById("dataset_to_add_targets_to").innerHTML
    const url = `${TARGET_BASE_URL}/${dataset}/${targetName}/add_target`;

    await fetchDataAndEmbedTemplateInPlaceholder(url, "targets-placeholder");
    // TODO: event listener für inputs?
}

function toggleDataframe() {
    let dataframeTable = document.getElementById("formulations_dataframe");
    if (dataframeTable.style.visibility === "collapse"){
        dataframeTable.style.visibility = "visible"
    }
    else {
        dataframeTable.style.visibility = "collapse"
    }
}

window.addEventListener("load", function () {
    document.getElementById("add_target_button").addEventListener("click", addTarget);
    document.getElementById("toggle_dataframe_button").addEventListener("click", toggleDataframe);
});
