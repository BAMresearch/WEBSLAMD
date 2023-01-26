document.getElementById("min_value").style.display = "none";
document.getElementById("max_value").style.display = "none";
window.addEventListener('load', function() {
  // Get the select_columns element
  var selectColumns = document.getElementById("select_columns");
  var selected_columns = new Set();
  // Add an event listener to the select_columns element
  selectColumns.addEventListener("change", function() {
    // Get the selected options
    var selectedOptions = selectColumns.selectedOptions;
    // Get the min-max container element
    var minMaxContainer = document.getElementsByClassName("min-max-container")[0];
    // Clear the min-max container
    minMaxContainer.innerHTML = "";
    // Check if any columns are selected
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

      // Loop through the selected options
      for (var i = 0; i < selectedOptions.length; i++) {
        // Get the column name
        var columnName = selectedOptions[i].value;

        // Create the min and max elements
        var minElement = document.createElement("div");
        var maxElement = document.createElement("div");

        // Add the appropriate classes to the min and max elements
        minElement.classList.add("col-4");
        maxElement.classList.add("col-4");

        // Set the innerHTML of the min and max elements
        minElement.innerHTML = '<label class="control-label">Min ' + columnName + '</label><input class="form-control" id="min_' + columnName + '" name="min_' + columnName + '" type="text">';
        maxElement.innerHTML = '<label class="control-label">Max ' + columnName + '</label><input class="form-control" id="max_' + columnName + '" name="max_' + columnName + '" type="text">';

        // Append the min and max elements to the min-max container
        minMaxContainer.appendChild(minElement);
        minMaxContainer.appendChild(maxElement);
      }
    }
  });
  console.log("Javascript is working!");
});