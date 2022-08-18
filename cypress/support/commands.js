// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
Cypress.Commands.add("createPowders", () => {
    cy.request("GET", "http://localhost:5001/materials/base").then((response) => {
        // Cypress sets the session cookie automatically for us
        const csrfTokenStart = response.body.split('<input id="csrf_token" name="csrf_token" type="hidden" value="', 2)[1];
        const csrfToken = csrfTokenStart.split('"', 1)[0];

        cy.request({
            url: "http://localhost:5001/materials/base",
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: {
                csrf_token: csrfToken,
                material_name: "Example Powder 1",
                material_type: "Powder",
                co2_footprint: "",
                costs: "",
                delivery_time: "",
                fe3_o2: "",
                si_o2: "",
                al2_o3: "",
                ca_o: "",
                mg_o: "",
                na2_o: "",
                k2_o: "",
                s_o3: "",
                p2_o5: "",
                ti_o2: "",
                sr_o: "",
                mn2_o3: "",
                fine: "",
                gravity: "",
                submit: "6 - Save material"
            }
        });
        cy.request({
            url: "http://localhost:5001/materials/base",
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: {
                csrf_token: csrfToken,
                material_name: "Example Powder 2",
                material_type: "Powder",
                co2_footprint: "",
                costs: "",
                delivery_time: "",
                fe3_o2: "",
                si_o2: "",
                al2_o3: "",
                ca_o: "",
                mg_o: "",
                na2_o: "",
                k2_o: "",
                s_o3: "",
                p2_o5: "",
                ti_o2: "",
                sr_o: "",
                mn2_o3: "",
                fine: "",
                gravity: "",
                submit: "6 - Save material"
            }
        });
    });
});

// Needed for Cypress testing library
// https://testing-library.com/docs/cypress-testing-library/intro/
import "@testing-library/cypress/add-commands"
