"""Tests for code endpoints."""
import pytest
from uuid import uuid4


def test_update_code_success(client):
    """Test updating code in an interview."""
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
    
    # Update code
    code = "def hello():\n    print('Hello, World!')"
    response = client.put(
        f"/api/v1/interviews/{interview_id}/code",
        json={
            "code": code,
            "participantId": participant_id,
        },
    )
    
    assert response.status_code == 204
    
    # Verify code was updated
    interview_response = client.get(f"/api/v1/interviews/{interview_id}")
    interview_data = interview_response.json()
    
    assert interview_data["code"] == code


def test_update_code_interview_not_found(client):
    """Test updating code for non-existent interview."""
    fake_id = str(uuid4())
    fake_participant_id = str(uuid4())
    
    response = client.put(
        f"/api/v1/interviews/{fake_id}/code",
        json={
            "code": "test code",
            "participantId": fake_participant_id,
        },
    )
    
    assert response.status_code == 404


def test_update_code_participant_not_found(client):
    """Test updating code with non-existent participant."""
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
    
    # Try to update code with non-existent participant
    response = client.put(
        f"/api/v1/interviews/{interview_id}/code",
        json={
            "code": "test code",
            "participantId": fake_participant_id,
        },
    )
    
    assert response.status_code == 404


def test_execute_code_success(client):
    """Test executing code successfully."""
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
    
    # Execute code
    response = client.post(
        f"/api/v1/interviews/{interview_id}/execute",
        json={
            "code": "print('Hello, World!')",
            "language": "python",
            "participantId": participant_id,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "output" in data
    assert "executionTime" in data
    assert data["output"] != ""


def test_execute_code_with_error(client):
    """Test executing code that contains an error."""
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
    
    # Execute code with error
    response = client.post(
        f"/api/v1/interviews/{interview_id}/execute",
        json={
            "code": "raise error('This is an error')",
            "language": "python",
            "participantId": participant_id,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "error" in data
    assert data["error"] is not None


def test_execute_code_interview_not_found(client):
    """Test executing code for non-existent interview."""
    fake_id = str(uuid4())
    fake_participant_id = str(uuid4())
    
    response = client.post(
        f"/api/v1/interviews/{fake_id}/execute",
        json={
            "code": "print('test')",
            "language": "python",
            "participantId": fake_participant_id,
        },
    )
    
    assert response.status_code == 404


def test_execute_code_creates_execution_history(client):
    """Test that code execution creates execution history."""
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
    
    # Execute code
    client.post(
        f"/api/v1/interviews/{interview_id}/execute",
        json={
            "code": "print('First execution')",
            "language": "python",
            "participantId": participant_id,
        },
    )
    
    # Execute again
    client.post(
        f"/api/v1/interviews/{interview_id}/execute",
        json={
            "code": "print('Second execution')",
            "language": "python",
            "participantId": participant_id,
        },
    )
    
    # Verify execution history
    interview_response = client.get(f"/api/v1/interviews/{interview_id}")
    interview_data = interview_response.json()
    
    assert len(interview_data["executions"]) == 2
    assert interview_data["executions"][0]["code"] == "print('First execution')"
    assert interview_data["executions"][1]["code"] == "print('Second execution')"


def test_execute_code_different_languages(client):
    """Test executing code in different programming languages."""
    languages = ["python", "javascript", "typescript", "java", "cpp", "go", "rust"]
    
    for lang in languages:
        # Create interview
        create_response = client.post(
            "/api/v1/interviews",
            json={
                "title": f"{lang} Interview",
                "language": lang,
                "creatorName": "User",
            },
        )
        interview_id = create_response.json()["id"]
        participant_id = create_response.json()["participants"][0]["id"]
        
        # Execute code
        response = client.post(
            f"/api/v1/interviews/{interview_id}/execute",
            json={
                "code": f"print('Hello from {lang}')",
                "language": lang,
                "participantId": participant_id,
            },
        )
        
        assert response.status_code == 200
        assert "output" in response.json()
