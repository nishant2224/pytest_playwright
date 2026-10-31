"""GuestApp facade composing guest actions and assertions."""

from quality_demo.apps.guest.actions import GuestActions
from quality_demo.apps.guest.assertions import GuestAssertions
from quality_demo.apps.guest.pages import ContactPage


class GuestApp:
    """Automation facade for the guest-facing public interface."""

    def __init__(self, page: ContactPage) -> None:
        self.page = page
        self.actions = GuestActions(page)
        self.assertions = GuestAssertions(page)
