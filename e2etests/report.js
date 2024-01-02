
const report = require("multiple-cucumber-html-reporter");
const fs = require("fs");

report.generate( {
    jsonDir: "./cypress/json-logs/",
    reportPath : "./cucumber-report/",
    metadata: {
        browser: {
            name :"chrome",
            version: 60,
        },
        device: "local test machine",
        platform :{
            name: "windows",
        },
    },
    reportName: "Oxidation State Analyser Test Report",
    customData: {
        title: "Run Info",
        data: [
            { label: "Project", value: "OSA Cypress Cucumber"  },
            { label: "Environment", value: "Local"},
        ]
    },
})