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

describe("Test blending powders and blended material deletion", () => {
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
        cy.findAllByLabelText("Increment (%)").first().type(20);
        cy.findAllByLabelText("Min (%)").first().type(0);
        cy.findAllByLabelText("Max (%)").first().type(100);
        // Check the autocompletion feature
        cy.findAllByLabelText("Min (%)").last().should("have.value", "100.00");
        cy.findAllByLabelText("Max (%)").last().should("have.value", "0.00");
        cy.findByText("5 - Confirm configuration").click().scrollIntoView();

        // Check that the configurations were generated correctly
        cy.findByDisplayValue("0/100").should("exist");
        cy.findByDisplayValue("20/80").should("exist");
        cy.findByDisplayValue("40/60").should("exist");
        cy.findByDisplayValue("60/40").should("exist");
        cy.findByDisplayValue("80/20").should("exist");
        cy.findByDisplayValue("100/0").should("exist");

        // Delete the last two blends and add them again
        cy.findByText("Delete blend").click().click();
        cy.findByText("Add blend").click().click();
        cy.get('input[id="all_ratio_entries-4-ratio"]').type("80/20");
        cy.get('input[id="all_ratio_entries-5-ratio"]').type("100/0");
        cy.findByText("6 - Create blended materials").click();

        // Check that the blended powders were generated correctly
        cy.findByText("All blended materials").scrollIntoView();
        cy.findByText("Example Blended Powder-0").should("exist");
        cy.findByText("Example Blended Powder-1").should("exist");
        cy.findByText("Example Blended Powder-2").should("exist");
        cy.findByText("Example Blended Powder-3").should("exist");
        cy.findByText("Example Blended Powder-4").should("exist");
        cy.findByText("Example Blended Powder-5").should("exist");

        // Delete all blended powders one by one
        for (let i = 6; i > 0; --i) {
            cy.get(".btn-group").last().click();
            // Wait for the modal animation to finish
            cy.wait(400);
            cy.findAllByText("Confirm").last().click();
            // Check that the table entry was deleted
            cy.get(".btn-group").should("have.length", i - 1);
        }
    });
});

