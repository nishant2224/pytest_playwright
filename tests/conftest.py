"""Shared pytest fixtures and hooks belong here."""
import httpx
import pytest

@pytest.fixture(scope="function")
def api_client():
    """Provides a fresh HTTP client session for each test function."""
    client = httpx.Client(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=5.0,
        headers={"Accept": "application/json"}
    )
    yield client
    client.close()