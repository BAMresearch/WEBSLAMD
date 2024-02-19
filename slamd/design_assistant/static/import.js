document
  .querySelector("#import_selection_container")
  .addEventListener("click", async function (e) {
    // Check if the clicked element is a list item
    let import_selection;
    if (e.target && e.target.nodeName === "INPUT") {
      import_selection = e.target.value;
      if (import_selection === "No") {
        await postDataAndEmbedTemplateInPlaceholder(
          "/design_assistant/import_selection",
          "material_type_container",
          "no_import"
        );
      } else {
        // implement here the logic for when user wants to import dataset, for now we always go with no import
        await postDataAndEmbedTemplateInPlaceholder(
          "/design_assistant/import_selection",
          "material_type_container",
          "no_import"
        );
      }
    }
    const import_choices = document.querySelectorAll(
      '#import_selection_container input[type="radio"]'
    );
    import_choices.forEach(function (choice) {
      if (!(choice.value == import_selection)) {
        choice.disabled = true;
      }
    });
  });
