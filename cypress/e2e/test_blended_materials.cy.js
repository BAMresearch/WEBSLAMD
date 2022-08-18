describe("Test blended materials page", () => {
    beforeEach(() => {
        // Cypress starts out with a blank slate for each test
        // so we must tell it to visit our website with the `cy.visit()` command.
        // Since we want to visit the same URL at the start of all our tests,
        // we include it in our beforeEach function so that it runs before each test
        cy.createPowders();
        cy.visit("http://localhost:5001/materials/blended");
    });

    it("Material types are listed correctly", () => {
        cy.findByText("Powder").should("exist");
        cy.findByLabelText("2 - Material type").select("Powder");
        cy.findByLabelText("2 - Material type").select("Liquid");
        cy.findByLabelText("2 - Material type").select("Aggregates");
        cy.findByLabelText("2 - Material type").select("Admixture");
        cy.findByLabelText("2 - Material type").select("Custom");
        cy.findByLabelText("2 - Material type").select("Powder");
    });

    it("Create blended powder", () => {
        cy.findByText("Example Powder 1").should("exist");
        cy.findByText("Example Powder 2").should("exist");
    });
});
