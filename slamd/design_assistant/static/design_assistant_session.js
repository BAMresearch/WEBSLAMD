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

export async function handleUploadDesignAssistantSession() {
    const token = document.getElementById("csrf_token").value;
    const selectedFile = document.getElementById("da-button-upload").files[0];
    const submitURL = `${window.location.protocol}//${window.location.host}/design_assistant/upload`;
    const formData = new FormData();
    formData.append("file", selectedFile);
    const response = await fetch(submitURL, {
        method: "POST",
        body: formData,
        files: selectedFile,
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

export function passClickToDAFileInput() {
    document.getElementById("da-button-upload").click();
}