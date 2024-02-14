async function selectDesignTask(userInput) {
  const url = "/design_assistant/task";
  await postDataAndEmbedTemplateInPlaceholder(
    url,
    "import_container",
    userInput
  );
}

var task_options = document.querySelectorAll('#tasks input[type="radio"]');

task_options.forEach(function (option) {
  option.addEventListener("click", function () {
    const userInput = {
      type: "design_assistant_task_selection",
      task: option.value,
    };
    selectDesignTask(userInput);
    task_options.forEach(function (otherRadio) {
      if (otherRadio !== option) {
        otherRadio.disabled = true;
      }
    });
  });
});
