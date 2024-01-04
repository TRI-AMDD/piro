const { defineConfig } = require('cypress')

module.exports = defineConfig({

  projectId:'ag5qdq',

  chromeWebSecurity: false,

  'cypress-cucumber-preprocessor': {

    nonGlobalStepDefinitions: true,

    step_definitions: './cypress/e2e/**/*.feature',

  },
  /*clientCertificates: [
    {
      url: 'https://oxi.matr.io/',
      certs: [
        {
          cert: 'cypress/certs/cert.pem',
          //key: 'cypress/certs/private.key',
        },
      ]
    }], */

  e2e: {

    baseUrl: 'https://piro.matr.io/',
    username: 'tri.jaramillo.group@tri.global',
    password: 'PiroTest1234!',
    mpid: 'mp-9029',
    ModifyObstructiveThirdPartyCode: true,
    SkipDomainInjection: [ '*.matr.io'],

    setupNodeEvents(on, config) {

      return require('./cypress/plugins/index.js')(on, config)

    },

    //retries: 1,

    testIsolation: false,

    specPattern: 'cypress/e2e/**/*.feature',
    experimentalWebKitSupport: true,
    supportFile:false

  },

})

