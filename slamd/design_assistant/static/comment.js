export function assignInputEventToCommentForm() {
  const comment_input = document.getElementById("comment");
  if (comment_input) {
    comment_input.addEventListener("input", handleCommentInput);
  }
}

function handleCommentInput(event) {
  const comment_input = document.getElementById("comment");
  const submit_comment_button = document.getElementById(
      "submit_comment_button"
  );
  comment_input.value = event.target.value;
  if (comment_input.value) {
    submit_comment_button.disabled = false;
  }
}

export async function handleCommentSubmission() {
  const comment_input = document.getElementById("comment");
  comment_input.disabled = "true";
  const submit_comment_button = document.getElementById(
      "submit_comment_button"
  );
  submit_comment_button.disabled = "true";
  insertSpinnerInPlaceholder(
      "knowledge_container",
      true,
      CHATBOT_RESPONSE_SPINNER
  );
  setTimeout(async function handleSubmission() {
    await postDataAndEmbedTemplateInPlaceholder(
        "/design_assistant/zero_shot/comment",
        "knowledge_container",
        comment_input.value
    );
  }, 1000);
}