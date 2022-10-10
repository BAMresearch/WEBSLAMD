describe("Test formulations page", () => {
  beforeEach(() => {
    cy.createExamplePowders();
    cy.createExampleLiquids();
    cy.createExampleAggregates();
    cy.visit("http://localhost:5001/materials/formulations");
  });

  it("Create formulations and submit them without a dataset name", () => {
    cy.findByLabelText("1.1 - Powders (select one at least)").select("Example Powder 1");
    cy.findByLabelText("1.2 - Liquids (select one at least)").select("Example Liquid 1");
    cy.findByLabelText("1.3 - Aggregates (select one at least)").select("Example Aggregates 1");
    cy.fillForm({
      "1.7 - Constraint (Sum of materials used for formulation) (kg) *": 100,
    });

    cy.findByText("4 - Configure weights for each material type").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/formulations/add_min_max_entries");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (kg)": [30, 15],
      "Min (kg)": [10, 5],
      "Max (kg)": [70, 25],
    });
    // Check the autocompletion feature
    cy.findAllByLabelText("Min (kg)").last().should("have.value", "85.00");
    cy.findAllByLabelText("Max (kg)").last().should("have.value", "5.00");
    cy.clickButtonWaitForAsyncRequest(
      "5 - Show mixture in terms of base material composition",
      "/materials/formulations/add_weights"
    );

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations([
      "10.0/5.0/85.0",
      "10.0/20.0/70.0",
      "40.0/5.0/55.0",
      "40.0/20.0/40.0",
      "70.0/5.0/25.0",
      "70.0/20.0/10.0",
    ]);
    cy.intercept("/materials/formulations/create_formulations_batch").as("create_formulations_batch");
    cy.findByText("6 - Create material formulations for given configuration").click();
    cy.wait("@create_formulations_batch");

    // Check that the materials formulations were generated correctly
    cy.findByText("Show / hide formulations").scrollIntoView();
    cy.findByText("Idx_Sample").should("exist");
    // Check the first 4 columns for every row
    cy.checkGeneratedTable([
      [0, 10.0, 5.0, 85.0],
      [1, 10.0, 20.0, 70.0],
      [2, 40.0, 5.0, 55.0],
      [3, 40.0, 20.0, 40.0],
      [4, 70.0, 5.0, 25.0],
      [5, 70.0, 20.0, 10.0],
    ]);

    // Submit dataset with the default dataset name
    cy.findByText("Submit").click();
  });

  it("Create formulations with two of every required material", () => {
    cy.findByLabelText("1.1 - Powders (select one at least)").select(["Example Powder 1", "Example Powder 2"]);
    cy.findByLabelText("1.2 - Liquids (select one at least)").select(["Example Liquid 1", "Example Liquid 2"]);
    cy.findByLabelText("1.3 - Aggregates (select one at least)").select([
      "Example Aggregates 1",
      "Example Aggregates 2",
    ]);
    cy.fillForm({
      "1.7 - Constraint (Sum of materials used for formulation) (kg) *": 100,
    });

    cy.findByText("4 - Configure weights for each material type").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/formulations/add_min_max_entries");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (kg)": [40, 10],
      "Min (kg)": [20, 10],
      "Max (kg)": [60, 10],
    });
    // Check the autocompletion feature
    cy.findAllByLabelText("Min (kg)").last().should("have.value", "70.00");
    cy.findAllByLabelText("Max (kg)").last().should("have.value", "30.00");
    cy.clickButtonWaitForAsyncRequest(
      "5 - Show mixture in terms of base material composition",
      "/materials/formulations/add_weights"
    );

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations(["20.0/10.0/70.0", "60.0/10.0/30.0"]);
    cy.intercept("/materials/formulations/create_formulations_batch").as("create_formulations_batch");
    cy.findByText("6 - Create material formulations for given configuration").click();
    cy.wait("@create_formulations_batch");

    // Check that the materials formulations were generated correctly
    cy.findByText("Show / hide formulations").scrollIntoView();
    cy.findByText("Idx_Sample").should("exist");
    // Check the first 4 columns for every row
    cy.checkGeneratedTable([
      [0, 20.0, 10.0, 70.0],
      [1, 60.0, 10.0, 30.0],
      [2, 20.0, 10.0, 70.0],
      [3, 60.0, 10.0, 30.0],
      [4, 20.0, 10.0, 70.0],
      [5, 60.0, 10.0, 30.0],
      [6, 20.0, 10.0, 70.0],
      [7, 60.0, 10.0, 30.0],
      [8, 20.0, 10.0, 70.0],
      [9, 60.0, 10.0, 30.0],
      [10, 20.0, 10.0, 70.0],
      [11, 60.0, 10.0, 30.0],
      [12, 20.0, 10.0, 70.0],
      [13, 60.0, 10.0, 30.0],
      [14, 20.0, 10.0, 70.0],
      [15, 60.0, 10.0, 30.0],
    ]);

    // Submit dataset with the default dataset name
    cy.findByText("Submit").click();
  });

  it("Delete formulations and create them again", () => {
    cy.findByLabelText("1.1 - Powders (select one at least)").select("Example Powder 1");
    cy.findByLabelText("1.2 - Liquids (select one at least)").select("Example Liquid 1");
    cy.findByLabelText("1.3 - Aggregates (select one at least)").select("Example Aggregates 1");
    cy.fillForm({
      "1.7 - Constraint (Sum of materials used for formulation) (kg) *": 100,
      "1.8 - Name of the dataset (optional)": "Example dataset name",
    });

    cy.findByText("4 - Configure weights for each material type").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/formulations/add_min_max_entries");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (kg)": [10, 10],
      "Min (kg)": [50, 40],
      "Max (kg)": [60, 40],
    });
    cy.clickButtonWaitForAsyncRequest(
      "5 - Show mixture in terms of base material composition",
      "/materials/formulations/add_weights"
    );

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations(["50.0/40.0/10.0", "60.0/40.0/0.0"]);
    cy.intercept("/materials/formulations/create_formulations_batch").as("create_formulations_batch");
    cy.findByText("6 - Create material formulations for given configuration").click();
    cy.wait("@create_formulations_batch");

    // Delete the last formulation
    cy.get(".input-group > button").last().click();
    cy.findByDisplayValue("60.0/40.0/0.0").should("not.exist");

    // Check that the materials formulations were generated correctly
    cy.findByText("Show / hide formulations").scrollIntoView();
    cy.findByText("Idx_Sample").should("exist");
    // Check the only generated row
    cy.checkGeneratedTable([[0, 50.0, 40.0, 10.0]]);
    // Delete all rows
    cy.findByText("Delete Material Formulation").click();
    cy.findByText("Idx_Sample").should("not.exist");

    // Create the formulation again
    cy.intercept("/materials/formulations/create_formulations_batch").as("create_formulations_batch");
    cy.findByText("6 - Create material formulations for given configuration").click();
    cy.wait("@create_formulations_batch");
    // Submit dataset with the given name
    cy.findByText("Submit").click();
  });
});

