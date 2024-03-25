// cypress/support/commands.js
const compareSnapshotCommand = require('cypress-image-diff-js/dist/command')
compareSnapshotCommand()
Cypress.Commands.add('login', () => {
    if((Cypress.config().baseUrl).includes('localhost'))
    {
      cy.intercept('POST', '/api', { fixture: 'piro_response.json' })
      cy.intercept('POST', '/api/recommend_routes_task', { fixture: 'piro_response_graph.json' })
      cy.intercept('GET', '/api/recommend_routes_task/ed867b97-b0e2-4203-b229-95ac922aace8', { fixture: 'piro_response_graph1.json' })
      cy.intercept('GET', '/api/recommend_routes_task/ed867b97-b0e2-4203-b229-95ac922aace8', { fixture: 'piro_response_graph2.json' })
    }  
})



Cypress.Commands.add('verify', (uifield) => {
    
    let theXpath="//input[@name='"+uifield+"']"
    cy.xpath(theXpath).should('be.visible')

    
})

Cypress.Commands.add('verifyById',(id) => {
    let theXpath="//input[@id='"+id+"']"
    cy.xpath(theXpath).should('be.visible')
})

Cypress.Commands.add('verifyCheckBox', (displayText) => {
    cy.get('[data-testid=checkboxes]').children().contains(displayText).should('be.visible')
})

Cypress.Commands.add('verifyDropDown', () => {
    cy.xpath("//button[@placeholder='Additional element']").click();
    cy.get('#material-tailwind-select-0').should('be.visible')
    cy.get('#material-tailwind-select-1').should('be.visible')
    cy.get('#material-tailwind-select-2').should('be.visible')
    
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
    cy.fillValue("target_entry_id",tc)
    cy.fillValue("temperature",temperature)
    cy.fillValue("max_component_precursors",comp)
    cy.fillValue("flexible_competition",depth)
    cy.xpath("//button[@placeholder='Run']").click({force : true})
})

Cypress.Commands.add('validateGraph', () => {
    
    cy.wait(10000);
    cy.scrollTo('bottom')
    cy.get('.js-plotly-plot').scrollIntoView().compareSnapshot('piro-graph')
})


Cypress.Commands.add('validateErr', (tc,temperature,comp,depth) => {
  
     if(temperature.trim() === ''){
        cy.xpath("//input[@name='temperature']").nextAll().invoke('text').should('eq',Cypress.config().errmsg1)
     }else if(comp.trim() === ''){
        cy.xpath("//input[@name='max_component_precursors']").nextAll().invoke('text').should('eq',Cypress.config().errmsg1)
     }else if(depth.trim() === ''){
        cy.xpath("//input[@name='flexible_competition']").nextAll().invoke('text').should('eq',Cypress.config().errmsg1)
     }else if(tc.trim() === ''){
        cy.xpath("//input[@name='target_entry_id']").nextAll().invoke('text').should('eq',Cypress.config().errmsg1)
     }
})

Cypress.Commands.add('validateAdditionalElementsField', () => {
    // cy.get("[id='react-select-2-input']").type("na")
    // cy.xpath("//div[@id='react-select-2-listbox']/div").click()
    // cy.xpath("//div[@class=' css-1y7rh0y-MultiValueGeneric2']").invoke('text').should('eq','Na')
    cy.enterValidElements("na","Na")
    cy.enterValidElements("PB","Pb")
    cy.enterValidElements("Mn","Mn")
    cy.get("[id='react-select-2-input']").type("Mn")
    cy.xpath("//div[@class=' css-nhbbvo-NoOptionsMessage2']").invoke('text').should('eq','No options')
    cy.get("[id='react-select-2-input']").clear().type("SS")
    cy.xpath("//p[@style='color: red;']").invoke('text').should('eq','Not an element')
    
    // cy.get("[id='react-select-2-input']").clear().type("PB")
    // cy.xpath("//div[@id='react-select-2-listbox']/div").click()
    // cy.xpath("//div[@class=' css-1y7rh0y-MultiValueGeneric2']").invoke('text').should('eq','Pb')

 

})

Cypress.Commands.add('enterValidElements', (elementName,message) => {
    cy.get("[id='react-select-2-input']").clear().type(elementName)
    cy.xpath("//div[@id='react-select-2-listbox']/div").click()
    cy.xpath("//div[@class=' css-1y7rh0y-MultiValueGeneric2']").invoke('text').should('eq',message)
})