import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

require('@cypress/xpath')

Cypress.on('certificate:error', (error, runnable) => {
   return true;
  });