describe("Test blending liquids and property interpolation", () => {
    beforeEach(() => {
        cy.createExampleLiquids();
        cy.visit("http://localhost:5001/materials/blended");
        cy.findByLabelText("2 - Material type").select("Liquid");
        cy.findByText("Example Liquid 1").should("exist");
        cy.findByText("Example Liquid 2").should("exist");
    });

    it("Create blended liquid", () => {
        cy.findByLabelText("1 - Name").type("Example Blended Liquid");
        cy.findByLabelText("2 - Material type").select("Liquid");
        cy.findByLabelText("3 - Base materials").select(["Example Liquid 1", "Example Liquid 2"]);
        cy.findByText("4 - Confirm Selection").click();
        // Wait for the modal animation to finish
        cy.wait(400);
        cy.findByText("Change Selection").should("exist");
        cy.findByText("Do you really want to change the chosen selection?").should("exist");
        cy.findByText("Close").should("exist");
        cy.findByText("Confirm").click();

        // Fill in the increment, min, max values
        cy.findAllByLabelText("Increment (%)").first().type(20);
        cy.findAllByLabelText("Min (%)").first().type(20);
        cy.findAllByLabelText("Max (%)").first().type(80);
        // Check the autocompletion feature
        cy.findAllByLabelText("Min (%)").last().should("have.value", "80.00");
        cy.findAllByLabelText("Max (%)").last().should("have.value", "20.00");
        cy.findByText("5 - Confirm configuration").click().scrollIntoView();

        // Check that the configurations were generated correctly
        cy.findByDisplayValue("20/80").should("exist");
        cy.findByDisplayValue("40/60").should("exist");
        cy.findByDisplayValue("60/40").should("exist");
        cy.findByDisplayValue("80/20").should("exist");
        cy.findByText("6 - Create blended materials").click();

        // Check that the blended liquids were generated correctly
        cy.findByText("All blended materials").scrollIntoView();
        cy.findByText("Example Blended Liquid-0").should("exist");
        cy.findByText("Example Blended Liquid-1").should("exist");
        cy.findByText("Example Blended Liquid-2").should("exist");
        cy.findByText("Example Blended Liquid-3").should("exist");

        // Check that the properties for the first blended liquid were interpolated correctly
        cy.findByText("Na₂SiO₃ (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("NaOH (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("Na₂SiO₃ specific (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("NaOH specific (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("Total solution (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("Na₂O (I) (%): 6.0", { exact: false }).should("exist");
        cy.findByText("SiO₂ (I) (%): 6.0", { exact: false }).should("exist");
        cy.findByText("H₂O (%): 6.0", { exact: false }).should("exist");
        cy.findByText("Na₂O (dry) (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("SiO₂ (dry) (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("Water (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("Total NaOH (m%): 6.0", { exact: false }).should("exist");
        cy.findByText("Costs (€/kg): 6.0", { exact: false }).should("exist");
        cy.findByText("CO₂ footprint (kg): 6.0", { exact: false }).should("exist");
        cy.findAllByText("Delivery time (days): 10.0", { exact: false }).first().should("exist");

        // Check that the properties for the second blended liquid were interpolated correctly
        cy.findByText("Na₂SiO₃ (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("NaOH (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("Na₂SiO₃ specific (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("NaOH specific (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("Total solution (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("Na₂O (I) (%): 7.0", { exact: false }).should("exist");
        cy.findByText("SiO₂ (I) (%): 7.0", { exact: false }).should("exist");
        cy.findByText("H₂O (%): 7.0", { exact: false }).should("exist");
        cy.findByText("Na₂O (dry) (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("SiO₂ (dry) (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("Water (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("Total NaOH (m%): 7.0", { exact: false }).should("exist");
        cy.findByText("Costs (€/kg): 7.0", { exact: false }).should("exist");
        cy.findByText("CO₂ footprint (kg): 7.0", { exact: false }).should("exist");
        cy.findAllByText("Delivery time (days): 10.0", { exact: false }).eq(1).should("exist");

        // Check that the properties for the third blended liquid were interpolated correctly
        cy.findByText("Na₂SiO₃ (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("NaOH (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("Na₂SiO₃ specific (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("NaOH specific (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("Total solution (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("Na₂O (I) (%): 8.0", { exact: false }).should("exist");
        cy.findByText("SiO₂ (I) (%): 8.0", { exact: false }).should("exist");
        cy.findByText("H₂O (%): 8.0", { exact: false }).should("exist");
        cy.findByText("Na₂O (dry) (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("SiO₂ (dry) (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("Water (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("Total NaOH (m%): 8.0", { exact: false }).should("exist");
        cy.findByText("Costs (€/kg): 8.0", { exact: false }).should("exist");
        cy.findByText("CO₂ footprint (kg): 8.0", { exact: false }).should("exist");
        cy.findAllByText("Delivery time (days): 10.0", { exact: false }).eq(2).should("exist");

        // Check that the properties for the fourth blended liquid were interpolated correctly
        cy.findByText("Na₂SiO₃ (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("NaOH (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("Na₂SiO₃ specific (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("NaOH specific (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("Total solution (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("Na₂O (I) (%): 9.0", { exact: false }).should("exist");
        cy.findByText("SiO₂ (I) (%): 9.0", { exact: false }).should("exist");
        cy.findByText("H₂O (%): 9.0", { exact: false }).should("exist");
        cy.findByText("Na₂O (dry) (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("SiO₂ (dry) (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("Water (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("Total NaOH (m%): 9.0", { exact: false }).should("exist");
        cy.findByText("Costs (€/kg): 9.0", { exact: false }).should("exist");
        cy.findByText("CO₂ footprint (kg): 9.0", { exact: false }).should("exist");
        cy.findAllByText("Delivery time (days): 10.0", { exact: false }).last().should("exist");
    });
});

describe("Test blending aggregates and incomplete data", () => {
    beforeEach(() => {
        cy.createExampleAggregates();
        cy.visit("http://localhost:5001/materials/blended");
        cy.findByLabelText("2 - Material type").select("Aggregates");
        cy.findByText("Example Aggregates 1").should("exist");
        cy.findByText("Example Aggregates 2").should("exist");
    });

    it("Create blended aggregates with additional properties", () => {
        cy.findByLabelText("1 - Name").type("Example Blended Aggregates");
        cy.findByLabelText("2 - Material type").select("Aggregates");
        cy.findByLabelText("3 - Base materials").select(["Example Aggregates 1", "Example Aggregates 2"]);
        cy.findByText("4 - Confirm Selection").click();
        // Wait for the modal animation to finish
        cy.wait(400);
        cy.findByText("Change Selection").should("exist");
        cy.findByText("Do you really want to change the chosen selection?").should("exist");
        cy.findByText("Close").should("exist");
        cy.findByText("Confirm").click();

        // Fill in the increment, min, max values
        cy.findAllByLabelText("Increment (%)").first().type(40);
        cy.findAllByLabelText("Min (%)").first().type(20);
        cy.findAllByLabelText("Max (%)").first().type(80);
        // Check the autocompletion feature
        cy.findAllByLabelText("Min (%)").last().should("have.value", "80.00");
        cy.findAllByLabelText("Max (%)").last().should("have.value", "20.00");
        cy.findByText("5 - Confirm configuration").click().scrollIntoView();

        // Check that the configurations were generated correctly
        cy.findByDisplayValue("20/80").should("exist");
        cy.findByDisplayValue("60/40").should("exist");
        cy.findByText("6 - Create blended materials").click();

        // Check that the blended aggregates were generated correctly
        cy.findByText("All blended materials").scrollIntoView();
        cy.findByText("Example Blended Aggregates-0").should("exist");
        cy.findByText("Example Blended Aggregates-1").should("exist");

        // Check that only the properties common to both base materials were interpolated
        cy.findByText("Costs (€/kg): 6.0", { exact: false }).should("exist");
        cy.findByText("CO₂ footprint (kg): 6.0", { exact: false }).should("exist");
        cy.findAllByText("Delivery time (days): 10.0", { exact: false }).first().should("exist");
        cy.findByText("Example shared property: 6.0", { exact: false }).should("exist");
        cy.findByText("Costs (€/kg): 8.0", { exact: false }).should("exist");
        cy.findByText("CO₂ footprint (kg): 8.0", { exact: false }).should("exist");
        cy.findAllByText("Delivery time (days): 10.0", { exact: false }).last().should("exist");
        cy.findByText("Example shared property: 8.0", { exact: false }).should("exist");
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

