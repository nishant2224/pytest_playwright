"""AdminApp facade composing admin actions and assertions."""

from playwright.sync_api import Page

from quality_demo.apps.admin.actions import AdminActions
from quality_demo.apps.admin.assertions import AdminAssertions
from quality_demo.apps.admin.pages import AdminInboxPage, AdminLoginPage, AdminRoomsPage


class AdminApp:
    """Automation facade for the administrator interface."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.login_page = AdminLoginPage(page, base_url)
        self.rooms_page = AdminRoomsPage(page, base_url)
        self.inbox_page = AdminInboxPage(page, base_url)
        self.actions = AdminActions(self.login_page, self.rooms_page, self.inbox_page)
        self.assertions = AdminAssertions(self.login_page, self.rooms_page, self.inbox_page)
