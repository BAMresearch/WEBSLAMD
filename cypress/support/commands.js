// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
Cypress.Commands.add("createBaseMaterial", (fixtureFilename, csrfToken) => {
    cy.fixture(fixtureFilename).then((materialData) => {
        // Add the CSRF Token, otherwise we get a 400 Bad Request from the backend.
        materialData.csrf_token = csrfToken;
        cy.request({
            url: "http://localhost:5001/materials/base",
            method: "POST",
            headers: {
                // This is the smallest set of headers we need for the request to work.
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: materialData
        });
    });
});

Cypress.Commands.add("createPowders", () => {
    cy.request("GET", "http://localhost:5001/materials/base").then((response) => {
        // Cypress sets the session cookie automatically for us
        const csrfTokenStart = response.body.split('<input id="csrf_token" name="csrf_token" type="hidden" value="', 2)[1];
        const csrfToken = csrfTokenStart.split('"', 1)[0];

        cy.createBaseMaterial("example_powder_1", csrfToken);
        cy.createBaseMaterial("example_powder_2", csrfToken);
    });
});


// Needed for Cypress testing library
// https://testing-library.com/docs/cypress-testing-library/intro/
import "@testing-library/cypress/add-commands"
