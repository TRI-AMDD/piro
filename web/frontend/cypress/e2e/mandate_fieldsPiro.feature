Feature: Validation of Graph in PIRO

  Scenario Outline: Error message : Validation of Graph in PIRO web on selecting input params

    Given I login the piro website

    When I enter tc as "<tc>"  temperature as "<temp>" number of components as "<numComp>" and depth as "<depth>"

    Then I should see Error message for tc as "<tc>"  temperature as "<temp>" number of components as "<numComp>" and depth as "<depth>"
    
    Examples:
        | tc |temp | numComp | depth | 
        |  mp-9029 |  | 5 | 10 |
        | mp-9029 | 750|  | 10 |
        | mp-9029 | 750| 5 |  |
        |  | 750 | 5 | 10 |