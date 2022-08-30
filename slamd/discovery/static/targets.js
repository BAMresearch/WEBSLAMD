const TARGET_BASE_URL = `${window.location.protocol}//${window.location.host}/materials/discovery`;

async function addTarget() {
  const targetName = document.getElementById("target_value").value;
  const dataset = document.getElementById("dataset_to_add_targets_to").innerHTML;
  const url = `${TARGET_BASE_URL}/${dataset}/${targetName}/add_target`;

  await fetchDataAndEmbedTemplateInPlaceholder(url, "targets-placeholder");
}

function toggleShowHideDataframe() {
  const dataframeTable = document.getElementById("formulations_dataframe");
  dataframeTable.classList.toggle("df-collapsed");
}

window.addEventListener("load", function () {
  document.getElementById("nav-bar-discovery").setAttribute("class", "nav-link active");
  document.getElementById("add_target_button").addEventListener("click", addTarget);
  document.getElementById("toggle_dataframe_button").addEventListener("click", toggleShowHideDataframe);
});
