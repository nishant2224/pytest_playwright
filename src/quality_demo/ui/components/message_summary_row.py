"""Message summary row component in the administrator inbox."""

from playwright.sync_api import Locator


class MessageSummaryRow:
    """Component representing a single enquiry summary row in /admin/message."""

    def __init__(self, root: Locator) -> None:
        self.root = root

    @property
    def name_locator(self) -> Locator:
        """Locator for the sender/guest name cell."""
        return self.root.locator("div[data-testid^='message'] p").first

    @property
    def subject_locator(self) -> Locator:
        """Locator for the subject description cell."""
        return self.root.locator("div[data-testid^='messageDescription'] p").first

    def get_name(self) -> str:
        """Get the guest name displayed in the row."""
        return self.name_locator.inner_text().strip()

    def get_subject(self) -> str:
        """Get the enquiry subject displayed in the row."""
        return self.subject_locator.inner_text().strip()
