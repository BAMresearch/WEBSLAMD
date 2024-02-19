async function selectDesignTask(task) {
  const url = "/design_assistant/task";
  await postDataAndEmbedTemplateInPlaceholder(
    url,
    "import_selection_container",
    task
  );
}

const task_options = document.querySelectorAll('#tasks input[type="radio"]');


task_options.forEach(function (option) {
  option.addEventListener("click", function () {
    let task;
    if (option.value === "Zero shot predictions using LLMs") {
      task = "zero_shot_learner";
    } else {
      task = "data_creation";
    }
    selectDesignTask(task);
    task_options.forEach(function (otherRadio) {
      if (otherRadio !== option) {
        otherRadio.disabled = true;
      }
    });
  });
});
