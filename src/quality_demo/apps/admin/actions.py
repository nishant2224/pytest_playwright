"""Administrator actions coordinating login and inbox navigation."""

from quality_demo.apps.admin.pages import AdminInboxPage, AdminLoginPage, AdminRoomsPage


class AdminActions:
    """Action coordinator for administrator interface."""

    def __init__(
        self,
        login_page: AdminLoginPage,
        rooms_page: AdminRoomsPage,
        inbox_page: AdminInboxPage,
    ) -> None:
        self.login_page = login_page
        self.rooms_page = rooms_page
        self.inbox_page = inbox_page

    def open_login(self) -> None:
        """Navigate to administrator login screen."""
        self.login_page.open()

    def login(self, username: str, password: str) -> None:
        """Submit credentials on login screen."""
        self.login_page.username_input.fill(username)
        self.login_page.password_input.fill(password)
        self.login_page.login_button.click()

    def open_inbox(self) -> None:
        """Navigate to administrator inbox."""
        self.inbox_page.open()
