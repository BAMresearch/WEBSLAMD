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
        cy.findByLabelText("1 - Name").type("Example Blended Powder");
        cy.findByLabelText("2 - Material type").select("Powder");
        cy.findByLabelText("3 - Base materials").select(["Example Powder 1", "Example Powder 2"]);
        cy.findByText("4 - Confirm Selection").click();
        // Wait for the modal animation to finish
        cy.wait(400);
        cy.findByText("Change Selection").should("exist");
        cy.findByText("Do you really want to change the chosen selection?").should("exist");
        cy.findByText("Close").should("exist");
        cy.findByText("Confirm").click();

        // Fill in the increment, min, max values
        cy.findAllByLabelText("Increment (%)").first().type(10);
        cy.findAllByLabelText("Min (%)").first().type(0);
        cy.findAllByLabelText("Max (%)").first().type(100);
        // Check the autocompletion feature
        cy.findAllByLabelText("Min (%)").last().should("have.value", "100.00");
        cy.findAllByLabelText("Max (%)").last().should("have.value", "0.00");
        cy.findByText("5 - Confirm configuration").click().scrollIntoView();

        // Check that the configurations were generated correctly
        cy.findByDisplayValue("0/100").should("exist");
        cy.findByDisplayValue("10/90").should("exist");
        cy.findByDisplayValue("20/80").should("exist");
        cy.findByDisplayValue("30/70").should("exist");
        cy.findByDisplayValue("40/60").should("exist");
        cy.findByDisplayValue("50/50").should("exist");
        cy.findByDisplayValue("60/40").should("exist");
        cy.findByDisplayValue("70/30").should("exist");
        cy.findByDisplayValue("80/20").should("exist");
        cy.findByDisplayValue("90/10").should("exist");
        cy.findByDisplayValue("100/0").should("exist");

        // Delete the last two blends and add them again
        cy.findByText("Delete blend").click().click();
        cy.findByText("Add blend").click().click();
        cy.get('input[id="all_ratio_entries-9-ratio"]').type("90/10");
        cy.get('input[id="all_ratio_entries-10-ratio"]').type("100/0");
        cy.findByText("6 - Create blended materials").click();

        // Check that the blended powders were generated correctly
        cy.findByText("All blended materials").scrollIntoView();
        cy.findByText("Example Blended Powder-0").should("exist");
        cy.findByText("Example Blended Powder-1").should("exist");
        cy.findByText("Example Blended Powder-2").should("exist");
        cy.findByText("Example Blended Powder-3").should("exist");
        cy.findByText("Example Blended Powder-4").should("exist");
        cy.findByText("Example Blended Powder-5").should("exist");
        cy.findByText("Example Blended Powder-6").should("exist");
        cy.findByText("Example Blended Powder-7").should("exist");
        cy.findByText("Example Blended Powder-8").should("exist");
        cy.findByText("Example Blended Powder-9").should("exist");
        cy.findByText("Example Blended Powder-10").should("exist");
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

