describe("Test upload dataset form", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/materials/discovery");
  });

  it("File upload works", () => {
    cy.get("input[type=file]").selectFile("examples/MaterialsDiscoveryExampleData.csv");
    cy.findByText("Upload dataset").click();
    cy.findByText("MaterialsDiscoveryExampleData.csv").should("exist");
    cy.findByText("Idx_Sample", { exact: false }).should("exist");
    cy.findByText("SiO2", { exact: false }).should("exist");
    cy.findByText("CaO", { exact: false }).should("exist");
    cy.findByText("SO3", { exact: false }).should("exist");
    cy.findByText("FA (kg/m3)", { exact: false }).should("exist");
    cy.findByText("GGBFS (kg/m3)", { exact: false }).should("exist");
    cy.findByText("Coarse aggregate (kg/m3)", { exact: false }).should("exist");
    cy.findByText("Fine aggregate (kg/m3)", { exact: false }).should("exist");
    cy.findByText("Total aggregates", { exact: false }).should("exist");
    cy.findByText("Na2SiO3", { exact: false }).should("exist");
    cy.findByText("Na2O (Dry)", { exact: false }).should("exist");
    cy.findByText("Sio2 (Dry)", { exact: false }).should("exist");
    cy.findByText("Superplasticizer", { exact: false }).should("exist");
    cy.findByText("water -eff", { exact: false }).should("exist");
    cy.findByText("Slump - Target (mm)", { exact: false }).should("exist");
    cy.findByText("CO2 (kg/t) - A-priori Information", { exact: false }).should("exist");
    cy.findByText("fc 28-d - Target (MPa)", { exact: false }).should("exist");
  });

  it("Delete dataset works", () => {
    cy.get("input[type=file]").selectFile("examples/MaterialsDiscoveryExampleData.csv");
    cy.findByText("Upload dataset").click();
    cy.get(".btn-group > div > button").eq(0).click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findAllByText("Confirm").first().click();
    cy.findByText("MaterialsDiscoveryExampleData.csv").should("not.exist");
  });

  it("Select dataset works", () => {
    cy.get("input[type=file]").selectFile("examples/MaterialsDiscoveryExampleData.csv");
    cy.findByText("Upload dataset").click();
    cy.get(".btn-group > div > a").eq(0).click();
    cy.url().should("eq", "http://localhost:5001/materials/discovery/MaterialsDiscoveryExampleData.csv");
  });
});
