"""HTTP API client for Restful Booker Platform."""

from types import TracebackType

import httpx

from quality_demo.settings import Settings


class ApiClient:
    """Synchronous HTTP client for interacting with Restful Booker Platform APIs.

    Handles explicit cookie authentication required by the hosted backend.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = httpx.Client(
            base_url=settings.base_url,
            timeout=settings.http_timeout_seconds,
            headers={"Accept": "application/json"},
            follow_redirects=True,
        )

    def close(self) -> None:
        """Close the underlying HTTP client session."""
        self._client.close()

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def login(self, username: str = "admin", password: str = "password") -> httpx.Response:
        """Authenticate with administrator credentials and store the token cookie.

        The hosted API returns `{"token": "..."}` without setting the cookie in headers,
        so we explicitly set the `token` cookie on the client for subsequent calls.
        """
        payload = {"username": username, "password": password}
        response = self._client.post("/api/auth/login", json=payload)
        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            if token:
                # Explicitly set host-scoped token cookie
                self._client.cookies.set("token", token, domain=self._client.base_url.host)
        return response

    def validate_token(self, token: str | None = None) -> httpx.Response:
        """Validate token with POST /api/auth/validate."""
        if token is None:
            token = self._client.cookies.get("token", "")
        return self._client.post("/api/auth/validate", json={"token": token})

    def get_rooms(self) -> httpx.Response:
        """Anonymous GET /api/room contract check."""
        return self._client.get("/api/room")

    def get_messages(self) -> httpx.Response:
        """GET /api/message summary list."""
        return self._client.get("/api/message")

    def get_message_detail(self, message_id: int) -> httpx.Response:
        """GET /api/message/{id} detailed view."""
        return self._client.get(f"/api/message/{message_id}")

    def create_message(self, payload: dict) -> httpx.Response:
        """POST /api/message submission."""
        return self._client.post("/api/message", json=payload)

    def delete_message(self, message_id: int) -> httpx.Response:
        """DELETE /api/message/{id} for owned record."""
        return self._client.delete(f"/api/message/{message_id}")
