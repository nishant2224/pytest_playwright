"""T06: Missing enquiry subject API rejection verification."""

import pytest

from quality_demo.api.client import ApiClient


@pytest.mark.api
@pytest.mark.negative
def test_missing_enquiry_subject_rejected(api_client: ApiClient) -> None:
    """T06: Anonymous POST /api/message without subject returns 400 with validation errors."""
    payload = {
        "name": "Validation Tester",
        "email": "validation.tester@example.com",
        "phone": "012345678901",
        "description": "Fictional message body exceeding the minimum required twenty characters.",
    }

    response = api_client.create_message(payload)

    assert response.status_code == 400, (
        f"Expected HTTP 400 Bad Request, got {response.status_code}: {response.text}"
    )

    data = response.json()
    assert isinstance(data, list), f"Expected list of validation messages, got {type(data)}"
    assert len(data) > 0, "Expected non-empty list of validation messages"

    combined_errors = " ".join(str(msg) for msg in data).lower()
    assert "subject" in combined_errors, f"Expected subject-specific validation feedback in: {data}"
