Feature: Administrator sign-in

  @bdd @ui @auth @smoke
  Scenario: Administrator signs in successfully
    Given I am on the administrator login page with a fresh session
    When I sign in using the configured demo administrator credentials
    Then I can see the administrator room-list screen

  @bdd @ui @auth @negative
  Scenario: Administrator login rejects an incorrect password
    Given I am on the administrator login page with a fresh session
    When I sign in using an incorrect password
    Then I see a login rejection message
    And I remain on the login screen
