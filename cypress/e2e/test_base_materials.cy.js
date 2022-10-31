describe("Test creating base materials", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/materials/base");
  });

  it("Material types are listed correctly", () => {
    cy.findByText("Powder").should("exist");
    cy.findByLabelText("2 - Material type / Process *").select("Powder").should("have.value", "Powder");
    cy.findByLabelText("2 - Material type / Process *").select("Liquid").should("have.value", "Liquid");
    cy.findByLabelText("2 - Material type / Process *").select("Aggregates").should("have.value", "Aggregates");
    cy.findByLabelText("2 - Material type / Process *").select("Admixture").should("have.value", "Admixture");
    cy.findByLabelText("2 - Material type / Process *").select("Process").should("have.value", "Process");
    cy.findByLabelText("2 - Material type / Process *").select("Custom").should("have.value", "Custom");
    cy.findByLabelText("2 - Material type / Process *").select("Powder").should("have.value", "Powder");
  });

  it("Create powder", () => {
    // Fill out name and material type
    cy.findByLabelText("1 - Name *").type("My Powder").should("have.value", "My Powder");

    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.fillForm({
      "CO₂ footprint (kg/ton)": "12.34",
      "Costs (€/ton)": "34.56",
      "Delivery time (days)": "56.78",
    });

    // Fill out composition properties
    cy.findByText("4 - Composition").click();
    cy.findByText("Molecular composition").scrollIntoView();
    cy.fillForm({
      "Fe₂O₃ (m%)": "12.3",
      "SiO₂ (m%)": "23.4",
      "Al₂O₃ (m%)": "34.5",
      "CaO (m%)": "45.6",
      "MgO (m%)": "56.7",
      "Na₂O (m%)": "67.8",
      "K₂O (m%)": "78.9",
      "SO₃ (m%)": "89.0",
      "P₂O₅ (m%)": "0.98",
      "TiO₂ (m%)": "9.87",
      "SrO (m%)": "8.76",
      "Mn₂O₃ (m%)": "7.65",
      "LOI (m%)": "1.65",
    });

    // Fill out structural composition properties
    cy.findByText("Structural composition").should("exist");
    cy.fillForm({
      "Fine modules (m²/kg)": "123.45",
      "Specific gravity (m%)": "67.890",
    });

    // Fill out additional properties
    cy.findByText("5 - Additional Properties - Leave empty if not needed.").click().scrollIntoView();
    cy.clickButtonWaitForAsyncRequest("Add property", "/materials/base/add_property");
    cy.clickButtonWaitForAsyncRequest("Add property", "/materials/base/add_property");
    cy.findAllByLabelText("Name").should("have.length", 2);
    cy.fillForm({
      Name: ["Prop 0", "Prop 1"],
      Value: ["Value 0", "Value 1"],
    });

    // Save material and check that it is listed
    cy.findByText("Submit").click();
    cy.findByText("All base materials / processes").should("exist");
    cy.findByText("My Powder").should("exist");
  });

  it("Create process", () => {
    // Fill out name and material type
    cy.findByLabelText("1 - Name *").type("My Process").should("have.value", "My Process");
    cy.selectInputWaitForAsyncRequest("2 - Material type / Process *", "Process", "/materials/base/process");

    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.fillForm({
      "CO₂ footprint (kg)": "12.34",
      "Costs (€)": "34.56",
    });

    // Fill out process information properties
    cy.findByText("4 - Composition").should("not.exist");
    cy.findByText("4 - Process Information").click();
    cy.fillForm({
      "Duration (days)": "12.3",
      "Temperature (°C)": "23.4",
      "Relative Humidity (%)": "34.5",
    });

    // Save material and check that it is listed
    cy.findByText("Submit").click();
    cy.findByText("All base materials / processes").should("exist");
    cy.findByText("My Process").should("exist");
  });

  it("Create custom", () => {
    // Fill out name and material type
    cy.findByLabelText("1 - Name *").type("My Custom Material").should("have.value", "My Custom Material");
    cy.selectInputWaitForAsyncRequest("2 - Material type / Process *", "Custom", "/materials/base/custom");

    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.fillForm({
      "CO₂ footprint (kg/ton)": "12.34",
      "Costs (€/ton)": "34.56",
      "Delivery time (days)": "56.78",
    });

    // No properties for Custom
    cy.findByText("4 - Composition").should("not.exist");

    // Fill out additional properties
    cy.findByText("4 - Additional Properties - Leave empty if not needed.").click().scrollIntoView();
    cy.clickButtonWaitForAsyncRequest("Add property", "/materials/base/add_property");
    cy.clickButtonWaitForAsyncRequest("Add property", "/materials/base/add_property");
    cy.clickButtonWaitForAsyncRequest("Add property", "/materials/base/add_property");
    cy.findAllByLabelText("Name").should("have.length", 3);
    cy.fillForm({
      Name: ["Prop 0", "Prop 1", "Prop 2"],
      Value: ["Value 0", "Value 1", "Value 2"],
    });

    // Delete additional properties one by one
    cy.findByText("Delete last property").click();
    cy.findByText("Prop 2").should("not.exist");
    cy.findByText("Value 2").should("not.exist");
    cy.findByText("Delete last property").click();
    cy.findByText("Prop 1").should("not.exist");
    cy.findByText("Value 1").should("not.exist");
    cy.findByText("Delete last property").click();
    cy.findByText("Prop 0").should("not.exist");
    cy.findByText("Value 0").should("not.exist");

    // Save material and check that it is listed
    cy.findByText("Submit").click();
    cy.findByText("All base materials / processes").should("exist");
    cy.findByText("My Custom Material").should("exist");
  });

  it("Create admixture", () => {
    // Fill out name and material type
    cy.findByLabelText("1 - Name *").type("My Admixture").should("have.value", "My Admixture");
    cy.selectInputWaitForAsyncRequest("2 - Material type / Process *", "Admixture", "/materials/base/admixture");

    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.fillForm({
      "CO₂ footprint (kg/ton)": "12.34",
      "Costs (€/ton)": "34.56",
      "Delivery time (days)": "56.78",
    });

    // No properties for Admixture
    cy.findByText("4 - Composition").should("not.exist");

    // Fill out additional properties
    cy.findByText("4 - Additional Properties - Leave empty if not needed.").click().scrollIntoView();
    cy.clickButtonWaitForAsyncRequest("Add property", "/materials/base/add_property");
    cy.clickButtonWaitForAsyncRequest("Add property", "/materials/base/add_property");
    cy.clickButtonWaitForAsyncRequest("Add property", "/materials/base/add_property");
    cy.findAllByLabelText("Name").should("have.length", 3);
    cy.fillForm({
      Name: ["Prop 0", "Prop 1", "Prop 2"],
      Value: ["Value 0", "Value 1", "Value 2"],
    });

    // Delete additional properties one by one
    cy.findByText("Delete last property").click();
    cy.findByText("Prop 2").should("not.exist");
    cy.findByText("Value 2").should("not.exist");
    cy.findByText("Delete last property").click();
    cy.findByText("Prop 1").should("not.exist");
    cy.findByText("Value 1").should("not.exist");
    cy.findByText("Delete last property").click();
    cy.findByText("Prop 0").should("not.exist");
    cy.findByText("Value 0").should("not.exist");

    // Save material and check that it is listed
    cy.findByText("Submit").click();
    cy.findByText("All base materials / processes").should("exist");
    cy.findByText("My Admixture").should("exist");
  });

  it("Delivery time is corrected automatically", () => {
    // Fill out cost properties
    cy.wait(500).findByText("3 - Cost").click();
    cy.findByLabelText("Delivery time (days)").type("123").should("have.value", "123");
    cy.findByLabelText("Delivery time (days)").type("{moveToStart}-");
    cy.findByLabelText("Delivery time (days)").should("have.value", 0);
    cy.findByLabelText("Delivery time (days)").clear().type("-0.2");
    cy.findByLabelText("Delivery time (days)").should("have.value", 0);
  });
});

describe("Test deleting base materials", () => {
  beforeEach(() => {
    cy.createExamplePowders();
    cy.visit("http://localhost:5001/materials/base");
  });

  it("Can delete two powders", () => {
    cy.findByText("Example Powder 1").should("exist");
    cy.findByText("Example Powder 2").should("exist");

    cy.get(".btn-group > div > button").eq(0).click();
    // Wait for the modal animation to finish
    cy.wait(500);
    cy.findAllByText("Confirm").filter(':visible').click();
    // Check that the table entry was deleted
    cy.get(".btn-group > div > button").should("have.length", 1);
    cy.get(".btn-group > div > button").eq(0).click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findAllByText("Confirm").filter(':visible').click();
  });
});
