import { Given, When, Then, And } from 'cypress-cucumber-preprocessor/steps';
import "cypress-xpath";
const genFilesPath = "cypress/fixtures/rpv.text"
const leFilesPath = "cypress/fixtures/le.text"
const newRpvPath = "cypress/fixtures/newRpv.text"
const newleFilesPath = "cypress/fixtures/newLe.text"
//cy.writeFile(genFilesPath,'test') tested


const sometext='';

Given('I login the piro website', () => {

cy.visit(Cypress.config().baseUrl)
cy.log('NAVIGATING TO PIRO WEB')
cy.wait(10000)
cy.login()
  
});


When('I enter value of Target Compound mp-id', () => {
cy.get('[name="target_entry_id"]').type(Cypress.config().mpid)

});


And('I click on run button', () => {
cy.get('[type="submit"]').click()
});


Then('the graph should be loaded', () => {
cy.wait(10000);
cy.scrollTo('bottom')
cy.get('.js-plotly-plot').scrollIntoView()
cy.screenshot
});
