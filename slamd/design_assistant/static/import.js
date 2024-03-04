import { assignClickEventToMaterialTypeField } from "./material_type.js";

export function assignClickEventToImportForm() {
  const import_options = document.querySelectorAll(".import_selection_option");
  import_options.forEach((import_option) =>
    import_option.addEventListener("click", handleImportSelection)
  );
}

async function handleImportSelection(event) {
  const import_selection = event.target.value;
  insertSpinnerInPlaceholder(
    "material_type_container",
    true,
    CHATBOT_RESPONSE_SPINNER
  );
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
      "/design_assistant/import_selection",
      "material_type_container",
      import_selection
    );
    assignClickEventToMaterialTypeField();
  }, 1000);
  const import_options = document.querySelectorAll(".import_selection_option");
  import_options.forEach(function (other_option) {
    if (other_option !== this) {
      other_option.disabled = true;
    }
  });
}
