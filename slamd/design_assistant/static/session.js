export async function handleDeleteDesignAssistantSession() {
  const token = document.getElementById("csrf_token").value;
  const response = await fetch("/design_assistant/delete_session", {
    method: "POST",
    headers: {
      "X-CSRF-TOKEN": token,
    },
  });
  if (response.ok) {
    window.location.reload();
  } else {
    const error = await response.text();
    document.write(error);
  }
}