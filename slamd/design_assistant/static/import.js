document
  .querySelector("#import_selection_container")
  .addEventListener("click", async function (e) {
    // Check if the clicked element is a list item
    if (e.target && e.target.nodeName === "INPUT") {
      console.log(e.target.value);
      let import_selection
      if (import_selection === 'No') {
        await postDataAndEmbedTemplateInPlaceholder("/design_assistant/import_selection", "campaign_container", 'no_import');
      } else {
        // implement here the logic for when user wants to import dataset, for now we always go with no import
        await postDataAndEmbedTemplateInPlaceholder("/design_assistant/import_selection", "campaign_container", 'no_import');
      }
    }
  });
