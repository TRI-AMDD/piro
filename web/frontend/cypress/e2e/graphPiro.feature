Feature: Validation of Graph in PIRO

  Scenario Outline: Graph Generation And Validation : Validation of Graph in PIRO web on selecting input params

    Given I login the piro website

    When I enter tc as "<tc>"  temperature as "<temp>" number of components as "<numComp>" and depth as "<depth>"

    Then the expected graph should be loaded

    Examples:
        | tc |temp | numComp | depth | 
        |  mp-9029 | 1000 | 0 | 0 |
    