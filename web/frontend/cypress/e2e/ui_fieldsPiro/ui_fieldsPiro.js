import { Given, When, Then, And } from 'cypress-cucumber-preprocessor/steps';
import "cypress-xpath";

Given('I login the piro website', () => {

cy.visit(Cypress.config().baseUrl)
cy.log('NAVIGATING TO PIRO WEB')
cy.wait(10000)
cy.clearAllCookies()
cy.login()

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
  cy.verifyCheckBox("Stable precursors only")
});                                    

Then('ICSD-based Precursors Only checkbox should be available', () => {
  cy.verifyCheckBox(" ICSD-based precursors only")
});

Then('Additional elements to consider field should be available', () => {
  cy.verifyById("react-select-2-input")
  cy.validateAdditionalElementsField()
})

Then('Explicity include as a preCursor field should be available', () => {
  cy.verifyById("react-select-3-input")
})

Then('Drop down input fields should be available', () => {
  cy.verifyDropDown()
})