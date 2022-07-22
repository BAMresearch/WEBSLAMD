const ACTION_BUTTON_DELIMITER = "___"
const MORE_THAN_TWO_DECIMAL_PLACES = /^\d*[.,]\d{3,}$/;

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

function removeInnerHtmlFromPlaceholder(placeholderID) {
    let placeholder = document.getElementById(placeholderID);
    placeholder.innerHTML = "";
}

function collectSelection(placeholder) {
    return Array.from(placeholder.children)
        .filter(option => option.selected)
        .map(option => {
            return {
                uuid: option.value,
                name: option.innerHTML
            }
        });
}
