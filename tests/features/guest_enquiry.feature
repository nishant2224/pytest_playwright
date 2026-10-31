Feature: Guest enquiries

  @bdd @ui @negative
  Scenario: Empty enquiry shows required-field feedback
    Given I am on the public contact form
    When I submit the form without entering any information
    Then I see required-field feedback
    And the enquiry has not been acknowledged

  @bdd @ui @e2e @writes_data
  Scenario: Guest enquiry appears in the administrator inbox
    Given I have a unique fictional enquiry
    And I am on the public contact form
    When I submit my enquiry
    Then I see an acknowledgement for my enquiry
    When I sign in to the administrator interface with a separate session
    And I open the administrator inbox
    Then exactly one inbox row matches my enquiry subject and name
