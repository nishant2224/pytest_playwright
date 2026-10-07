import pytest

@pytest.mark.api
@pytest.mark.smoke
def test_get_single_post(api_client):
    """Verify endpoint retrieves an existing post by ID."""
    response = api_client.get("/posts/1")
    
    # 1. Transport status
    assert response.status_code == 200
    
    # 2. Content negotiation
    assert "application/json" in response.headers.get("content-type", "")
    
    # 3. Payload integrity
    data = response.json()
    assert data["id"] == 1
    assert isinstance(data["title"], str)
    assert len(data["title"]) > 0

@pytest.mark.api
@pytest.mark.smoke
def test_get_nonexistent_post(api_client):
    """Verify endpoint handles resource misses with 404."""
    response = api_client.get("/posts/999999")
    
    assert response.status_code == 404