describe("Test blending materials page", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/materials/blended");
  });

  it("Material types are listed correctly", () => {
    cy.findByText("Powder").should("exist");
    cy.findByLabelText("2 - Material type *").select("Powder").should("have.value", "Powder");
    cy.findByLabelText("2 - Material type *").select("Liquid").should("have.value", "Liquid");
    cy.findByLabelText("2 - Material type *").select("Aggregates").should("have.value", "Aggregates");
    cy.findByLabelText("2 - Material type *").select("Admixture").should("have.value", "Admixture");
    cy.findByLabelText("2 - Material type *").select("Custom").should("have.value", "Custom");
    cy.findByLabelText("2 - Material type *").select("Powder").should("have.value", "Powder");
  });
});

describe("Test blending powders and blended material deletion", () => {
  beforeEach(() => {
    cy.createExamplePowders();
    cy.visit("http://localhost:5001/materials/blended");
  });

  it("Create blended powder", () => {
    cy.findByLabelText("1 - Name *").type("Example Blended Powder").should("have.value", "Example Blended Powder");
    cy.findByLabelText("2 - Material type *").select("Powder").should("have.value", "Powder");
    cy.findByLabelText("3 - Base materials *").select(["Example Powder 1", "Example Powder 2"]);
    cy.findByText("4 - Configure blending ratios").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/blended/add_min_max_entries/powder/2");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (%)": [20],
      "Min (%)": [0],
      "Max (%)": [100],
    });
    // Check the autocompletion feature
    cy.findAllByLabelText("Max (%)").last().should("have.value", "100.00");
    cy.findAllByLabelText("Min (%)").last().should("have.value", "0.00");
    cy.clickButtonWaitForAsyncRequest("5 - Preview blending ratios", "/materials/blended/add_ratios");

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations(["0/100", "20/80", "40/60", "60/40", "80/20", "100/0"]);

    // Delete the last two blends and add them again
    cy.findByText("Delete blending ratio").click().click();
    cy.findByText("Add blending ratio").click().click();
    cy.get('input[id="all_ratio_entries-4-ratio"]').type("80/20").should("have.value", "80/20");
    cy.get('input[id="all_ratio_entries-5-ratio"]').type("100/0").should("have.value", "100/0");
    cy.findByText("Submit").click();

    // Check that the blended powders were generated correctly
    cy.findByText("All blended materials").scrollIntoView();
    cy.checkGeneratedContent([
      "Example Blended Powder-0.0/1.0",
      "Example Blended Powder-0.2/0.8",
      "Example Blended Powder-0.4/0.6",
      "Example Blended Powder-0.6/0.4",
      "Example Blended Powder-0.8/0.2",
      "Example Blended Powder-1.0/0.0",
    ]);

    // Delete all blended powders one by one
    for (let i = 6; i > 0; --i) {
      cy.get("th > div > button").last().click();
      // Wait for the modal animation to finish
      cy.wait(400);
      cy.findAllByText("Confirm").last().click();
      // Check that the table entry was deleted
      cy.get("th > div > button").should("have.length", i - 1);
    }
  });
});

