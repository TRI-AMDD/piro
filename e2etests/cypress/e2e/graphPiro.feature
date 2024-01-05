Feature: Validation of Graph in PIRO

  Scenario: Validation of Graph in PIRO web on selecting input params

    Given I login the piro website

    When I enter value of Target Compound mp-id

    And I click on run button

    Then the graph should be loaded
    