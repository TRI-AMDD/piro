Feature: Validation of Graph in PIRO

  Scenario: Validation of Graph in PIRO web on selecting input params

    Given I login the piro website

    Then target compound field should be available

    Then temperature field should be available

    Then max_component_precursors field should be available

    Then flexible_competition field should be available

    Then hull_distance field should be available

    Then gaseous reaction products checkbox should be available

    Then show the fraction of known precursors checkbox should be available

    Then show only reactions with known precursors checkbox should be available

    Then stable Precursors Only checkbox should be available

    Then ICSD-based Precursors Only checkbox should be available

    Then Additional elements to consider field should be available

    Then Explicity include as a preCursor field should be available

    Then Drop down input fields should be available
    





    