describe("Test blending liquids and property interpolation", () => {
  beforeEach(() => {
    cy.createExampleLiquids();
    cy.visit("http://localhost:5001/materials/blended");
    cy.findByLabelText("2 - Material type *").select("Liquid").should("have.value", "Liquid");
  });

  it("Create blended liquid", () => {
    cy.findByLabelText("1 - Name *").type("Example Blended Liquid").should("have.value", "Example Blended Liquid");
    cy.findByLabelText("2 - Material type *").select("Liquid").should("have.value", "Liquid");
    cy.findByLabelText("3 - Base materials *").select(["Example Liquid 1", "Example Liquid 2"]);
    cy.findByText("4 - Configure blending ratios").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/blended/add_min_max_entries/liquid/2");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (%)": [20],
      "Min (%)": [20],
      "Max (%)": [80],
    });
    // Check the autocompletion feature
    cy.findAllByLabelText("Max (%)").last().should("have.value", "80.00");
    cy.findAllByLabelText("Min (%)").last().should("have.value", "20.00");
    cy.clickButtonWaitForAsyncRequest("5 - Preview blending ratios", "/materials/blended/add_ratios");

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations(["20/80", "40/60", "60/40", "80/20"]);
    cy.findByText("Submit").click();

    // Check that the blended liquids were generated correctly
    cy.findByText("All blended materials").scrollIntoView();
    cy.checkGeneratedContent([
      "Example Blended Liquid-0.2/0.8",
      "Example Blended Liquid-0.4/0.6",
      "Example Blended Liquid-0.6/0.4",
      "Example Blended Liquid-0.8/0.2",
    ]);

    // Check that the properties for the first blended liquid were interpolated correctly
    cy.checkGeneratedContent(
      [
        "Na₂SiO₃ (m%): 6.0",
        "NaOH (m%): 6.0",
        "Na₂SiO₃ (mol%): 6.0",
        "NaOH (mol%): 6.0",
        "Na₂O (m%): 6.0",
        "SiO₂ (m%): 6.0",
        "H₂O (m%): 6.0",
        "Na₂O (mol%): 6.0",
        "SiO₂ (mol%): 6.0",
        "H₂O (mol%): 6.0",
        "NaOH (mol%): 6.0",
        "Costs (€/ton for materials, € for processes): 6.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): 6.0",
      ],
      false
    );

    // Check that the properties for the second blended liquid were interpolated correctly
    cy.checkGeneratedContent(
      [
        "Na₂SiO₃ (m%): 7.0",
        "NaOH (m%): 7.0",
        "Na₂SiO₃ (mol%): 7.0",
        "NaOH (mol%): 7.0",
        "Na₂O (m%): 7.0",
        "SiO₂ (m%): 7.0",
        "H₂O (m%): 7.0",
        "Na₂O (mol%): 7.0",
        "SiO₂ (mol%): 7.0",
        "H₂O (mol%): 7.0",
        "Costs (€/ton for materials, € for processes): 7.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): 7.0",
      ],
      false
    );

    // Check that the properties for the third blended liquid were interpolated correctly
    cy.checkGeneratedContent(
      [
        "Na₂SiO₃ (m%): 8.0",
        "NaOH (m%): 8.0",
        "Na₂SiO₃ (mol%): 8.0",
        "NaOH (mol%): 8.0",
        "Na₂O (m%): 8.0",
        "SiO₂ (m%): 8.0",
        "H₂O (m%): 8.0",
        "Na₂O (mol%): 8.0",
        "SiO₂ (mol%): 8.0",
        "H₂O (mol%): 8.0",
        "Costs (€/ton for materials, € for processes): 8.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): 8.0",
      ],
      false
    );

    // Check that the properties for the fourth blended liquid were interpolated correctly
    cy.checkGeneratedContent(
      [
        "Na₂SiO₃ (m%): 9.0",
        "NaOH (m%): 9.0",
        "Na₂SiO₃ (mol%): 9.0",
        "NaOH (mol%): 9.0",
        "Na₂O (m%): 9.0",
        "SiO₂ (m%): 9.0",
        "H₂O (m%): 9.0",
        "Na₂O (mol%): 9.0",
        "SiO₂ (mol%): 9.0",
        "H₂O (mol%): 9.0",
        "Costs (€/ton for materials, € for processes): 9.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): 9.0",
      ],
      false
    );

    // Delivery time is calculated as the maximum value of all used materials.
    // It should be the same for all generated blends.
    cy.findAllByText("Delivery time (days): 10.0", { exact: false }).should("have.length", 4);
  });
});

describe("Test blending aggregates and incomplete data", () => {
  beforeEach(() => {
    cy.createExampleAggregates();
    cy.visit("http://localhost:5001/materials/blended");
    cy.findByLabelText("2 - Material type *").select("Aggregates").should("have.value", "Aggregates");
  });

  it("Create blended aggregates with additional properties", () => {
    cy.findByLabelText("1 - Name *")
      .type("Example Blended Aggregates")
      .should("have.value", "Example Blended Aggregates");
    cy.findByLabelText("2 - Material type *").select("Aggregates").should("have.value", "Aggregates");
    cy.findByLabelText("3 - Base materials *").select(["Example Aggregates 1", "Example Aggregates 2"]);
    cy.findByText("4 - Configure blending ratios").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/blended/add_min_max_entries/aggregates/2");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (%)": [40],
      "Min (%)": [20],
      "Max (%)": [80],
    });
    // Check the autocompletion feature
    cy.findAllByLabelText("Max (%)").last().should("have.value", "80.00");
    cy.findAllByLabelText("Min (%)").last().should("have.value", "20.00");
    cy.clickButtonWaitForAsyncRequest("5 - Preview blending ratios", "/materials/blended/add_ratios");

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations(["20/80", "60/40"]);
    cy.findByText("Submit").click();

    // Check that the blended aggregates were generated correctly
    cy.findByText("All blended materials").scrollIntoView();
    cy.checkGeneratedContent(["Example Blended Aggregates-0.2/0.8", "Example Blended Aggregates-0.6/0.4"]);

    // Check that only the properties common to both base materials were interpolated
    cy.checkGeneratedContent(
      [
        "Costs (€/ton for materials, € for processes): 6.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): 6.0",
        "Example shared property: 6.0",
        "Costs (€/ton for materials, € for processes): 8.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): 8.0",
        "Example shared property: 8.0",
      ],
      false
    );

    // Delivery time is calculated as the maximum value of all used materials.
    // It should be the same for all generated blends.
    cy.findAllByText("Delivery time (days): 10.0", { exact: false }).should("have.length", 2);
  });
});

