document.getElementById("min_value").style.display = "none";
document.getElementById("max_value").style.display = "none";
window.addEventListener('load', function() {
  var selectColumns = document.getElementById("select_columns");
  var selected_columns = new Set();
  selectColumns.addEventListener("change", function() {
    var selectedOptions = selectColumns.selectedOptions;
    var minMaxContainer = document.getElementsByClassName("min-max-container")[0];
    minMaxContainer.innerHTML = "";
    if (selectedOptions.length == 0) {
        var minValue = document.getElementById("min_value");
        var maxValue = document.getElementById("max_value");
        if (minValue) minValue.style.display = "none";
        if (maxValue) maxValue.style.display = "none";
    } else {
        var minValue = document.getElementById("min_value");
        var maxValue = document.getElementById("max_value");
        if (minValue) minValue.style.display = "block";
        if (maxValue) maxValue.style.display = "block";
      for (var i = 0; i < selectedOptions.length; i++) {
        var columnName = selectedOptions[i].value;
        var minElement = document.createElement("div");
        var maxElement = document.createElement("div");
        var row = document.createElement("div");
        minElement.classList.add("col-6");
        maxElement.classList.add("col-6");
        row.classList.add("row");
        minElement.innerHTML = '<label class="control-label">Min ' + columnName + '</label><input class="form-control" id="min_' + columnName + '" name="min_' + columnName + '" type="text">';
        maxElement.innerHTML = '<label class="control-label">Max ' + columnName + '</label><input class="form-control" id="max_' + columnName + '" name="max_' + columnName + '" type="text">';
        row.appendChild(minElement);
        row.appendChild(maxElement);
        minMaxContainer.appendChild(row);
      }
    }
  });
  console.log("Javascript is working!");
});
