"""Base page object maintaining reference to page and navigation helper."""

from playwright.sync_api import Page, Response


class BasePage:
    """Base page object providing page reference and base URL navigation."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/")

    def navigate_to(self, path: str = "") -> Response | None:
        """Navigate to relative path from base URL."""
        target_path = path if path.startswith("/") else f"/{path}"
        target_url = f"{self.base_url}{target_path}"
        return self.page.goto(target_url, wait_until="domcontentloaded")
