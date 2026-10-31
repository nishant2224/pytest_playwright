"""Guest enquiry BDD scenario bindings."""

import pytest
from pytest_bdd import scenario


@pytest.mark.bdd
@pytest.mark.ui
@pytest.mark.negative
@scenario("../features/guest_enquiry.feature", "Empty enquiry shows required-field feedback")
def test_guest_empty_enquiry_feedback() -> None:
    """T03: Empty enquiry submission displays required-field validation feedback."""


@pytest.mark.bdd
@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.writes_data
@scenario("../features/guest_enquiry.feature", "Guest enquiry appears in the administrator inbox")
def test_guest_enquiry_reaches_admin_inbox() -> None:
    """T04: Guest enquiry appears in the administrator inbox."""
