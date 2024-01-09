const { defineConfig } = require('cypress')

module.exports = defineConfig({

  chromeWebSecurity: false,

  'cypress-cucumber-preprocessor': {

    nonGlobalStepDefinitions: true,

    step_definitions: './cypress/e2e/**/*.feature',

  },
  e2e: {

    baseUrl: 'https://piro.matr.io/',
    username: '',
    password: '',
    mpid: 'mp-9029',
    ModifyObstructiveThirdPartyCode: true,
    SkipDomainInjection: [ '*.matr.io'],

    setupNodeEvents(on, config) {

      return require('./cypress/plugins/index.js')(on, config)

    },

    testIsolation: false,
    supportFile: 'cypress/support/commands.js',
    specPattern: 'cypress/e2e/**/*.feature',
    experimentalWebKitSupport: true,
    
  },

})

