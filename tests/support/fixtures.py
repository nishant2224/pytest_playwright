"""Core pytest fixtures supporting UI, API, data isolation, and cleanup."""

import os
import uuid
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from quality_demo.api.client import ApiClient
from quality_demo.apps.admin.facade import AdminApp
from quality_demo.apps.guest.facade import GuestApp
from quality_demo.apps.guest.pages import ContactPage
from quality_demo.credentials import Credentials
from quality_demo.data import build_enquiry
from quality_demo.models import Enquiry
from quality_demo.ownership import OwnershipRecord, OwnershipRegistry
from quality_demo.settings import Settings


@pytest.fixture(scope="session")
def run_id() -> str:
    """Unique run identifier distributed across worker processes."""
    return uuid.uuid4().hex[:8]


@pytest.fixture(scope="session")
def worker_label() -> str:
    """Label identifying the current serial process or xdist worker."""
    return os.getenv("PYTEST_XDIST_WORKER", "main")


@pytest.fixture(scope="session")
def settings(request: pytest.FixtureRequest) -> Settings:
    """Session-scoped runtime settings."""
    target = request.config.getoption("--target", default="demo")
    return Settings.load(target=target)


@pytest.fixture(scope="session")
def credentials() -> Credentials:
    """Session-scoped resolved credentials."""
    return Credentials.resolve()


@pytest.fixture(scope="session")
def ownership_registry(
    settings: Settings,
    run_id: str,
    worker_label: str,
) -> OwnershipRegistry:
    """Registry managing owned test records across execution."""
    return OwnershipRegistry(
        artifact_root=settings.artifact_dir,
        run_id=run_id,
        worker_label=worker_label,
    )


@pytest.fixture(scope="function")
def api_client(settings: Settings) -> Generator[ApiClient, None, None]:
    """Fresh standalone HTTP API client."""
    client = ApiClient(settings)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture(scope="function")
def page_evidence_tracker() -> dict[str, Page]:
    """Map tracking open pages for failure evidence capture."""
    return {}


@pytest.fixture(scope="function")
def guest_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Independent anonymous browser context for guest interactions."""
    context = browser.new_context()
    try:
        yield context
    finally:
        context.close()


@pytest.fixture(scope="function")
def guest_page(
    guest_context: BrowserContext,
    page_evidence_tracker: dict[str, Page],
) -> Generator[Page, None, None]:
    """Fresh page inside guest context."""
    page = guest_context.new_page()
    page_evidence_tracker["guest"] = page
    try:
        yield page
    finally:
        page.close()


@pytest.fixture(scope="function")
def admin_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Independent browser context for administrator interactions."""
    context = browser.new_context()
    try:
        yield context
    finally:
        context.close()


@pytest.fixture(scope="function")
def admin_page(
    admin_context: BrowserContext,
    page_evidence_tracker: dict[str, Page],
) -> Generator[Page, None, None]:
    """Fresh page inside admin context."""
    page = admin_context.new_page()
    page_evidence_tracker["admin"] = page
    try:
        yield page
    finally:
        page.close()


@pytest.fixture(scope="function")
def guest_app(guest_page: Page, settings: Settings) -> GuestApp:
    """Constructor-injected GuestApp facade."""
    contact_page = ContactPage(guest_page, settings.base_url)
    return GuestApp(contact_page)


@pytest.fixture(scope="function")
def admin_app(admin_page: Page, settings: Settings) -> AdminApp:
    """Constructor-injected AdminApp facade."""
    return AdminApp(admin_page, settings.base_url)


@pytest.fixture(scope="function")
def enquiry(run_id: str, worker_label: str) -> Enquiry:
    """Fictional enquiry entity with unique identity."""
    return build_enquiry(scenario_id="T04", run_id=run_id, worker_label=worker_label)


@pytest.fixture(scope="function")
def owned_enquiry(
    request: pytest.FixtureRequest,
    enquiry: Enquiry,
    ownership_registry: OwnershipRegistry,
    api_client: ApiClient,
    credentials: Credentials,
) -> Generator[Enquiry, None, None]:
    """Provides unique enquiry, registers ownership upfront, and handles safe cleanup."""
    record: OwnershipRecord = ownership_registry.register(
        enquiry=enquiry,
        node_id=request.node.nodeid,
        scenario_id="T04",
    )

    try:
        yield enquiry
    finally:
        # Teardown: lookup ID from summary API
        cleanup_error_msg: str | None = None
        try:
            summary_resp = api_client.get_messages()
            if summary_resp.status_code == 200:
                messages = summary_resp.json().get("messages", [])
                matching = [
                    m
                    for m in messages
                    if m.get("subject") == enquiry.subject and m.get("name") == enquiry.name
                ]
                if len(matching) == 1:
                    discovered_id = matching[0].get("id")
                    record.discovered_id = discovered_id
                    # Authenticate and attempt deletion
                    api_client.login(credentials.username, credentials.password)
                    del_resp = api_client.delete_message(discovered_id)
                    record.cleanup_status_code = del_resp.status_code
                    if del_resp.status_code == 200:
                        record.status = "deleted"
                    else:
                        record.status = "failed_cleanup"
                        record.cleanup_error = f"HTTP {del_resp.status_code}: {del_resp.text[:200]}"
                        cleanup_error_msg = (
                            f"Cleanup DELETE returned {del_resp.status_code} "
                            f"for record {discovered_id}"
                        )
                elif len(matching) > 1:
                    record.status = "ambiguous_match"
                    record.cleanup_error = f"Multiple matches ({len(matching)}) found for subject"
                    cleanup_error_msg = record.cleanup_error
                else:
                    record.status = "not_found"
            else:
                record.status = "summary_lookup_failed"
                record.cleanup_status_code = summary_resp.status_code
                cleanup_error_msg = f"Summary lookup returned HTTP {summary_resp.status_code}"
        except Exception as ex:
            record.status = "cleanup_exception"
            record.cleanup_error = str(ex)
            cleanup_error_msg = f"Cleanup exception: {ex}"

        manifest_path = ownership_registry.write_manifest(record)

        if cleanup_error_msg:
            # Raise teardown error to make cleanup failure visible per specification
            raise RuntimeError(f"{cleanup_error_msg}. Manifest written to {manifest_path}")
