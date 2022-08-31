describe("Test materials formulations form", () => {
  beforeEach(() => {
    cy.createExamplePowders();
    cy.createExampleLiquids();
    cy.createExampleAggregates();
    cy.visit("http://localhost:5001/materials/formulations");
    cy.findByText("Example Powder 1").should("exist");
    cy.findByText("Example Powder 2").should("exist");
    cy.findByText("Example Liquid 1").should("exist");
    cy.findByText("Example Liquid 2").should("exist");
    cy.findByText("Example Aggregates 1").should("exist");
    cy.findByText("Example Aggregates 2").should("exist");
  });

  it("Confirm selection works", () => {});
});
