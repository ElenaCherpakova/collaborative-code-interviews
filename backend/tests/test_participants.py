"""Tests for participant endpoints."""
import pytest
from uuid import uuid4


def test_join_interview_success(client):
    """Test joining an interview with valid data."""
    # Create an interview first
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "python",
            "creatorName": "Interviewer",
        },
    )
    interview_id = create_response.json()["id"]
    
    # Join the interview
    response = client.post(
        f"/api/v1/interviews/{interview_id}/join",
        json={
            "participantName": "Candidate",
            "role": "candidate",
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "interview" in data
    assert "participant" in data
    assert data["participant"]["name"] == "Candidate"
    assert data["participant"]["role"] == "candidate"
    assert len(data["interview"]["participants"]) == 2


def test_join_interview_not_found(client):
    """Test joining a non-existent interview."""
    fake_id = str(uuid4())
    response = client.post(
        f"/api/v1/interviews/{fake_id}/join",
        json={
            "participantName": "Test User",
            "role": "candidate",
        },
    )
    
    assert response.status_code == 404


def test_update_cursor_position_success(client):
    """Test updating cursor position."""
    # Create interview and join
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
    
    # Update cursor
    response = client.put(
        f"/api/v1/interviews/{interview_id}/participants/{participant_id}/cursor",
        json={"line": 10, "column": 5},
    )
    
    assert response.status_code == 204


def test_update_cursor_position_not_found(client):
    """Test updating cursor for non-existent participant."""
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
    
    # Try to update cursor for non-existent participant
    response = client.put(
        f"/api/v1/interviews/{interview_id}/participants/{fake_participant_id}/cursor",
        json={"line": 10, "column": 5},
    )
    
    assert response.status_code == 404


def test_leave_interview_success(client):
    """Test leaving an interview."""
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
    
    # Leave interview
    response = client.post(
        f"/api/v1/interviews/{interview_id}/participants/{participant_id}/leave"
    )
    
    assert response.status_code == 204
    
    # Verify participant is marked offline
    interview_response = client.get(f"/api/v1/interviews/{interview_id}")
    interview_data = interview_response.json()
    
    assert interview_data["participants"][0]["isOnline"] == False


def test_leave_interview_not_found(client):
    """Test leaving with non-existent participant."""
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
    
    # Try to leave with non-existent participant
    response = client.post(
        f"/api/v1/interviews/{interview_id}/participants/{fake_participant_id}/leave"
    )
    
    assert response.status_code == 404


def test_multiple_participants_join(client):
    """Test multiple participants joining the same interview."""
    # Create interview
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "python",
            "creatorName": "Interviewer",
        },
    )
    interview_id = create_response.json()["id"]
    
    # Join as candidate 1
    response1 = client.post(
        f"/api/v1/interviews/{interview_id}/join",
        json={
            "participantName": "Candidate 1",
            "role": "candidate",
        },
    )
    assert response1.status_code == 200
    
    # Join as candidate 2
    response2 = client.post(
        f"/api/v1/interviews/{interview_id}/join",
        json={
            "participantName": "Candidate 2",
            "role": "candidate",
        },
    )
    assert response2.status_code == 200
    
    # Verify all participants are in the interview
    interview_response = client.get(f"/api/v1/interviews/{interview_id}")
    interview_data = interview_response.json()
    
    assert len(interview_data["participants"]) == 3
    participant_names = [p["name"] for p in interview_data["participants"]]
    assert "Interviewer" in participant_names
    assert "Candidate 1" in participant_names
    assert "Candidate 2" in participant_names
