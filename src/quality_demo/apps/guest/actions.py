"""Guest user actions coordinating interactions on the public interface."""

from quality_demo.apps.guest.pages import ContactPage
from quality_demo.models import Enquiry


class GuestActions:
    """Action coordinator for guest interactions."""

    def __init__(self, page: ContactPage) -> None:
        self.page = page

    def open_contact_form(self) -> None:
        """Navigate to the public contact form."""
        self.page.open()

    def submit_enquiry(self, enquiry: Enquiry) -> None:
        """Fill and submit all contact form fields with enquiry data."""
        self.page.name_input.fill(enquiry.name)
        self.page.email_input.fill(enquiry.email)
        self.page.phone_input.fill(enquiry.phone)
        self.page.subject_input.fill(enquiry.subject)
        self.page.description_input.fill(enquiry.description)
        self.page.submit_button.click()

    def submit_empty_form(self) -> None:
        """Submit the contact form without entering any data."""
        self.page.submit_button.click()