describe("Test blending three custom materials with properties with negative values", () => {
  beforeEach(() => {
    cy.createExampleCustomMaterials();
    cy.visit("http://localhost:5001/materials/blended");
    cy.findByLabelText("2 - Material type *").select("Custom").should("have.value", "Custom");
  });

  it("Create blend from three custom materials", () => {
    cy.findByLabelText("1 - Name *").type("Example Blended Custom").should("have.value", "Example Blended Custom");
    cy.findByLabelText("2 - Material type *").select("Custom").should("have.value", "Custom");
    cy.findByLabelText("3 - Base materials *").select(["Example Custom 1", "Example Custom 2", "Example Custom 3"]);
    cy.findByText("4 - Configure blending ratios").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/blended/add_min_max_entries/custom/3");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (%)": [50, 5],
      "Min (%)": [20, 20],
      "Max (%)": [75, 25],
    });
    // Check the autocompletion feature
    cy.findAllByLabelText("Max (%)").last().should("have.value", "60.00");
    cy.findAllByLabelText("Min (%)").last().should("have.value", "0.00");
    cy.clickButtonWaitForAsyncRequest("5 - Preview blending ratios", "/materials/blended/add_ratios");

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations(["20/20/60", "20/25/55", "70/20/10", "70/25/5"]);
    cy.findByText("Submit").click();

    // Check that the blended custom materials were generated correctly
    cy.findByText("All blended materials").scrollIntoView();
    cy.checkGeneratedContent([
      "Example Blended Custom-0.2/0.2/0.6",
      "Example Blended Custom-0.2/0.25/0.55",
      "Example Blended Custom-0.7/0.2/0.1",
      "Example Blended Custom-0.7/0.25/0.05",
    ]);

    // Check that the properties for the blends were interpolated correctly
    cy.checkGeneratedContent(
      [
        // First blend
        "Costs (€/ton for materials, € for processes): 15.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): -4.4",
        // Second blend
        "Costs (€/ton for materials, € for processes): 20.5",
        "CO₂ footprint (kg/ton for materials, kg for processes): -3.65",
        // Third blend
        "Costs (€/ton for materials, € for processes): 22.5",
        "CO₂ footprint (kg/ton for materials, kg for processes): 2.1",
        // Fourth blend
        "Costs (€/ton for materials, € for processes): 28.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): 2.85",
      ],
      false
    );

    // Delivery time is calculated as the maximum value of all used materials.
    // It should be the same for all generated blends.
    cy.findAllByText("Delivery time (days): 20.0", { exact: false }).should("have.length", 4);
  });
});

