"""Guest assertions validating outcomes using retrying Playwright expectations."""

from playwright.sync_api import expect

from quality_demo.apps.guest.pages import ContactPage
from quality_demo.models import Enquiry


class GuestAssertions:
    """Assertions for guest contact form workflows."""

    def __init__(self, page: ContactPage) -> None:
        self.page = page

    def acknowledgement_visible(self, enquiry: Enquiry, timeout: int = 10000) -> None:
        """Assert that personalized enquiry acknowledgement appears for guest."""
        ack = self.page.acknowledgement_locator(enquiry.name)
        expect(ack).to_be_visible(timeout=timeout)

    def acknowledgement_not_visible(self) -> None:
        """Assert that no submission acknowledgement is displayed."""
        generic_ack = self.page.page.locator("text=Thanks for getting in touch")
        expect(generic_ack).not_to_be_visible()

    def required_field_feedback_visible(self, timeout: int = 10000) -> None:
        """Assert that validation feedback appears for required fields."""
        expect(self.page.feedback_alert).to_be_visible(timeout=timeout)
        feedback_texts = self.page.feedback_items.all_text_contents()
        combined = " ".join(feedback_texts).lower()
        assert any(term in combined for term in ["blank", "between", "empty"]), (
            f"Expected required-field feedback, got: {feedback_texts}"
        )

    def form_visible(self) -> None:
        """Assert that the contact form remains displayed on the page."""
        expect(self.page.name_input).to_be_visible()
        expect(self.page.submit_button).to_be_visible()
