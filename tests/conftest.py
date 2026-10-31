"""Root pytest configuration and hook registrations."""

import pytest

from quality_demo.settings import Settings
from tests.support.fixtures import (
    admin_app,
    admin_context,
    admin_page,
    api_client,
    credentials,
    enquiry,
    guest_app,
    guest_context,
    guest_page,
    owned_enquiry,
    ownership_registry,
    page_evidence_tracker,
    run_id,
    settings,
    worker_label,
)
from tests.support.reporting import capture_page_evidence

pytest_plugins = []

__all__ = [
    "admin_app",
    "admin_context",
    "admin_page",
    "api_client",
    "credentials",
    "enquiry",
    "guest_app",
    "guest_context",
    "guest_page",
    "owned_enquiry",
    "ownership_registry",
    "page_evidence_tracker",
    "run_id",
    "settings",
    "worker_label",
]


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register custom CLI options for target selection."""
    parser.addoption(
        "--target",
        action="store",
        default="demo",
        help="Target configuration name matching config/<target>.toml",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """Capture page screenshots and attach to evidence when UI tests fail."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check if page_evidence_tracker fixture exists in item
        tracker = item.funcargs.get("page_evidence_tracker")
        settings_obj: Settings = item.funcargs.get("settings")
        if tracker and settings_obj:
            for label, page in tracker.items():
                capture_page_evidence(
                    page=page,
                    label=label,
                    artifact_root=settings_obj.artifact_dir,
                    node_id=item.nodeid,
                )