describe("Test formulations with admixture, process and custom", () => {
  beforeEach(() => {
    cy.createExamplePowders();
    cy.createExampleLiquids();
    cy.createExampleAggregates();
    cy.createExampleAdmixtures();
    cy.createExampleCustomMaterials();
    cy.createExampleProcesses();
    cy.visit("http://localhost:5001/materials/formulations");
  });

  it("Create formulations and submit them without a dataset name", () => {
    cy.findByLabelText("1.1 - Powders (select one at least)").select("Example Powder 1");
    cy.findByLabelText("1.2 - Liquids (select one at least)").select("Example Liquid 1");
    cy.findByLabelText("1.3 - Aggregates (select one at least)").select("Example Aggregates 1");
    cy.findByLabelText("1.4 - Admixture (optional)").select("Example Admixture 1");
    cy.findByLabelText("1.5 - Custom (optional)").select(["Example Custom 1", "Example Custom 2", "Example Custom 3"]);
    cy.findByLabelText("1.6 - Processes (optional)").select(["Example Process 1", "Example Process 2"]);
    cy.fillForm({
      "1.7 - Constraint (Sum of materials used for formulation) (kg) *": 100,
    });

    cy.findByText("4 - Configure weights for each material type").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/formulations/add_min_max_entries");

    // Fill in the increment, min, max values
    cy.fillForm({
      "Increment (kg)": [5, 5, 5, 5],
      "Min (kg)": [20, 20, 20, 20],
      "Max (kg)": [20, 20, 20, 20],
    });
    // Check the autocompletion feature
    cy.findAllByLabelText("Min (kg)").last().should("have.value", "20.00");
    cy.findAllByLabelText("Max (kg)").last().should("have.value", "20.00");
    cy.clickButtonWaitForAsyncRequest(
      "5 - Show mixture in terms of base material composition",
      "/materials/formulations/add_weights"
    );

    // Check that the configurations were generated correctly
    cy.checkGeneratedConfigurations(["20.0/20.0/20.0/20.0/20.0"]);
    cy.intercept("/materials/formulations/create_formulations_batch").as("create_formulations_batch");
    cy.findByText("6 - Create material formulations for given configuration").click();
    cy.wait("@create_formulations_batch");

    // Check that the materials formulations were generated correctly
    cy.findByText("Show / hide formulations").scrollIntoView();
    cy.findByText("Idx_Sample").should("exist");
    // Check the first 4 columns for every row
    cy.checkGeneratedTable([
      [0, 20.0, 20.0, 20.0],
      [1, 20.0, 20.0, 20.0],
      [2, 20.0, 20.0, 20.0],
      [3, 20.0, 20.0, 20.0],
      [4, 20.0, 20.0, 20.0],
      [5, 20.0, 20.0, 20.0],
    ]);

    // Submit dataset with the default dataset name
    cy.findByText("Submit").click();
  });
});
