"""T05: Public room-list contract verification."""

import pytest

from quality_demo.api.client import ApiClient


@pytest.mark.api
@pytest.mark.smoke
def test_public_room_list_contract(api_client: ApiClient) -> None:
    """T05: Anonymous GET /api/room returns valid schema, unique IDs, and sensible field types."""
    response = api_client.get_rooms()

    assert response.status_code == 200, (
        f"Expected 200 OK, got {response.status_code}: {response.text}"
    )
    assert "application/json" in response.headers.get("content-type", "")

    payload = response.json()
    assert isinstance(payload, dict), f"Expected JSON object payload, got {type(payload)}"
    assert "rooms" in payload, f"Expected 'rooms' key in payload: {payload.keys()}"

    rooms = payload["rooms"]
    assert isinstance(rooms, list), f"Expected 'rooms' to be a list, got {type(rooms)}"
    assert len(rooms) > 0, "Expected at least one room in the rooms list"

    seen_ids: set[int] = set()
    for room in rooms:
        assert isinstance(room, dict), f"Expected room to be dict, got {type(room)}"

        room_id = room.get("roomid")
        assert isinstance(room_id, int), f"Expected integer roomid, got {room_id}"
        assert room_id > 0, f"Expected positive roomid, got {room_id}"
        assert room_id not in seen_ids, f"Found duplicate roomid: {room_id}"
        seen_ids.add(room_id)

        assert isinstance(room.get("roomName"), str), "Expected string roomName"
        assert isinstance(room.get("type"), str), "Expected string type"
        assert isinstance(room.get("roomPrice"), (int, float)), "Expected numeric roomPrice"
        assert room["roomPrice"] >= 0, f"Expected non-negative price, got {room['roomPrice']}"
        assert isinstance(room.get("accessible"), bool), "Expected boolean accessible"
        assert isinstance(room.get("features"), list), "Expected list features"
