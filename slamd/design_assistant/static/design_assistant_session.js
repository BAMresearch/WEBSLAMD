export async function handleDeleteDesignAssistantSession() {
    const token = document.getElementById("csrf_token").value;
    const response = await fetch("/design_assistant/session", {
        method: "DELETE",
        headers: {
            "X-CSRF-TOKEN": token,
            'Content-Type': 'application/json'
        },
    });
    if (response.ok) {
        window.location.reload();
    } else {
        const error = await response.text();
        document.write(error);
    }
}