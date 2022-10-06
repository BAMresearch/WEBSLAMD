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
    cy.findByLabelText("1.7 - Constraint (Sum of materials used for formulation) (kg) *")
      .type("100")
      .should("have.value", "100");

    cy.findByText("4 - Configure weights for each material type").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/formulations/add_min_max_entries");

    // Fill in the increment, min, max values
    cy.findAllByLabelText("Increment (kg)").first().type(30).should("have.value", 30);
    cy.findAllByLabelText("Min (kg)").first().type(10).should("have.value", 10);
    cy.findAllByLabelText("Max (kg)").first().type(70).should("have.value", 70);
    cy.findAllByLabelText("Increment (kg)").eq(1).type(15).should("have.value", 15);
    cy.findAllByLabelText("Min (kg)").eq(1).type(5).should("have.value", 5);
    cy.findAllByLabelText("Max (kg)").eq(1).type(25).should("have.value", 25);
    // Check the autocompletion feature
    cy.findAllByLabelText("Min (kg)").last().should("have.value", "85.00");
    cy.findAllByLabelText("Max (kg)").last().should("have.value", "5.00");
    cy.clickButtonWaitForAsyncRequest(
      "5 - Show mixture in terms of base material composition",
      "/materials/formulations/add_weights"
    );

    // Check that the configurations were generated correctly
    cy.findByDisplayValue("10.0/5.0/85.0").should("exist");
    cy.findByDisplayValue("10.0/20.0/70.0").should("exist");
    cy.findByDisplayValue("40.0/5.0/55.0").should("exist");
    cy.findByDisplayValue("40.0/20.0/40.0").should("exist");
    cy.findByDisplayValue("70.0/5.0/25.0").should("exist");
    cy.findByDisplayValue("70.0/20.0/10.0").should("exist");
    cy.intercept("/materials/formulations/create_formulations_batch").as("create_formulations_batch");
    cy.findByText("6 - Create material formulations for given configuration").click();
    cy.wait("@create_formulations_batch");

    // Check that the materials formulations were generated correctly
    cy.findByText("Show / hide formulations").scrollIntoView();
    cy.findByText("Idx_Sample").should("exist");
    // Check the first 4 columns for every row
    cy.findByText(0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(5.0).next().expectFloatToEqual(85.0);
    cy.findByText(1).next().expectFloatToEqual(10.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(70.0);
    cy.findByText(2).next().expectFloatToEqual(40.0).next().expectFloatToEqual(5.0).next().expectFloatToEqual(55.0);
    cy.findByText(3).next().expectFloatToEqual(40.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(40.0);
    cy.findByText(4).next().expectFloatToEqual(70.0).next().expectFloatToEqual(5.0).next().expectFloatToEqual(25.0);
    cy.findByText(5).next().expectFloatToEqual(70.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0);

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
    cy.findByLabelText("1.7 - Constraint (Sum of materials used for formulation) (kg) *")
      .type("100")
      .should("have.value", "100");

    cy.findByText("4 - Configure weights for each material type").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/formulations/add_min_max_entries");

    // Fill in the increment, min, max values
    cy.findAllByLabelText("Increment (kg)").first().type(40).should("have.value", 40);
    cy.findAllByLabelText("Min (kg)").first().type(20).should("have.value", 20);
    cy.findAllByLabelText("Max (kg)").first().type(60).should("have.value", 60);
    cy.findAllByLabelText("Increment (kg)").eq(1).type(10).should("have.value", 10);
    cy.findAllByLabelText("Min (kg)").eq(1).type(10).should("have.value", 10);
    cy.findAllByLabelText("Max (kg)").eq(1).type(10).should("have.value", 10);
    // Check the autocompletion feature
    cy.findAllByLabelText("Min (kg)").last().should("have.value", "70.00");
    cy.findAllByLabelText("Max (kg)").last().should("have.value", "30.00");
    cy.clickButtonWaitForAsyncRequest(
      "5 - Show mixture in terms of base material composition",
      "/materials/formulations/add_weights"
    );

    // Check that the configurations were generated correctly
    cy.findByDisplayValue("20.0/10.0/70.0").should("exist");
    cy.findByDisplayValue("60.0/10.0/30.0").should("exist");
    cy.intercept("/materials/formulations/create_formulations_batch").as("create_formulations_batch");
    cy.findByText("6 - Create material formulations for given configuration").click();
    cy.wait("@create_formulations_batch");

    // Check that the materials formulations were generated correctly
    cy.findByText("Show / hide formulations").scrollIntoView();
    cy.findByText("Idx_Sample").should("exist");
    // Check the first 4 columns for every row
    cy.findByText(0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(70.0);
    cy.findByText(1).next().expectFloatToEqual(60.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(30.0);
    cy.findByText(2).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(70.0);
    cy.findByText(3).next().expectFloatToEqual(60.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(30.0);
    cy.findByText(4).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(70.0);
    cy.findByText(5).next().expectFloatToEqual(60.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(30.0);
    cy.findByText(6).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(70.0);
    cy.findByText(7).next().expectFloatToEqual(60.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(30.0);
    cy.findByText(8).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(70.0);
    cy.findByText(9).next().expectFloatToEqual(60.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(30.0);
    cy.findByText(10).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(70.0);
    cy.findByText(11).next().expectFloatToEqual(60.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(30.0);
    cy.findByText(12).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(70.0);
    cy.findByText(13).next().expectFloatToEqual(60.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(30.0);
    cy.findByText(14).next().expectFloatToEqual(20.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(70.0);
    cy.findByText(15).next().expectFloatToEqual(60.0).next().expectFloatToEqual(10.0).next().expectFloatToEqual(30.0);

    // Submit dataset with the default dataset name
    cy.findByText("Submit").click();
  });

  it("Delete formulations and create them again", () => {
    cy.findByLabelText("1.1 - Powders (select one at least)").select("Example Powder 1");
    cy.findByLabelText("1.2 - Liquids (select one at least)").select("Example Liquid 1");
    cy.findByLabelText("1.3 - Aggregates (select one at least)").select("Example Aggregates 1");
    cy.findByLabelText("1.7 - Constraint (Sum of materials used for formulation) (kg) *")
      .type("100")
      .should("have.value", "100");
    cy.findByLabelText("1.8 - Name of the dataset (optional)")
      .type("Example dataset name")
      .should("have.value", "Example dataset name");

    cy.findByText("4 - Configure weights for each material type").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/formulations/add_min_max_entries");

    // Fill in the increment, min, max values
    cy.findAllByLabelText("Increment (kg)").first().type(10).should("have.value", 10);
    cy.findAllByLabelText("Min (kg)").first().type(50).should("have.value", 50);
    cy.findAllByLabelText("Max (kg)").first().type(60).should("have.value", 60);
    cy.findAllByLabelText("Increment (kg)").eq(1).type(10).should("have.value", 10);
    cy.findAllByLabelText("Min (kg)").eq(1).type(40).should("have.value", 40);
    cy.findAllByLabelText("Max (kg)").eq(1).type(40).should("have.value", 40);
    cy.clickButtonWaitForAsyncRequest(
      "5 - Show mixture in terms of base material composition",
      "/materials/formulations/add_weights"
    );

    // Check that the configurations were generated correctly
    cy.findByDisplayValue("50.0/40.0/10.0").should("exist");
    cy.findByDisplayValue("60.0/40.0/0.0").should("exist");
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
    cy.findByText(0).next().expectFloatToEqual(50.0).next().expectFloatToEqual(40.0).next().expectFloatToEqual(10.0);
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
    cy.findByLabelText("1.7 - Constraint (Sum of materials used for formulation) (kg) *")
      .type("100")
      .should("have.value", "100");

    cy.findByText("4 - Configure weights for each material type").click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findByText("Change Selection").should("exist");
    cy.findByText("Do you really want to change the chosen selection?").should("exist");
    cy.findByText("Close").should("exist");
    cy.clickButtonWaitForAsyncRequest("Confirm", "/materials/blended/add_min_max_entries");

    // Fill in the increment, min, max values
    cy.findAllByLabelText("Increment (kg)").first().type(5).should("have.value", 5);
    cy.findAllByLabelText("Min (kg)").first().type(20).should("have.value", 20);
    cy.findAllByLabelText("Max (kg)").first().type(20).should("have.value", 20);
    cy.findAllByLabelText("Increment (kg)").eq(1).type(5).should("have.value", 5);
    cy.findAllByLabelText("Min (kg)").eq(1).type(20).should("have.value", 20);
    cy.findAllByLabelText("Max (kg)").eq(1).type(20).should("have.value", 20);
    cy.findAllByLabelText("Increment (kg)").eq(2).type(5).should("have.value", 5);
    cy.findAllByLabelText("Min (kg)").eq(2).type(20).should("have.value", 20);
    cy.findAllByLabelText("Max (kg)").eq(2).type(20).should("have.value", 20);
    cy.findAllByLabelText("Increment (kg)").eq(3).type(5).should("have.value", 5);
    cy.findAllByLabelText("Min (kg)").eq(3).type(20).should("have.value", 20);
    cy.findAllByLabelText("Max (kg)").eq(3).type(20).should("have.value", 20);
    // Check the autocompletion feature
    cy.findAllByLabelText("Min (kg)").last().should("have.value", "20.00");
    cy.findAllByLabelText("Max (kg)").last().should("have.value", "20.00");
    cy.clickButtonWaitForAsyncRequest(
      "5 - Show mixture in terms of base material composition",
      "/materials/formulations/add_weights"
    );

    // Check that the configurations were generated correctly
    cy.findByDisplayValue("20.0/20.0/20.0/20.0/20.0").should("exist");
    cy.intercept("/materials/formulations/create_formulations_batch").as("create_formulations_batch");
    cy.findByText("6 - Create material formulations for given configuration").click();
    cy.wait("@create_formulations_batch");

    // Check that the materials formulations were generated correctly
    cy.findByText("Show / hide formulations").scrollIntoView();
    cy.findByText("Idx_Sample").should("exist");
    // Check the first 4 columns for every row
    cy.findByText(0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0);
    cy.findByText(1).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0);
    cy.findByText(2).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0);
    cy.findByText(3).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0);
    cy.findByText(4).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0);
    cy.findByText(5).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0).next().expectFloatToEqual(20.0);

    // Submit dataset with the default dataset name
    cy.findByText("Submit").click();
  });
});
