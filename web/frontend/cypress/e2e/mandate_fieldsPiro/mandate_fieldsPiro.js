import { Given, When, Then, And } from 'cypress-cucumber-preprocessor/steps';
import "cypress-xpath";

Given('I login the piro website', () => {

cy.visit(Cypress.config().baseUrl)
cy.log('NAVIGATING TO PIRO WEB')
cy.wait(10000)
cy.clearAllCookies()
cy.login()

});


When('I enter tc as {string}  temperature as {string} number of components as {string} and depth as {string}', (tc,temperature,comp,depth) => {
  cy.wait(3000)
  cy.generateGraph(tc,temperature,comp,depth)

})

Then('I should see Error message for tc as {string}  temperature as {string} number of components as {string} and depth as {string}', (tc,temperature,comp,depth) => {
  cy.wait(10000)
  cy.validateErr(tc,temperature,comp,depth)
})