describe('Test base materials page', () => {
    beforeEach(() => {
        // Cypress starts out with a blank slate for each test
        // so we must tell it to visit our website with the `cy.visit()` command.
        // Since we want to visit the same URL at the start of all our tests,
        // we include it in our beforeEach function so that it runs before each test
        cy.visit('http://localhost:5001/')
    })

    it('Material types are listed correctly', () => {
        cy.findByText("Powder").should("exist")
        cy.findByLabelText("Material type / Process").select("Powder")
        cy.findByLabelText("Material type / Process").select("Liquid")
        cy.findByLabelText("Material type / Process").select("Aggregates")
        cy.findByLabelText("Material type / Process").select("Aggregates")
        cy.findByLabelText("Material type / Process").select("Admixture")
        cy.findByLabelText("Material type / Process").select("Process")
        cy.findByLabelText("Material type / Process").select("Custom")
        cy.findByLabelText("Material type / Process").select("Powder")
    })

    it('Create powder', () => {
        // Fill out name and material type
        cy.findByLabelText("Name").type("My Powder")
        cy.findByLabelText("Material type / Process").select("Powder")

        // Fill out cost properties
        cy.findByText("Cost").click()
        cy.findByLabelText("CO₂ footprint (kg)").type("12.34")
        cy.findByLabelText("Costs (€/kg)").type("34.56")
        cy.findByLabelText("Delivery time (days)").type("56.78")

        // Fill out composition properties
        cy.findByText("Composition").click()
        cy.findByText("Molecular composition").scrollIntoView()
        cy.findByLabelText("Fe₂O₃ (m%)").type("12.3")
        cy.findByLabelText("SiO₂ (m%)").type("23.4")
        cy.findByLabelText("Al₂O₃ (m%)").type("34.5")
        cy.findByLabelText("CaO (m%)").type("45.6")
        cy.findByLabelText("MgO (m%)").type("56.7")
        cy.findByLabelText("Na₂O (m%)").type("67.8")
        cy.findByLabelText("K₂O (m%)").type("78.9")
        cy.findByLabelText("SO₃ (m%)").type("89.0")
        cy.findByLabelText("P₂O₅ (m%)").type("0.98")
        cy.findByLabelText("TiO₂ (m%)").type("9.87")
        cy.findByLabelText("SrO (m%)").type("8.76")
        cy.findByLabelText("Mn₂O₃ (m%)").type("7.65")

        // Fill out structural composition properties
        cy.findByText("Structural composition").should("exist")
        cy.findByLabelText("Fine modules (m2/kg)").type("123.45")
        cy.findByLabelText("Specific gravity (m%)").type("67.890")

        // Fill out additional properties
        cy.findByText("Additional Properties - Leave empty if not needed.").click().scrollIntoView()
        cy.findByText("Add property").click()
        cy.findAllByLabelText("Name").last().type("Prop 0")
        cy.findAllByLabelText("Value").last().type("Value 0")
        cy.findByText("Add property").click()
        cy.findAllByLabelText("Name").last().type("Prop 1")
        cy.findAllByLabelText("Value").last().type("Value 1")

        // Save material and check that it is listed
        cy.findByText("Save material").click()
        cy.findByText("All base materials").should("exist")
        cy.findByText("My Powder").should("exist")
    })
})

