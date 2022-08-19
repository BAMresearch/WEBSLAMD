describe("Test blending materials page", () => {
    beforeEach(() => {
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
});

describe("Test blending powders", () => {
    beforeEach(() => {
        cy.createExamplePowders();
        cy.visit("http://localhost:5001/materials/blended");
        cy.findByText("Example Powder 1").should("exist");
        cy.findByText("Example Powder 2").should("exist");
    });

    it("Create blended powder", () => {

    });
});

describe("Test blending liquids", () => {
    beforeEach(() => {
        cy.createExampleLiquids();
        cy.visit("http://localhost:5001/materials/blended");
        cy.findByLabelText("2 - Material type").select("Liquid");
        cy.findByText("Example Liquid 1").should("exist");
        cy.findByText("Example Liquid 2").should("exist");
    });

    it("Create blended liquid", () => {

    });
});

describe("Test blending aggregates", () => {
    beforeEach(() => {
        cy.createExampleAggregates();
        cy.visit("http://localhost:5001/materials/blended");
        cy.findByLabelText("2 - Material type").select("Aggregates");
        cy.findByText("Example Aggregates 1").should("exist");
        cy.findByText("Example Aggregates 2").should("exist");
    });

    it("Create blended aggregates", () => {

    });
});

describe("Test blending admixtures", () => {
    beforeEach(() => {
        cy.createExampleAdmixtures();
        cy.visit("http://localhost:5001/materials/blended");
        cy.findByLabelText("2 - Material type").select("Admixture");
        cy.findByText("Example Admixture 1").should("exist");
        cy.findByText("Example Admixture 2").should("exist");
    });

    it("Create blended admixture", () => {

    });
});

