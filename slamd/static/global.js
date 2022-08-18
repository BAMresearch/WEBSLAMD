const ACTION_BUTTON_DELIMITER = "___"
const MORE_THAN_TWO_DECIMAL_PLACES = /^\d*[.,]\d{3,}$/;

async function fetchDataAndEmbedTemplateInPlaceholder(url, placeholderID, append = false) {
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

async function deleteDataAndEmbedTemplateInPlaceholder(url, placeholderID) {
    const token = document.getElementById("csrf_token").value
    const response = await fetch(url, {
        method: "DELETE",
        headers: {
            'X-CSRF-TOKEN': token
        },
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

function fixInputValue(currentInputField) {
    if (MORE_THAN_TWO_DECIMAL_PLACES.test(currentInputField.value)) {
        currentInputField.value = parseFloat(currentInputField.value).toFixed(2);
    }

    if (currentInputField.value < 0) {
        currentInputField.value = 0;
    }
}

/**
 * Enable tooltips everywhere
 * See Bootstrap docs: https://getbootstrap.com/docs/5.0/components/tooltips/#example-enable-tooltips-everywhere
 */
 const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
 const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
   return new bootstrap.Tooltip(tooltipTriggerEl)
 })