"""Administrator assertions validating outcomes using retrying Playwright expectations."""

from playwright.sync_api import expect

from quality_demo.apps.admin.pages import AdminInboxPage, AdminLoginPage, AdminRoomsPage
from quality_demo.models import Enquiry


class AdminAssertions:
    """Assertions for administrator workflows."""

    def __init__(
        self,
        login_page: AdminLoginPage,
        rooms_page: AdminRoomsPage,
        inbox_page: AdminInboxPage,
    ) -> None:
        self.login_page = login_page
        self.rooms_page = rooms_page
        self.inbox_page = inbox_page

    def rooms_screen_visible(self, timeout: int = 15000) -> None:
        """Assert that user reached /admin/rooms screen with authenticated navigation."""
        expect(self.rooms_page.page).to_have_url(
            f"{self.rooms_page.base_url}/admin/rooms",
            timeout=timeout,
        )
        expect(self.rooms_page.logout_button).to_be_visible(timeout=timeout)

    def login_rejection_visible(self, timeout: int = 10000) -> None:
        """Assert that invalid credentials rejection alert is displayed."""
        expect(self.login_page.error_alert).to_be_visible(timeout=timeout)
        expect(self.login_page.error_alert).to_contain_text("Invalid credentials")

    def remains_on_login_screen(self) -> None:
        """Assert that browser remains on the unauthenticated login screen."""
        expect(self.login_page.login_button).to_be_visible()
        expect(self.login_page.username_input).to_be_visible()
        assert "/admin/rooms" not in self.login_page.page.url

    def inbox_row_matches(self, enquiry: Enquiry, timeout: int = 15000) -> None:
        """Assert that exactly one inbox row matches enquiry subject and name."""
        matching_rows = self.inbox_page.rows_for_subject(enquiry.subject)
        # Use retrying assertion to wait for row appearance
        expect(matching_rows.first).to_be_visible(timeout=timeout)

        count = matching_rows.count()
        assert count == 1, (
            f"Expected exactly 1 inbox row for subject '{enquiry.subject}', found {count}"
        )

        row_comp = self.inbox_page.find_row_component(enquiry.subject)
        expect(row_comp.name_locator).to_have_text(enquiry.name)
        expect(row_comp.subject_locator).to_have_text(enquiry.subject)
