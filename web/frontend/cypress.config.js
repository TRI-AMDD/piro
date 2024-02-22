const { defineConfig } = require('cypress')
const cucumber = require('cypress-cucumber-preprocessor').default;
const getCompareSnapshotsPlugin = require('cypress-image-diff-js/plugin');
module.exports = defineConfig({

  chromeWebSecurity: false,

  'cypress-cucumber-preprocessor': {

    nonGlobalStepDefinitions: true,

    step_definitions: './cypress/e2e/**/*.feature',

  },
  e2e: {

    baseUrl: 'http://localhost:3000',
    username: '',
    password: '',
    errmsg1: 'This field is required',
    errmsg2: 'Formula field is required',
    mpid: 'mp-9029',
    ModifyObstructiveThirdPartyCode: true,
    SkipDomainInjection: [ '*.matr.io'],

    setupNodeEvents(on, config) {

      //return require('./cypress/plugins/index.js')(on, config)
      on('file:preprocessor', cucumber());
      return getCompareSnapshotsPlugin(on, config);
    },

    testIsolation: true,
    supportFile: 'cypress/support/commands.js',
    specPattern: 'cypress/e2e/**/*.feature',
    experimentalWebKitSupport: true,
    defaultCommandTimeout: 10000
  },

})

