"""Public guest interface and contact form page objects."""

from playwright.sync_api import Locator, Page

from quality_demo.ui.base_page import BasePage


class ContactPage(BasePage):
    """Page object for the public front page and embedded contact form."""

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page, base_url)

    @property
    def name_input(self) -> Locator:
        return self.page.locator("[data-testid='ContactName']")

    @property
    def email_input(self) -> Locator:
        return self.page.locator("[data-testid='ContactEmail']")

    @property
    def phone_input(self) -> Locator:
        return self.page.locator("[data-testid='ContactPhone']")

    @property
    def subject_input(self) -> Locator:
        return self.page.locator("[data-testid='ContactSubject']")

    @property
    def description_input(self) -> Locator:
        return self.page.locator("[data-testid='ContactDescription']")

    @property
    def submit_button(self) -> Locator:
        return self.page.get_by_role("button", name="Submit")

    @property
    def form(self) -> Locator:
        return self.page.locator("form").filter(has=self.name_input)

    @property
    def feedback_alert(self) -> Locator:
        return self.page.locator(".alert-danger, .alert")

    @property
    def feedback_items(self) -> Locator:
        return self.page.locator(".alert-danger p, .alert p")

    def acknowledgement_locator(self, name: str) -> Locator:
        """Locator for the personalized submission confirmation message."""
        return self.page.locator(f"text=Thanks for getting in touch {name}!")

    def open(self) -> None:
        """Open the public contact page and wait for form elements."""
        self.navigate_to("/")
        self.name_input.wait_for(state="visible")
