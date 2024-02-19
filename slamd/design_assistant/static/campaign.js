document
  .querySelector("#material_type_container")
  .addEventListener("click", async function (e) {
    if (e.target && e.target.nodeName === "INPUT") {
      await postDataAndEmbedTemplateInPlaceholder(
        "/design_assistant/material",
        "design_targets_container",
        e.target.value
      );
    }
    const material_choices = document.querySelectorAll(
      '#material_type_container input[type="radio"]'
    );
    material_choices.forEach(function (choice) {
      if (!(choice.value == e.target.value)) {
        choice.disabled = true;
      }
    });
  });
