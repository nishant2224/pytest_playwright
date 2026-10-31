"""BDD step definitions for guest enquiry workflows."""

from pytest_bdd import given, then, when

from quality_demo.apps.guest.facade import GuestApp
from quality_demo.models import Enquiry


@given("I am on the public contact form")
def on_contact_form(guest_app: GuestApp) -> None:
    guest_app.actions.open_contact_form()


@when("I submit the form without entering any information")
def submit_empty_contact_form(guest_app: GuestApp) -> None:
    guest_app.actions.submit_empty_form()


@then("I see required-field feedback")
def assert_required_field_feedback(guest_app: GuestApp) -> None:
    guest_app.assertions.required_field_feedback_visible()


@then("the enquiry has not been acknowledged")
def assert_enquiry_not_acknowledged(guest_app: GuestApp) -> None:
    guest_app.assertions.acknowledgement_not_visible()


@given("I have a unique fictional enquiry", target_fixture="current_enquiry")
def provide_unique_enquiry(owned_enquiry: Enquiry) -> Enquiry:
    return owned_enquiry


@when("I submit my enquiry")
def submit_my_enquiry(guest_app: GuestApp, current_enquiry: Enquiry) -> None:
    guest_app.actions.submit_enquiry(current_enquiry)


@then("I see an acknowledgement for my enquiry")
def assert_enquiry_acknowledgement(guest_app: GuestApp, current_enquiry: Enquiry) -> None:
    guest_app.assertions.acknowledgement_visible(current_enquiry)
