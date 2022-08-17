describe("Test landing page", () => {
  beforeEach(() => {
    // Cypress starts out with a blank slate for each test
    // so we must tell it to visit our website with the `cy.visit()` command.
    // Since we want to visit the same URL at the start of all our tests,
    // we include it in our beforeEach function so that it runs before each test
    cy.visit("http://localhost:5001/")
  })

  it("Page loads", () => {
    cy.title().should("contain", "SLAMD - Sequential Learning App for Materials Discovery")
    cy.findAllByText("SLAMD Dashboard").should("have.length", 2)
    cy.url().should('eq', 'http://localhost:5001/')
    cy.findByText("Step 1: Define base materials and processes").should("exist")
    cy.findByText("Step 2: Blend base materials to create blended materials").should("exist")
  })
})
