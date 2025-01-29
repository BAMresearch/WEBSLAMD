/**
 * This file contains functions used by base_materials.js and blended_materials.js
 * The functions defined here should be general enough to be used in both cases.
 * */
const BASE_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/base`;
const BLENDED_MATERIALS_URL = `${window.location.protocol}//${window.location.host}/materials/blended`;

function toggleSubmitButtonIfInputFieldEmpty(event) {
  const material_name = document.getElementById("material_name").value
  const specific_gravity = document.getElementById("specific_gravity").value
  document.getElementById("submit").disabled = (material_name === undefined || material_name === "") || (specific_gravity  === undefined || specific_gravity === "");
}

/**
 * The id parameter corresponds to the id of the HTML <button> element. It is specified in materials_table.html
 * For consistency, it is constructed from a part describing the action, here 'delete_material_button' and a uuid
 * identifying the corresponding model object. To extract it for calling our API, we use the special delimiter.
 * The function calls the corresponding endpoint depending on whether the material is blended or not.
 *
 * @param id
 * @param material_type
 * @param isBlended
 */
async function deleteMaterialByType(id, material_type, isBlended) {
  const uuid = id.split(ACTION_BUTTON_DELIMITER)[1];
  const endpoint = isBlended ? BLENDED_MATERIALS_URL : BASE_MATERIALS_URL;
  const url = endpoint + `/${material_type.toLowerCase()}/${uuid}`;
  await deleteDataAndEmbedTemplateInPlaceholder(url, "materials-table-placeholder");
}
