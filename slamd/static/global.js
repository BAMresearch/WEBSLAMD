async function fetchEmbedTemplateInPlaceholder(url, placeholderID, append = false) {
    const response = await fetch(url);
    if (response.ok) {
        const form = await response.json();
        if (append) {
            document.getElementById(placeholderID).innerHTML += form["template"];
        } else {
            document.getElementById(placeholderID).innerHTML = form["template"];
        }
    } else {
        const error = await response.text()
        document.write(error)
    }
}

async function postDataAndEmbedTemplateInPlaceholder(url, placeholderID, body) {
    const token = document.getElementById("csrf_token").value
    const response = await fetch(url, {
        method: "POST",
        headers: {
            'X-CSRF-TOKEN': token
        },
        body: JSON.stringify(body)
    });
    if (response.ok) {
        const form = await response.json();
        document.getElementById(placeholderID).innerHTML = form["template"];
    } else {
        const error = await response.text()
        document.write(error);
    }
}
