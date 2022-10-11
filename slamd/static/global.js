const ACTION_BUTTON_DELIMITER = "___";
const MORE_THAN_TWO_DECIMAL_PLACES = /^\d*[.,]\d{3,}$/;
const SPINNER =
  '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';

function roundInputFieldValueToTwoDecimalPlaces(inputFieldElem) {
  if (MORE_THAN_TWO_DECIMAL_PLACES.test(inputFieldElem.value)) {
    inputFieldElem.value = parseFloat(inputFieldElem.value).toFixed(2);
  }
}

function clipMinInputFieldValue(inputFieldElem, minValue) {
  if (typeof minValue !== "number" || isNaN(minValue) || !isFinite(minValue)) {
    return;
  }
  if (parseFloat(inputFieldElem.value) < minValue) {
    inputFieldElem.value = minValue;
  }
}

function clipMaxInputFieldValue(inputFieldElem, maxValue) {
  if (typeof maxValue !== "number" || isNaN(maxValue) || !isFinite(maxValue)) {
    return;
  }
  if (parseFloat(inputFieldElem.value) > maxValue) {
    inputFieldElem.value = maxValue;
  }
}

function correctInputFieldValue(inputFieldElem, minValue, maxValue) {
  roundInputFieldValueToTwoDecimalPlaces(inputFieldElem);
  clipMinInputFieldValue(inputFieldElem, minValue);
  clipMaxInputFieldValue(inputFieldElem, maxValue);
}

function countSelectedOptionsMultipleSelectField(elem) {
  if (elem.childElementCount !== 0) {
    return Array.from(elem.children).filter((option) => option.selected).length;
  }
  return 0;
}

async function fetchDataAndEmbedTemplateInPlaceholder(url, placeholderId, append = false) {
  const response = await fetch(url);
  if (response.ok) {
    const form = await response.json();
    if (append) {
      document.getElementById(placeholderId).innerHTML += form["template"];
    } else {
      document.getElementById(placeholderId).innerHTML = form["template"];
    }
  } else {
    const error = await response.text();
    document.write(error);
  }
}

async function postDataAndEmbedTemplateInPlaceholder(url, placeholderId, body) {
  const token = document.getElementById("csrf_token").value;
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "X-CSRF-TOKEN": token,
    },
    body: JSON.stringify(body),
  });
  if (response.ok) {
    const form = await response.json();
    document.getElementById(placeholderId).innerHTML = form["template"];
  } else {
    const error = await response.text();
    document.write(error);
  }
}

async function deleteDataAndEmbedTemplateInPlaceholder(url, placeholderId) {
  const token = document.getElementById("csrf_token").value;
  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      "X-CSRF-TOKEN": token,
    },
  });
  if (response.ok) {
    const form = await response.json();
    document.getElementById(placeholderId).innerHTML = form["template"];
  } else {
    const error = await response.text();
    document.write(error);
  }
}

function removeInnerHtmlFromPlaceholder(placeholderId) {
  document.getElementById(placeholderId).innerHTML = "";
}

function insertSpinnerInPlaceholder(placeholderId, append = false) {
  if (append) {
    document.getElementById(placeholderId).innerHTML += SPINNER;
  } else {
    document.getElementById(placeholderId).innerHTML = SPINNER;
  }
}

function removeSpinnerInPlaceholder(placeholderId) {
  const placeholder = document.getElementById(placeholderId);
  placeholder.innerHTML = placeholder.innerHTML.replace(SPINNER, "");
}

function collectSelection(placeholder) {
  return Array.from(placeholder.children)
    .filter((option) => option.selected)
    .map((option) => {
      return {
        uuid: option.value,
        name: option.innerHTML,
      };
    });
}

function atLeastOneItemIsSelected(placeholder) {
  const selectedItems = Array.from(placeholder.children).filter((option) => option.selected);
  return selectedItems.length > 0;
}

function enableTooltip(elem) {
  return new bootstrap.Tooltip(elem, { trigger: "hover" });
}

/**
 * Enable tooltips everywhere
 * See Bootstrap docs: https://getbootstrap.com/docs/5.0/components/tooltips/#example-enable-tooltips-everywhere
 */
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl, { trigger: "hover" });
});

function setNavBarHomeToActive() {
  if (window.location.pathname === "/") {
    document.getElementById("nav-bar-home").setAttribute("class", "nav-link active");
  }
}

window.addEventListener("load", function () {
  setNavBarHomeToActive();
});
