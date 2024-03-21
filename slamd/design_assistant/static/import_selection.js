import { assignClickEventToMaterialTypeField } from "./material_type.js";


export function assignClickEventToImportSelectionForm() {
  const import_choices = document.querySelectorAll(".import_selection_choice");
  import_choices.forEach((import_choice) =>
    import_choice.addEventListener("click", handleImportSelection)
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
      "/design_assistant/zero_shot/import_selection",
      "material_type_container",
      import_selection
    );
    assignClickEventToMaterialTypeField();
  }, 1000);
  const import_choices = document.querySelectorAll(".import_selection_choice");
  import_choices.forEach(function (other_choice) {
    if (other_choice !== this) {
      other_choice.disabled = true;
    }
  });
}
