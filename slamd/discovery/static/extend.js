document.getElementById("min_value").style.display = "none";
document.getElementById("max_value").style.display = "none";
var target_columns = ["column1", "column2", "column3"];

window.addEventListener('load', function() {
  var selectColumns = document.getElementById("select_columns");
  var selected_columns = new Set();

  function removeSelectedColumns() {
    target_columns = target_columns.filter(function(column) {
      return !selected_columns.has(column);
    });
  }

  selectColumns.addEventListener("change", function() {
    var selectedOptions = selectColumns.selectedOptions;
    var minMaxContainer = document.getElementsByClassName("min-max-container")[0];
    minMaxContainer.innerHTML = "";
    selected_columns.clear();
    for (var i = 0; i < selectedOptions.length; i++) {
      selected_columns.add(selectedOptions[i].value);
    }
    removeSelectedColumns();
    var target_columns = document.getElementById("target_columns");

    for (var i = 0; i < target_columns.options.length; i++) {
        if (selected_columns.has(target_columns.options[i].value)) {
            target_columns.options[i].style.display = "none";
        } else {
            target_columns.options[i].style.display = "block";
        }
    }

    if (selectedOptions.length === 0) {
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
