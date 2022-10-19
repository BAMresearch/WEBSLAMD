// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands

// Needed for Cypress testing library
// https://testing-library.com/docs/cypress-testing-library/intro/
import "@testing-library/cypress/add-commands";

Cypress.Commands.add("getCsrfToken", () => {
  cy.request("GET", "http://localhost:5001/materials/base").then((response) => {
    // Cypress sets the session cookie automatically for us
    // We need to parse the CSRF Token ourselves
    const csrfTokenStart = response.body.split('<input id="csrf_token" name="csrf_token" type="hidden" value="', 2)[1];
    const csrfToken = csrfTokenStart.split('"', 1)[0];
    // Yield the csrfToken to the next command
    cy.wrap(csrfToken);
  });
});

Cypress.Commands.add("createBaseMaterial", (fixtureFilename, csrfToken) => {
  cy.fixture(fixtureFilename).then((materialData) => {
    // Add the CSRF Token, otherwise we get a 400 Bad Request from the backend
    materialData.csrf_token = csrfToken;
    cy.request({
      url: "http://localhost:5001/materials/base",
      method: "POST",
      headers: {
        // This is the smallest set of headers we need for the request to work
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: materialData,
    });
  });
});

Cypress.Commands.add("createExamplePowders", () => {
  cy.getCsrfToken().then((csrfToken) => {
    cy.createBaseMaterial("example_powder_1", csrfToken);
    cy.createBaseMaterial("example_powder_2", csrfToken);
  });
});

Cypress.Commands.add("createExampleLiquids", () => {
  cy.getCsrfToken().then((csrfToken) => {
    cy.createBaseMaterial("example_liquid_1", csrfToken);
    cy.createBaseMaterial("example_liquid_2", csrfToken);
  });
});

Cypress.Commands.add("createExampleAggregates", () => {
  cy.getCsrfToken().then((csrfToken) => {
    cy.createBaseMaterial("example_aggregates_1", csrfToken);
    cy.createBaseMaterial("example_aggregates_2", csrfToken);
  });
});

Cypress.Commands.add("createExampleCustomMaterials", () => {
  cy.getCsrfToken().then((csrfToken) => {
    cy.createBaseMaterial("example_custom_1", csrfToken);
    cy.createBaseMaterial("example_custom_2", csrfToken);
    cy.createBaseMaterial("example_custom_3", csrfToken);
  });
});

Cypress.Commands.add("createExampleAdmixtures", () => {
  cy.getCsrfToken().then((csrfToken) => {
    cy.createBaseMaterial("example_admixture_1", csrfToken);
    cy.createBaseMaterial("example_admixture_2", csrfToken);
    cy.createBaseMaterial("example_admixture_3", csrfToken);
  });
});

Cypress.Commands.add("createExampleProcesses", () => {
  cy.getCsrfToken().then((csrfToken) => {
    cy.createBaseMaterial("example_process_1", csrfToken);
    cy.createBaseMaterial("example_process_2", csrfToken);
  });
});

Cypress.Commands.add("expectFloatToEqual", { prevSubject: true }, (subject, expectedValue) => {
  // Compare the float values using an epsilon to prevent errors due to rounding
  expect(parseFloat(subject.text().replace(",", "."))).to.be.closeTo(expectedValue, 0.000002);
  // Yield the DOM element to the next command
  cy.wrap(subject);
});

Cypress.Commands.add("clickButtonWaitForAsyncRequest", (buttonText, endpoint) => {
  cy.intercept(endpoint).as(endpoint);
  cy.findAllByText(buttonText).filter(':visible').click();
  cy.wait(`@${endpoint}`);
});

Cypress.Commands.add("fillForm", (formContent) => {
  // Receive the form content as an object of the form:
  // { labelText1: inputValue1, labelText2: inputValue2, ...}
  // If inputValue is an array, the label is interpreted as appearing several times on the page,
  // then for every occurrence it fills out the input field with the n-th value of the array.
  for (const [labelText, inputValue] of Object.entries(formContent)) {
    if (Array.isArray(inputValue)) {
      cy.fillRepeatedFormElement(labelText, inputValue);
    } else {
      cy.findByLabelText(labelText).type(inputValue).should("have.value", inputValue);
    }
  }
});

Cypress.Commands.add("fillRepeatedFormElement", (labelText, inputValues) => {
  // Fill for every appearance of labelText one value from the inputValues array.
  for (const [index, inputValue] of inputValues.entries()) {
    cy.findAllByLabelText(labelText).eq(index).type(inputValue).should("have.value", inputValue);
  }
});

Cypress.Commands.add("selectInputWaitForAsyncRequest", (selectInputLabelText, option, endpoint) => {
  cy.intercept(endpoint).as(endpoint);
  cy.findByLabelText(selectInputLabelText).select(option);
  cy.wait(`@${endpoint}`);
});

Cypress.Commands.add("checkGeneratedConfigurations", (confArray) => {
  // Check that each element of confArray appears only once as the display value of an input field.
  for (const conf of confArray) {
    cy.findByDisplayValue(conf).should("exist");
  }
});

Cypress.Commands.add("checkGeneratedContent", (textsToCheck, exactMatch = false) => {
  // Check that each element of textsToCheck appears only once.
  for (const text of textsToCheck) {
    cy.findByText(text, { exact: exactMatch }).should("exist");
  }
});

Cypress.Commands.add("checkGeneratedTable", (tableContent) => {
  // Receive the table content as a two-dimensional array of the form:
  // [ [col1, col2, col3, ...], [col1, col2, col3, ...], [col1, col2, col3, ...], ... ]
  for (let rowIndex = 0; rowIndex < tableContent.length; ++rowIndex) {
    for (let colIndex = 0; colIndex < tableContent[rowIndex].length; ++colIndex) {
      // Skip the header, add one to the rowIndex
      cy.get("tr")
        .eq(rowIndex + 1)
        .children()
        .eq(colIndex)
        .expectFloatToEqual(tableContent[rowIndex][colIndex]);
    }
  }
});
