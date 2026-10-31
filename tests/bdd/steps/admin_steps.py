"""BDD step definitions for administrator workflows."""

from pytest_bdd import given, then, when

from quality_demo.apps.admin.facade import AdminApp
from quality_demo.credentials import Credentials
from quality_demo.models import Enquiry


@given("I am on the administrator login page with a fresh session")
def on_admin_login_page(admin_app: AdminApp) -> None:
    admin_app.actions.open_login()


@when("I sign in using the configured demo administrator credentials")
def sign_in_valid_credentials(admin_app: AdminApp, credentials: Credentials) -> None:
    admin_app.actions.login(credentials.username, credentials.password)


@then("I can see the administrator room-list screen")
def assert_rooms_screen_visible(admin_app: AdminApp) -> None:
    admin_app.assertions.rooms_screen_visible()


@when("I sign in using an incorrect password")
def sign_in_incorrect_password(admin_app: AdminApp, credentials: Credentials) -> None:
    admin_app.actions.login(credentials.username, "fictional-incorrect-password-999")


@then("I see a login rejection message")
def assert_login_rejection_message(admin_app: AdminApp) -> None:
    admin_app.assertions.login_rejection_visible()


@then("I remain on the login screen")
def assert_remains_on_login_screen(admin_app: AdminApp) -> None:
    admin_app.assertions.remains_on_login_screen()


@when("I sign in to the administrator interface with a separate session")
def sign_in_separate_session(admin_app: AdminApp, credentials: Credentials) -> None:
    admin_app.actions.open_login()
    admin_app.actions.login(credentials.username, credentials.password)
    admin_app.assertions.rooms_screen_visible()


@when("I open the administrator inbox")
def open_admin_inbox(admin_app: AdminApp) -> None:
    admin_app.actions.open_inbox()


@then("exactly one inbox row matches my enquiry subject and name")
def assert_inbox_row_matches(admin_app: AdminApp, current_enquiry: Enquiry) -> None:
    admin_app.assertions.inbox_row_matches(current_enquiry)
