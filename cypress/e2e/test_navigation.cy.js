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
    cy.url().should("eq", "http://localhost:5001/materials/formulations/concrete");
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

  it("Go to formulations concrete page", () => {
    cy.get("nav").within(() => {
      cy.get("a > .bi-list").click();
    });
    cy.findByText("Formulations - Concrete").click();
    cy.url().should("eq", "http://localhost:5001/materials/formulations/concrete");
  });

  it("Go to formulations binder page", () => {
    cy.get("nav").within(() => {
      cy.get("a > .bi-list").click();
    });
    cy.findByText("Formulations - Binder").click();
    cy.url().should("eq", "http://localhost:5001/materials/formulations/binder");
  });

  it("Go to discovery page", () => {
    cy.get("nav").within(() => {
      cy.get("a > .bi-list").click();
    });
    cy.findAllByText("Discovery").last().click();
    cy.url().should("eq", "http://localhost:5001/materials/discovery");
  });
});
