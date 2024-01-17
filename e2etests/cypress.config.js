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
    errmsg1: 'Error Message:[{"loc":["body","temperature"],"msg":"none is not an allowed value","type":"type_error.none.not_allowed"}]',
    errmsg2: 'Error Message:[{"loc":["body","max_component_precursors"],"msg":"none is not an allowed value","type":"type_error.none.not_allowed"}]',
    errmsg3: 'Error Message:[{"loc":["body","flexible_competition"],"msg":"none is not an allowed value","type":"type_error.none.not_allowed"}]',
    errmsg4: 'Formula field is required',
    mpid: 'mp-9029',
    ModifyObstructiveThirdPartyCode: true,
    SkipDomainInjection: [ '*.matr.io'],

    setupNodeEvents(on, config) {

      return require('./cypress/plugins/index.js')(on, config)

    },

    testIsolation: true,
    supportFile: 'cypress/support/commands.js',
    specPattern: 'cypress/e2e/**/*.feature',
    experimentalWebKitSupport: true,
    
  },

})

