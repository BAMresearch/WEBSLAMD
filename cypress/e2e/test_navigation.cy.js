describe("Test navigation bar", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/");
  });

  it("Go to base materials page", () => {
    cy.get("nav").within(() => {
      cy.findByText("Base").click();
    });
    cy.url().should("eq", "http://localhost:5001/materials/base");
  });

  it("Go to blended materials page", () => {
    cy.get("nav").within(() => {
      cy.findByText("Blend").click();
    });
    cy.url().should("eq", "http://localhost:5001/materials/blended");
  });

  it("Go to formulations page", () => {
    cy.get("nav").within(() => {
      cy.findByText("Formulations").click();
    });
    cy.url().should("eq", "http://localhost:5001/materials/formulations");
  });

  it("Go to discovery page", () => {
    cy.get("nav").within(() => {
      cy.findByText("Discovery").click();
    });
    cy.url().should("eq", "http://localhost:5001/materials/discovery");
  });
});

describe("Test navigation sidebar", () => {
  beforeEach(() => {
    cy.visit("http://localhost:5001/");
  });

  it("Go to base materials page", () => {
    cy.get("nav").within(() => {
      cy.get("a > .bi-list").click();
    });
    cy.findAllByText("Base").last().click();
    cy.url().should("eq", "http://localhost:5001/materials/base");
  });

  it("Go to blended materials page", () => {
    cy.get("nav").within(() => {
      cy.get("a > .bi-list").click();
    });
    cy.findAllByText("Blend").last().click();
    cy.url().should("eq", "http://localhost:5001/materials/blended");
  });

  it("Go to formulations page", () => {
    cy.get("nav").within(() => {
      cy.get("a > .bi-list").click();
    });
    cy.findAllByText("Formulations").last().click();
    cy.url().should("eq", "http://localhost:5001/materials/formulations");
  });

  it("Go to discovery page", () => {
    cy.get("nav").within(() => {
      cy.get("a > .bi-list").click();
    });
    cy.findAllByText("Discovery").last().click();
    cy.url().should("eq", "http://localhost:5001/materials/discovery");
  });
});
