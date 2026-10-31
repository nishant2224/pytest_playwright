"""Administrator login BDD scenario bindings."""

import pytest
from pytest_bdd import scenario


@pytest.mark.bdd
@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.smoke
@scenario("../features/admin_login.feature", "Administrator signs in successfully")
def test_admin_login_success() -> None:
    """T01: Administrator signs in with valid credentials."""


@pytest.mark.bdd
@pytest.mark.ui
@pytest.mark.auth
@pytest.mark.negative
@scenario("../features/admin_login.feature", "Administrator login rejects an incorrect password")
def test_admin_login_rejected() -> None:
    """T02: Administrator login rejects invalid password."""
