
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
