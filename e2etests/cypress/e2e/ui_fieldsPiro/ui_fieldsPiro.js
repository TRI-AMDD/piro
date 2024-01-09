import { Given, When, Then, And } from 'cypress-cucumber-preprocessor/steps';
import "cypress-xpath";

Given('I login the piro website', () => {

cy.visit(Cypress.config().baseUrl)
cy.log('NAVIGATING TO PIRO WEB')
cy.wait(10000)
cy.clearCookies()
cy.get(".login_login__19CNz")
  .should('be.visible')
  .click()
  
cy.get("#signInFormUsername")
  .type(Cypress.config().username,{force: true})

cy.get("#signInFormPassword")
  .type(Cypress.config().password,{force : true})

cy.get('[name="signInSubmitButton"]').eq(1)
  .click()
  
});


Then('target compound field should be available', () => {
  cy.wait(3000)
  cy.verify("target_entry_id")
});


Then('temperature field should be available', () => {
  cy.verify("temperature")
  });

Then('max_component_precursors field should be available', () => {
cy.verify("max_component_precursors")
});  

Then('flexible_competition field should be available', () => {
cy.verify("flexible_competition") 
});  

Then('hull_distance field should be available', () => {
cy.verify("hull_distance")
    }); 


Then('gaseous reaction products checkbox should be available', () => {
cy.verifyCheckBox("Allow for gaseous reaction products")
});

Then('show the fraction of known precursors checkbox should be available', () => {
  cy.verifyCheckBox("Show the fraction of known precursors in reaction")
});

Then('show only reactions with known precursors checkbox should be available', () => {
  cy.verifyCheckBox("Show only reactions with known precursors")
});  

Then('stable Precursors Only checkbox should be available', () => {
  cy.verifyCheckBox("Stable Precursors Only")
});                                     

Then('ICSD-based Precursors Only checkbox should be available', () => {
  cy.verifyCheckBox("ICSD-based Precursors Only")
});

Then('Drop down input fields should be available', () => {
  cy.verifyDropDown()
})