describe("Test blending three admixtures with properties with negative values", () => {
  beforeEach(() => {
    cy.createExampleAdmixtures();
    cy.visit("http://localhost:5001/materials/blended");
    cy.findByLabelText("2 - Material type *").select("Admixture").should("have.value", "Admixture");
  });

  it("Create blend from three admixtures", () => {
    cy.findByLabelText("1 - Name *")
      .type("Example Blended Admixture")
      .should("have.value", "Example Blended Admixture");
    cy.findByLabelText("2 - Material type *").select("Admixture").should("have.value", "Admixture");
    cy.findByLabelText("3 - Base materials *").select([
      "Example Admixture 1",
      "Example Admixture 2",
      "Example Admixture 3",
    ]);
    cy.findByText("4 - Configure blending ratios").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/blended/add_min_max_entries/admixture/3");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (%)": [50, 5],
      "Min (%)": [20, 20],
      "Max (%)": [75, 25],
    });
    // Check the autocompletion feature
    cy.findAllByLabelText("Max (%)").last().should("have.value", "60.00");
    cy.findAllByLabelText("Min (%)").last().should("have.value", "0.00");
    cy.clickButtonWaitForAsyncRequest("5 - Preview blending ratios", "/materials/blended/add_ratios");

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations(["20/20/60", "20/25/55", "70/20/10", "70/25/5"]);
    cy.findByText("Submit").click();

    // Check that the blended admixtures were generated correctly
    cy.findByText("All blended materials").scrollIntoView();
    cy.checkGeneratedContent([
      "Example Blended Admixture-0.2/0.2/0.6",
      "Example Blended Admixture-0.2/0.25/0.55",
      "Example Blended Admixture-0.7/0.2/0.1",
      "Example Blended Admixture-0.7/0.25/0.05",
    ]);

    // Check that the properties for the blends were interpolated correctly
    cy.checkGeneratedContent(
      [
        // First blend
        "Costs (€/ton for materials, € for processes): 15.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): -4.4",
        // Second blend
        "Costs (€/ton for materials, € for processes): 20.5",
        "CO₂ footprint (kg/ton for materials, kg for processes): -3.65",
        // Third blend
        "Costs (€/ton for materials, € for processes): 22.5",
        "CO₂ footprint (kg/ton for materials, kg for processes): 2.1",
        // Fourth blend
        "Costs (€/ton for materials, € for processes): 28.0",
        "CO₂ footprint (kg/ton for materials, kg for processes): 2.85",
      ],
      false
    );

    // Delivery time is calculated as the maximum value of all used materials.
    // It should be the same for all generated blends.
    cy.findAllByText("Delivery time (days): 20.0", { exact: false }).should("have.length", 4);
  });
});

describe("Test autocorrect features", () => {
  beforeEach(() => {
    cy.createExamplePowders();
    cy.visit("http://localhost:5001/materials/blended");
  });

  it("Increment, min and max fields are corrected automatically", () => {
    cy.findByLabelText("1 - Name *").type("Example Blended Powder").should("have.value", "Example Blended Powder");
    cy.findByLabelText("2 - Material type *").select("Powder").should("have.value", "Powder");
    cy.findByLabelText("3 - Base materials *").select(["Example Powder 1", "Example Powder 2"]);
    cy.findByText("4 - Configure blending ratios").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/blended/add_min_max_entries/powder/2");

    // Check that it clips the value to 100 from above
    cy.findAllByLabelText("Increment (%)").first().type("123");
    cy.findAllByLabelText("Increment (%)").first().should("have.value", 100);
    // Check that it clips the value to 0 from below
    cy.findAllByLabelText("Increment (%)").first().type("{moveToStart}-");
    cy.findAllByLabelText("Increment (%)").first().should("have.value", 0);
    // Check that it rounds the value to two decimals
    cy.findAllByLabelText("Increment (%)").first().clear().type("45.678");
    cy.findAllByLabelText("Increment (%)").first().should("have.value", 45.68);

    // Check that it clips the value to 100 from above
    cy.findAllByLabelText("Min (%)").first().type("123");
    cy.findAllByLabelText("Min (%)").first().should("have.value", "100.00");
    // Check that it clips the value to 0 from below
    cy.findAllByLabelText("Min (%)").first().type("{moveToStart}-");
    cy.findAllByLabelText("Min (%)").first().should("have.value", 0);
    // Check that it rounds the value to two decimals
    cy.findAllByLabelText("Min (%)").first().clear().type("45.678");
    cy.findAllByLabelText("Min (%)").first().should("have.value", 45.68);

    // Check that it clips the value to 100 from above
    cy.findAllByLabelText("Max (%)").first().type("123");
    cy.findAllByLabelText("Max (%)").first().should("have.value", "100.00");
    // Check that it clips the value to 0 from below
    cy.findAllByLabelText("Max (%)").first().type("{moveToStart}-");
    cy.findAllByLabelText("Max (%)").first().should("have.value", 0);
    // Check that it rounds the value to two decimals
    cy.findAllByLabelText("Max (%)").first().clear().type("45.678");
    cy.findAllByLabelText("Max (%)").first().should("have.value", 45.68);
  });
});
