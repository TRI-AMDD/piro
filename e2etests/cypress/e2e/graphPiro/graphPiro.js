import { Given, When, Then, And } from 'cypress-cucumber-preprocessor/steps';
import "cypress-xpath";
const genFilesPath = "cypress/fixtures/rpv.text"
const leFilesPath = "cypress/fixtures/le.text"
const newRpvPath = "cypress/fixtures/newRpv.text"
const newleFilesPath = "cypress/fixtures/newLe.text"
//cy.writeFile(genFilesPath,'test') tested


const sometext='';

Given('I open the piro website', () => {

  //cy.visit('https://oxi.matr.io/');
  //cy.visit('https://www.google.co.in/');
  //cy.visit(baseUrl)
  cy.visit(Cypress.config().baseUrl),{
    Headers:{
        "Accept":"application/json, text/plain, */*",
        "User-Agent": "axios/0.18.0"
    }
  }
  cy.screenshot() // Replace with your website URL
  cy.log('NAVIGATING TO PIRO WEB')
  cy.wait(10000)
    
});


