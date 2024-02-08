async function selectDesignTask(userInput) {
  const url = "/design_assistant/select_task";
  await postDataAndEmbedTemplateInPlaceholder(
    url,
    "design_assistant_task",
    userInput
  );
}

var task_options = document.querySelectorAll(
  '#design_assistant_task input[type="radio"]'
);

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
