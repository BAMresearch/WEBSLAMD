describe("Test upload dataset form", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/materials/discovery");
  });

  it("File upload works", () => {
    cy.get("input[type=file]").last().selectFile("examples/MaterialsDiscoveryExampleData.csv");
    cy.findByText("Upload dataset").click();
    cy.checkGeneratedContent(
      [
        "MaterialsDiscoveryExampleData.csv",
        "Idx_Sample",
        "SiO2",
        "CaO",
        "SO3",
        "FA (kg/m3)",
        "GGBFS (kg/m3)",
        "Coarse aggregate (kg/m3)",
        "Fine aggregate (kg/m3)",
        "Total aggregates",
        "Na2SiO3",
        "Na2O (Dry)",
        "Sio2 (Dry)",
        "Superplasticizer",
        "water -eff",
        "Slump - Target (mm)",
        "CO2 (kg/t) - A-priori Information",
        "fc 28-d - Target (MPa)",
      ],
      false
    );
  });

  it("Delete dataset works", () => {
    cy.get("input[type=file]").last().selectFile("examples/MaterialsDiscoveryExampleData.csv");
    cy.findByText("Upload dataset").click();
    cy.get(".btn-group > div > button").eq(0).click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findAllByText("Confirm").filter(':visible').click();
    cy.findByText("MaterialsDiscoveryExampleData.csv").should("not.exist");
  });

  it("Select dataset works", () => {
    cy.get("input[type=file]").last().selectFile("examples/MaterialsDiscoveryExampleData.csv");
    cy.findByText("Upload dataset").click();
    cy.get(".btn-group > div > a").eq(0).click();
    cy.url().should("eq", "http://localhost:5001/materials/discovery/MaterialsDiscoveryExampleData.csv");
  });
});

describe("Test running experiments with example dataset", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/materials/discovery");
    cy.get("input[type=file]").last().selectFile("examples/MaterialsDiscoveryExampleData.csv");
    cy.findByText("Upload dataset").click();
    cy.get(".btn-group > div > a").eq(0).click();
    cy.url().should("eq", "http://localhost:5001/materials/discovery/MaterialsDiscoveryExampleData.csv");
  });

  it("One target property and one a priori information minimized works", () => {
    // Select features
    cy.findByLabelText("Materials Data (Input) (select one column at least)").select([
      "SiO2",
      "CaO",
      "SO3",
      "FA (kg/m3)",
      "GGBFS (kg/m3)",
      "Coarse aggregate (kg/m3)",
      "Fine aggregate (kg/m3)",
      "Total aggregates",
      "Na2SiO3",
      "Na2O (Dry)",
      "Sio2 (Dry)",
      "Superplasticizer",
      "water -eff",
    ]);

    // Select target properties
    cy.selectInputWaitForAsyncRequest(
      "Target Properties (select one column at least)",
      ["fc 28-d - Target (MPa)"],
      "materials/discovery/create_target_configuration_form"
    );

    // Check that a form appeared
    cy.findAllByLabelText("Maximize").should("have.length", 1);
    cy.findAllByLabelText("Minimize").should("have.length", 1);
    cy.findAllByLabelText("Weight").should("have.length", 1);
    cy.findAllByLabelText("Threshold").should("have.length", 1);

    // Select a priori information
    cy.selectInputWaitForAsyncRequest(
      "A priori Information (optional)",
      ["CO2 (kg/t) - A-priori Information"],
      "materials/discovery/create_a_priori_information_configuration_form"
    );

    // Check that a second form appeared
    cy.findAllByLabelText("Maximize").should("have.length", 2);
    cy.findAllByLabelText("Minimize").should("have.length", 2);
    cy.findAllByLabelText("Weight").should("have.length", 2);
    cy.findAllByLabelText("Threshold").should("have.length", 2);

    // Minimize CO2
    cy.findAllByLabelText("Minimize").eq(1).check();

    // Run the experiment, wait for the request to complete
    cy.clickButtonWaitForAsyncRequest(
      "Run experiment with given configuration",
      "materials/discovery/MaterialsDiscoveryExampleData.csv"
    );
    cy.get(".spinner-border").should("not.exist");

    // Check first for the columns
    // [Row number, Utility, Novelty, fc 28-d - Target (MPa), Uncertainty (fc 28-d - Target (MPa)), CO2 (kg/t) - A-priori Information]
    cy.get(".table-responsive")
      .eq(1)
      .within(() => {
        cy.checkGeneratedTable([
          [1, 2.50395, 0.224525, 55.171406, 7.57989, 116.12407],
        ]);
      });
  });

});
