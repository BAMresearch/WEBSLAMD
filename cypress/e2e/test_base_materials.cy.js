describe("Test creating base materials", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/materials/base");
  });

  it("Material types are listed correctly", () => {
    cy.findByText("Powder").should("exist");
    cy.findByLabelText("2 - Material type / Process").select("Powder");
    cy.findByLabelText("2 - Material type / Process").select("Liquid");
    cy.findByLabelText("2 - Material type / Process").select("Aggregates");
    cy.findByLabelText("2 - Material type / Process").select("Admixture");
    cy.findByLabelText("2 - Material type / Process").select("Process");
    cy.findByLabelText("2 - Material type / Process").select("Custom");
    cy.findByLabelText("2 - Material type / Process").select("Powder");
  });

  it("Create powder", () => {
    // Fill out name and material type
    cy.findByLabelText("1 - Name").type("My Powder");
    cy.findByLabelText("2 - Material type / Process").select("Powder");

    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.findByLabelText("CO₂ footprint (kg/ton)").type("12.34");
    cy.findByLabelText("Costs (€/kg)").type("34.56");
    cy.findByLabelText("Delivery time (days)").type("56.78");

    // Fill out composition properties
    cy.findByText("4 - Composition").click();
    cy.findByText("Molecular composition").scrollIntoView();
    cy.findByLabelText("Fe₂O₃ (m%)").type("12.3");
    cy.findByLabelText("SiO₂ (m%)").type("23.4");
    cy.findByLabelText("Al₂O₃ (m%)").type("34.5");
    cy.findByLabelText("CaO (m%)").type("45.6");
    cy.findByLabelText("MgO (m%)").type("56.7");
    cy.findByLabelText("Na₂O (m%)").type("67.8");
    cy.findByLabelText("K₂O (m%)").type("78.9");
    cy.findByLabelText("SO₃ (m%)").type("89.0");
    cy.findByLabelText("P₂O₅ (m%)").type("0.98");
    cy.findByLabelText("TiO₂ (m%)").type("9.87");
    cy.findByLabelText("SrO (m%)").type("8.76");
    cy.findByLabelText("Mn₂O₃ (m%)").type("7.65");
    cy.findByLabelText("LOI (m%)").type("1.65");

    // Fill out structural composition properties
    cy.findByText("Structural composition").should("exist");
    cy.findByLabelText("Fine modules (m²/kg)").type("123.45");
    cy.findByLabelText("Specific gravity (m%)").type("67.890");

    // Fill out additional properties
    cy.intercept("/materials/base/add_property").as("add_property");
    cy.findByText("5 - Additional Properties - Leave empty if not needed.").click().scrollIntoView();
    cy.findByText("Add property").click();
    cy.wait("@add_property");
    cy.findAllByLabelText("Name").last().type("Prop 0");
    cy.findAllByLabelText("Value").last().type("Value 0");
    cy.findByText("Add property").click();
    cy.wait("@add_property");
    cy.findAllByLabelText("Name").last().type("Prop 1");
    cy.findAllByLabelText("Value").last().type("Value 1");

    // Save material and check that it is listed
    cy.findByText("6 - Save material/process").click();
    cy.findByText("All base materials / processes").should("exist");
    cy.findByText("My Powder").should("exist");
  });

  it("Create process", () => {
    // Fill out name and material type
    cy.findByLabelText("1 - Name").type("My Process");
    cy.findByLabelText("2 - Material type / Process").select("Process");

    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.findByLabelText("CO₂ footprint (kg/ton)").type("12.34");
    cy.findByLabelText("Costs (€/kg)").type("34.56");

    // Fill out process information properties
    cy.findByText("4 - Composition").should("not.exist");
    cy.findByText("4 - Process Information").click();
    cy.findByLabelText("Duration (days)").type("12.3");
    cy.findByLabelText("Temperature (°C)").type("23.4");
    cy.findByLabelText("Relative Humidity (%)").type("34.5");

    // Save material and check that it is listed
    cy.findByText("6 - Save material/process").click();
    cy.findByText("All base materials / processes").should("exist");
    cy.findByText("My Process").should("exist");
  });

  it("Create custom", () => {
    // Fill out name and material type
    cy.findByLabelText("1 - Name").type("My Custom Material");
    cy.findByLabelText("2 - Material type / Process").select("Custom");

    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.findByLabelText("CO₂ footprint (kg/ton)").type("12.34");
    cy.findByLabelText("Costs (€/kg)").type("34.56");
    cy.findByLabelText("Delivery time (days)").type("56.78");

    // No properties for Custom
    cy.findByText("4 - Composition").should("not.exist");

    // Fill out additional properties
    cy.intercept("/materials/base/add_property").as("add_property");
    cy.findByText("4 - Additional Properties - Leave empty if not needed.").click().scrollIntoView();
    cy.findByText("Add property").click();
    cy.wait("@add_property");
    cy.findAllByLabelText("Name").last().type("Prop 0");
    cy.findAllByLabelText("Value").last().type("Value 0");
    cy.findByText("Add property").click();
    cy.wait("@add_property");
    cy.findAllByLabelText("Name").last().type("Prop 1");
    cy.findAllByLabelText("Value").last().type("Value 1");
    cy.findByText("Add property").click();
    cy.wait("@add_property");
    cy.findAllByLabelText("Name").last().type("Prop 2");
    cy.findAllByLabelText("Value").last().type("Value 2");

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
    cy.findByText("6 - Save material/process").click();
    cy.findByText("All base materials / processes").should("exist");
    cy.findByText("My Custom Material").should("exist");
  });

  it("Create admixture", () => {
    // Fill out name and material type
    cy.findByLabelText("1 - Name").type("My Admixture");
    cy.findByLabelText("2 - Material type / Process").select("Admixture");

    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.findByLabelText("CO₂ footprint (kg/ton)").type("12.34");
    cy.findByLabelText("Costs (€/kg)").type("34.56");
    cy.findByLabelText("Delivery time (days)").type("56.78");

    // No properties for Admixture
    cy.findByText("4 - Composition").should("not.exist");

    // Fill out additional properties
    cy.findByText("4 - Additional Properties - Leave empty if not needed.").click().scrollIntoView();
    cy.findByText("Add property").click();
    cy.findAllByLabelText("Name").last().type("Prop 0");
    cy.findAllByLabelText("Value").last().type("Value 0");
    cy.findByText("Add property").click();
    cy.findAllByLabelText("Name").last().type("Prop 1");
    cy.findAllByLabelText("Value").last().type("Value 1");
    cy.findByText("Add property").click();
    cy.findAllByLabelText("Name").last().type("Prop 2");
    cy.findAllByLabelText("Value").last().type("Value 2");

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
    cy.findByText("6 - Save material/process").click();
    cy.findByText("All base materials / processes").should("exist");
    cy.findByText("My Admixture").should("exist");
  });

  it("Delivery time is corrected automatically", () => {
    // Fill out cost properties
    cy.findByText("3 - Cost").click();
    cy.findByLabelText("Delivery time (days)").type("123");
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
    cy.findByText("Example Powder 1").should("exist");
    cy.findByText("Example Powder 2").should("exist");
  });

  it("Can delete two powders", () => {
    cy.get(".btn-group > div > button").eq(0).click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findAllByText("Confirm").first().click();
    // Check that the table entry was deleted
    cy.get(".btn-group > div > button").should("have.length", 1);
    cy.get(".btn-group > div > button").eq(0).click();
    // Wait for the modal animation to finish
    cy.wait(400);
    cy.findAllByText("Confirm").first().click();
  });
});
