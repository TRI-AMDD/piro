Cypress.Commands.add('login', () => {
    cy.get(".login_login__19CNz").should('be.visible').click()
    cy.get("#signInFormUsername").type(Cypress.config().username,{force: true})
    cy.get("#signInFormPassword").type(Cypress.config().password,{force : true})
    cy.get('[name="signInSubmitButton"]').eq(1).click()
})



Cypress.Commands.add('verify', (uifield) => {
    
    let theXpath="//input[@name='"+uifield+"']"
    cy.xpath(theXpath).should('be.visible')

    
})

Cypress.Commands.add('verifyCheckBox', (displayText) => {
    
    cy.get('.css-my3lu9').children().contains(displayText).should('be.visible')
    
})

Cypress.Commands.add('verifyDropDown', () => {
    
    cy.get('#react-select-2-input').should('be.visible')
    cy.get('#react-select-3-input').should('be.visible')
    cy.get('#react-select-4-input').should('be.visible')
    
})
