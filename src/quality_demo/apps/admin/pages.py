"""Administrator interface page objects."""

from playwright.sync_api import Locator, Page

from quality_demo.ui.base_page import BasePage
from quality_demo.ui.components.message_summary_row import MessageSummaryRow


class AdminLoginPage(BasePage):
    """Page object for /admin sign-in screen."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    @property
    def username_input(self) -> Locator:
        return self.page.locator("#username")

    @property
    def password_input(self) -> Locator:
        return self.page.locator("#password")

    @property
    def login_button(self) -> Locator:
        return self.page.locator("#doLogin")

    @property
    def error_alert(self) -> Locator:
        """Scoped invalid credentials alert on login form."""
        return self.page.locator(".alert.alert-danger")

    def open(self) -> None:
        """Open administrator login page."""
        self.navigate_to("/admin")
        self.login_button.wait_for(state="visible")


class AdminRoomsPage(BasePage):
    """Page object for /admin/rooms landing screen."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    @property
    def logout_button(self) -> Locator:
        return self.page.get_by_role("button", name="Logout")

    @property
    def rooms_container(self) -> Locator:
        return self.page.locator(".container:has-text('Rooms')")


class AdminInboxPage(BasePage):
    """Page object for /admin/message inbox screen."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    @property
    def messages_container(self) -> Locator:
        return self.page.locator(".messages")

    @property
    def summary_rows(self) -> Locator:
        return self.page.locator(".messages .row.detail")

    def rows_for_subject(self, subject: str) -> Locator:
        """Locator for rows containing the exact subject string."""
        return self.page.locator(".messages .row.detail").filter(has_text=subject)

    def find_row_component(self, subject: str) -> MessageSummaryRow:
        """Return MessageSummaryRow component for given subject."""
        row_locator = self.rows_for_subject(subject)
        return MessageSummaryRow(row_locator)

    def open(self) -> None:
        """Navigate to inbox and wait for container."""
        self.navigate_to("/admin/message")
        self.messages_container.wait_for(state="visible")
