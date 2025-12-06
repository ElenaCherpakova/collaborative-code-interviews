"""Tests for WebSocket endpoints."""
import pytest
from uuid import uuid4


def test_websocket_connection_success(client):
    """Test establishing a WebSocket connection."""
    # Create interview
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "python",
            "creatorName": "User",
        },
    )
    interview_id = create_response.json()["id"]
    participant_id = create_response.json()["participants"][0]["id"]
    
    # Connect via WebSocket
    with client.websocket_connect(
        f"/ws/interviews/{interview_id}?participantId={participant_id}"
    ) as websocket:
        # Connection should be established
        assert websocket is not None


def test_websocket_connection_interview_not_found(client):
    """Test WebSocket connection with non-existent interview."""
    fake_id = str(uuid4())
    fake_participant_id = str(uuid4())
    
    # Try to connect to non-existent interview
    with pytest.raises(Exception):
        with client.websocket_connect(
            f"/ws/interviews/{fake_id}?participantId={fake_participant_id}"
        ):
            pass


def test_websocket_connection_participant_not_found(client):
    """Test WebSocket connection with non-existent participant."""
    # Create interview
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "python",
            "creatorName": "User",
        },
    )
    interview_id = create_response.json()["id"]
    fake_participant_id = str(uuid4())
    
    # Try to connect with non-existent participant
    with pytest.raises(Exception):
        with client.websocket_connect(
            f"/ws/interviews/{interview_id}?participantId={fake_participant_id}"
        ):
            pass


def test_websocket_code_update_event(client):
    """Test sending code update events via WebSocket."""
    # Create interview
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "python",
            "creatorName": "User",
        },
    )
    interview_id = create_response.json()["id"]
    participant_id = create_response.json()["participants"][0]["id"]
    
    # Connect via WebSocket
    with client.websocket_connect(
        f"/ws/interviews/{interview_id}?participantId={participant_id}"
    ) as websocket:
        # Send code update event
        websocket.send_json({
            "event": "code_update",
            "payload": {
                "code": "print('Hello')",
                "participantId": str(participant_id),
            },
        })
        
        # Note: In a real scenario with multiple connections,
        # we would receive the broadcast here


def test_websocket_cursor_update_event(client):
    """Test sending cursor update events via WebSocket."""
    # Create interview
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "python",
            "creatorName": "User",
        },
    )
    interview_id = create_response.json()["id"]
    participant_id = create_response.json()["participants"][0]["id"]
    
    # Connect via WebSocket
    with client.websocket_connect(
        f"/ws/interviews/{interview_id}?participantId={participant_id}"
    ) as websocket:
        # Send cursor update event
        websocket.send_json({
            "event": "cursor_update",
            "payload": {
                "line": 10,
                "column": 5,
                "participantId": str(participant_id),
            },
        })
        
        # Note: In a real scenario with multiple connections,
        # we would receive the broadcast here


def test_websocket_disconnect_marks_participant_offline(client):
    """Test that disconnecting marks participant as offline."""
    # Create interview
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "python",
            "creatorName": "User",
        },
    )
    interview_id = create_response.json()["id"]
    participant_id = create_response.json()["participants"][0]["id"]
    
    # Connect and disconnect
    with client.websocket_connect(
        f"/ws/interviews/{interview_id}?participantId={participant_id}"
    ):
        pass  # Connection will be closed when exiting context
    
    # Verify participant is marked offline
    interview_response = client.get(f"/api/v1/interviews/{interview_id}")
    interview_data = interview_response.json()
    
    assert interview_data["participants"][0]["isOnline"] == False
