const WARNING_MAX_ADDITIONAL_PROPERTIES = '<p class="text-warning">You may define up to 10 additional properties</p>';
const MAX_ADDITIONAL_PROPERTIES = 10;

async function selectMaterialType(event) {
  const materialType = event.target.value;
  const url = `${BASE_MATERIALS_URL}/${materialType.toLowerCase()}`;
  await fetchDataAndEmbedTemplateInPlaceholder(url, "material-type-form-placeholder");
  document.getElementById("add-property-button").addEventListener("click", addAdditionalProperty);
  document.getElementById("delete-property-button").addEventListener("click", deleteAdditionalProperty);
}

function collectAdditionalProperties(newPropIndex) {
  const usersInputs = [];
  if (newPropIndex <= 0) {
    return usersInputs;
  }

  for (let i = 0; i < newPropIndex; i++) {
    const name = document.getElementById(`additional_properties-${i}-property_name`).value;
    const value = document.getElementById(`additional_properties-${i}-property_value`).value;
    usersInputs.push({
      property_name: name,
      property_value: value,
    });
  }
  return usersInputs;
}

async function addAdditionalProperty() {
  // Each additional property form is contained in one single div.
  // We index the additional properties starting from zero.
  const placeholder = document.getElementById("additional-properties-placeholder");
  const newPropIndex = placeholder.childElementCount;

  // Handle max number of properties and show a warning
  if (newPropIndex === MAX_ADDITIONAL_PROPERTIES) {
    placeholder.innerHTML += WARNING_MAX_ADDITIONAL_PROPERTIES;
    return;
  }

  const usersInputs = collectAdditionalProperties(newPropIndex);
  const url = `${BASE_MATERIALS_URL}/add_property`;
  await postDataAndEmbedTemplateInPlaceholder(url, "additional-properties-placeholder", usersInputs);
}

function deleteAdditionalProperty() {
  const placeholder = document.getElementById("additional-properties-placeholder");
  const newPropIndex = placeholder.childElementCount;

  // Remove the warning for the max number of properties
  if (newPropIndex === MAX_ADDITIONAL_PROPERTIES + 1) {
    placeholder.innerHTML = placeholder.innerHTML.replace(WARNING_MAX_ADDITIONAL_PROPERTIES, "");
    document.getElementById(`additional-properties-${newPropIndex - 2}-row`).remove();
    return;
  }

  // Select the row div element that contains the last entry and delete it
  if (newPropIndex > 0) {
    document.getElementById(`additional-properties-${newPropIndex - 1}-row`).remove();
  }
}

async function deleteMaterial(id, material_type) {
  deleteMaterialByType(id, material_type, false);
}

function autocorrectDeliveryTime(event) {
  correctInputFieldValue(event.target, 0);
}

window.addEventListener("load", function () {
  document.getElementById("nav-bar-base").setAttribute("class", "nav-link active");
  document.getElementById("material_name").addEventListener("keyup", toggleSubmitButtonIfInputFieldEmpty);
  document.getElementById('specific_gravity').addEventListener("keyup", toggleSubmitButtonIfInputFieldEmpty);
  document.getElementById("material_type").addEventListener("change", selectMaterialType);
  document.getElementById("add-property-button").addEventListener("click", addAdditionalProperty);
  document.getElementById("delete-property-button").addEventListener("click", deleteAdditionalProperty);
  document.getElementById("delivery_time").addEventListener("keyup", autocorrectDeliveryTime);
});
