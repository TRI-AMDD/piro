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


Cypress.Commands.add('fillValue',(propname,propvalue) => {
    if (propvalue=='') {
        cy.log("LOGGING EMPTY",propname)
        cy.get('[name='+propname+']').clear() 
        cy.get('[name='+propname+']').type('{backspace}')
    }
    else{
        cy.get('[name='+propname+']').clear() 
        cy.get('[name='+propname+']').type(propvalue)
    }
})

Cypress.Commands.add('generateGraph',(tc,temperature,comp,depth) => {
    cy.log("LOGGING")
    cy.wait(5000)
    cy.fillValue("target_entry_id",tc)
    cy.fillValue("temperature",temperature)
    cy.fillValue("max_component_precursors",comp)
    cy.fillValue("flexible_competition",depth)
    cy.get('[type="submit"]').click()
})




Cypress.Commands.add('validateErr', (tc,temperature,comp,depth) => {
    if(temperature=='')
    {
        cy.get('.Home_Error__OCU2n')
         .invoke('text')
         .should('eq',Cypress.config().errmsg1)
    }
    else if(comp=='')
    {
        cy.get('.Home_Error__OCU2n')
         .invoke('text')
         .should('eq',Cypress.config().errmsg2)
    }
    else if(depth=='')
    {
        cy.get('.Home_Error__OCU2n')
         .invoke('text')
         .should('eq',Cypress.config().errmsg3)
    }
    else if(tc==''){
        cy.get([name="target_entry_id"])
         .invoke('text')
         .should('eq',Cypress.config().errmsg4)   
    }
})