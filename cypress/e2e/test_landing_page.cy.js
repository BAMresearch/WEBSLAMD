describe("Test landing page", () => {
  beforeEach(() => {
    // Cypress starts out with a blank slate for each test
    // so we must tell it to visit our website with the `cy.visit()` command.
    // Since we want to visit the same URL at the start of all our tests,
    // we include it in our beforeEach function so that it runs before each test
    cy.visit("http://localhost:5001/");
  });

  it("Page loads", () => {
    cy.title().should("contain", "SLAMD - Sequential Learning App for Materials Discovery");
    cy.findAllByText("SLAMD Dashboard").should("have.length", 2);
    cy.url().should("eq", "http://localhost:5001/");
    cy.findByText("Base").should("exist");
    cy.findByText("Blend").should("exist");
    cy.findByText("Formulations").should("exist");
    cy.findByText("Materials Discovery").should("exist");
  });

  it("Link to GitHub repo is present", () => {
    cy.findByText("GitHub Repository").should(($a) => {
      expect($a.attr("href"), "href").to.contain("github.com");
      expect($a.attr("target"), "target").to.equal("_blank");
    });
  });

  it("Link to BAM website is present", () => {
    cy.findByText("BAM website").should(($a) => {
      expect($a.attr("href"), "href").to.contain("bam.de");
      expect($a.attr("target"), "target").to.equal("_blank");
    });
  });

  it("Link to User Manual is present", () => {
    cy.findByText("User Manual").should(($a) => {
      expect($a.attr("href"), "href").to.contain("/static/SLAMD-UserManual.pdf");
      expect($a.attr("target"), "target").to.equal("_blank");
    });
  });

  it("Link to iteratec website is present", () => {
    cy.findByText("Powered by iteratec").should(($a) => {
      expect($a.attr("href"), "href").to.contain("iteratec.com");
      expect($a.attr("target"), "target").to.equal("_blank");
    });
  });
});
