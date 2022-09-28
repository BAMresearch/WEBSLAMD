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

describe("Test running experiments with example dataset", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/materials/discovery");
    cy.get("input[type=file]").selectFile("examples/MaterialsDiscoveryExampleData.csv");
    cy.findByText("Upload dataset").click();
    cy.get(".btn-group > div > a").eq(0).click();
    cy.url().should("eq", "http://localhost:5001/materials/discovery/MaterialsDiscoveryExampleData.csv");
  });

  it("One target property works", () => {
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
    cy.intercept("materials/discovery/create_target_configuration_form").as("create_target_configuration_form");
    cy.findByLabelText("Target Properties (select one column at least)").select(["fc 28-d - Target (MPa)"]);
    cy.wait("@create_target_configuration_form");

    // Check that a form appeared
    cy.findAllByLabelText("Maximize").should("have.length", 1);
    cy.findAllByLabelText("Minimize").should("have.length", 1);
    cy.findAllByLabelText("Weight").should("have.length", 1);
    cy.findAllByLabelText("Threshold").should("have.length", 1);

    // Run the experiment, wait for the request to complete
    cy.intercept("materials/discovery/MaterialsDiscoveryExampleData.csv").as("run_experiment");
    cy.findByText("Run experiment with given configuration").click();
    cy.wait("@run_experiment");
    cy.get(".spinner-border").should("not.exist");

    // Check the first three rows for the columns [Row number, Utility, Novelty, fc 28-d - Target (MPa)]
    // while also checking [CO2 (kg/t) - A-priori Information]
    cy.get(".table-responsive")
      .eq(1)
      .scrollIntoView()
      .within(() => {
        cy.findByText(1)
          .next()
          .expectFloatToEqual(2.531052)
          .next()
          .expectFloatToEqual(0.599547)
          .next()
          .expectFloatToEqual(63.442981);
        // This number appears twice
        cy.findAllByText(160.79328);
        cy.findByText(2)
          .next()
          .expectFloatToEqual(2.372714)
          .next()
          .expectFloatToEqual(0.620889)
          .next()
          .expectFloatToEqual(59.014729);
        cy.findByText(164.35337);
        cy.findByText(3)
          .next()
          .expectFloatToEqual(2.243499)
          .next()
          .expectFloatToEqual(0.523664)
          .next()
          .expectFloatToEqual(59.452994);
        cy.findAllByText(160.79328);
      });
  });

  it("One target property and one a priori information maximized works", () => {
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
    cy.intercept("materials/discovery/create_target_configuration_form").as("create_target_configuration_form");
    cy.findByLabelText("Target Properties (select one column at least)").select(["fc 28-d - Target (MPa)"]);
    cy.wait("@create_target_configuration_form");

    // Check that a form appeared
    cy.findAllByLabelText("Maximize").should("have.length", 1);
    cy.findAllByLabelText("Minimize").should("have.length", 1);
    cy.findAllByLabelText("Weight").should("have.length", 1);
    cy.findAllByLabelText("Threshold").should("have.length", 1);

    // Select a priori information
    cy.intercept("materials/discovery/create_a_priori_information_configuration_form").as(
      "create_a_priori_information_configuration_form"
    );
    cy.findByLabelText("A priori Information (optional)").select(["CO2 (kg/t) - A-priori Information"]);
    cy.wait("@create_a_priori_information_configuration_form");

    // Check that a second form appeared
    cy.findAllByLabelText("Maximize").should("have.length", 2);
    cy.findAllByLabelText("Minimize").should("have.length", 2);
    cy.findAllByLabelText("Weight").should("have.length", 2);
    cy.findAllByLabelText("Threshold").should("have.length", 2);

    // Run the experiment, wait for the request to complete
    cy.intercept("materials/discovery/MaterialsDiscoveryExampleData.csv").as("run_experiment");
    cy.findByText("Run experiment with given configuration").click();
    cy.wait("@run_experiment");
    cy.get(".spinner-border").should("not.exist");

    // Check the first three rows for the columns [Row number, Utility, Novelty, fc 28-d - Target (MPa)]
    // while also checking [CO2 (kg/t) - A-priori Information]
    cy.get(".table-responsive")
      .eq(1)
      .scrollIntoView()
      .within(() => {
        cy.findByText(1)
          .next()
          .expectFloatToEqual(4.048724)
          .next()
          .expectFloatToEqual(0.620889)
          .next()
          .expectFloatToEqual(59.014729);
        cy.findByText(164.35337);
        cy.findByText(2)
          .next()
          .expectFloatToEqual(4.037003)
          .next()
          .expectFloatToEqual(0.789527)
          .next()
          .expectFloatToEqual(54.640386);
        cy.findByText(167.90098);
        cy.findByText(3)
          .next()
          .expectFloatToEqual(3.954029)
          .next()
          .expectFloatToEqual(0.599547)
          .next()
          .expectFloatToEqual(63.442981);
        // This number appears twice
        cy.findAllByText(160.79328);
      });
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
    cy.intercept("materials/discovery/create_target_configuration_form").as("create_target_configuration_form");
    cy.findByLabelText("Target Properties (select one column at least)").select(["fc 28-d - Target (MPa)"]);
    cy.wait("@create_target_configuration_form");

    // Check that a form appeared
    cy.findAllByLabelText("Maximize").should("have.length", 1);
    cy.findAllByLabelText("Minimize").should("have.length", 1);
    cy.findAllByLabelText("Weight").should("have.length", 1);
    cy.findAllByLabelText("Threshold").should("have.length", 1);

    // Select a priori information
    cy.intercept("materials/discovery/create_a_priori_information_configuration_form").as(
      "create_a_priori_information_configuration_form"
    );
    cy.findByLabelText("A priori Information (optional)").select(["CO2 (kg/t) - A-priori Information"]);
    cy.wait("@create_a_priori_information_configuration_form");

    // Check that a second form appeared
    cy.findAllByLabelText("Maximize").should("have.length", 2);
    cy.findAllByLabelText("Minimize").should("have.length", 2);
    cy.findAllByLabelText("Weight").should("have.length", 2);
    cy.findAllByLabelText("Threshold").should("have.length", 2);

    // Minimize CO2
    cy.findAllByLabelText("Minimize").eq(1).check();

    // Run the experiment, wait for the request to complete
    cy.intercept("materials/discovery/MaterialsDiscoveryExampleData.csv").as("run_experiment");
    cy.findByText("Run experiment with given configuration").click();
    cy.wait("@run_experiment");
    cy.get(".spinner-border").should("not.exist");

    // Check the first three rows for the columns [Row number, Utility, Novelty, fc 28-d - Target (MPa)]
    // while also checking [CO2 (kg/t) - A-priori Information]
    cy.get(".table-responsive")
      .eq(1)
      .scrollIntoView()
      .within(() => {
        cy.findByText(1)
          .next()
          .expectFloatToEqual(3.831002)
          .next()
          .expectFloatToEqual(0.224525)
          .next()
          .expectFloatToEqual(64.10796);
        // This number appears twice
        cy.findAllByText(116.12407);
        cy.findByText(2)
          .next()
          .expectFloatToEqual(3.83015)
          .next()
          .expectFloatToEqual(0.224525)
          .next()
          .expectFloatToEqual(64.099414);
        cy.findAllByText(116.12407);
        cy.findByText(3)
          .next()
          .expectFloatToEqual(3.424517)
          .next()
          .expectFloatToEqual(0.311907)
          .next()
          .expectFloatToEqual(57.296066);
        // This number appears twice
        cy.findAllByText(114.39607);
      });
  });

  it("Two target properties and one a priori information minimized works", () => {
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
    cy.intercept("materials/discovery/create_target_configuration_form").as("create_target_configuration_form");
    cy.findByLabelText("Target Properties (select one column at least)").select([
      "fc 28-d - Target (MPa)",
      "Slump - Target (mm)",
    ]);
    cy.wait("@create_target_configuration_form");

    // Check that two forms appeared
    cy.findAllByText("Maximize").should("have.length", 2);
    cy.findAllByText("Minimize").should("have.length", 2);
    cy.findAllByLabelText("Weight").should("have.length", 2);
    cy.findAllByLabelText("Threshold").should("have.length", 2);

    // Select a priori information
    cy.intercept("materials/discovery/create_a_priori_information_configuration_form").as(
      "create_a_priori_information_configuration_form"
    );
    cy.findByLabelText("A priori Information (optional)").select(["CO2 (kg/t) - A-priori Information"]);
    cy.wait("@create_a_priori_information_configuration_form");

    // Check that a third form appeared
    cy.findAllByText("Maximize").should("have.length", 3);
    cy.findAllByText("Minimize").should("have.length", 3);
    cy.findAllByLabelText("Weight").should("have.length", 3);
    cy.findAllByLabelText("Threshold").should("have.length", 3);

    // Minimize CO2
    cy.findAllByLabelText("Minimize").eq(2).check();

    // Run the experiment, wait for the request to complete
    cy.intercept("materials/discovery/MaterialsDiscoveryExampleData.csv").as("run_experiment");
    cy.findByText("Run experiment with given configuration").click();
    cy.wait("@run_experiment");
    cy.get(".spinner-border").should("not.exist");

    // Check the first three rows for the columns [Row number, Utility, Novelty, Slump - Target (mm)]
    // while also checking [CO2 (kg/t) - A-priori Information]
    cy.get(".table-responsive")
      .eq(1)
      .scrollIntoView()
      .within(() => {
        cy.findByText(1)
          .next()
          .expectFloatToEqual(6.061092)
          .next()
          .expectFloatToEqual(0.224525)
          .next()
          .expectFloatToEqual(181.669628);
        // This number appears twice
        cy.findAllByText(116.12407);
        cy.findByText(2)
          .next()
          .expectFloatToEqual(6.057715)
          .next()
          .expectFloatToEqual(0.224525)
          .next()
          .expectFloatToEqual(181.588483);
        cy.findAllByText(116.12407);
        cy.findByText(3)
          .next()
          .expectFloatToEqual(5.137301)
          .next()
          .expectFloatToEqual(0.311907)
          .next()
          .expectFloatToEqual(151.522781);
        // This number appears twice
        cy.findAllByText(114.39607);
      });
  });
});
