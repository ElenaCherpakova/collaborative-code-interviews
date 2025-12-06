"""Tests for interview endpoints."""
import pytest
from uuid import uuid4


def test_create_interview_success(client):
    """Test creating an interview with valid data."""
    response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Senior Backend Engineer Interview",
            "language": "python",
            "creatorName": "John Doe",
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["title"] == "Senior Backend Engineer Interview"
    assert data["language"] == "python"
    assert data["code"] == ""
    assert len(data["participants"]) == 1
    assert data["participants"][0]["name"] == "John Doe"
    assert data["participants"][0]["role"] == "interviewer"
    assert "id" in data
    assert "shareableLink" in data


def test_create_interview_invalid_language(client):
    """Test creating an interview with invalid language."""
    response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "invalid_language",
            "creatorName": "John Doe",
        },
    )
    
    assert response.status_code == 422  # Validation error


def test_get_interview_success(client):
    """Test getting an existing interview."""
    # First create an interview
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Test Interview",
            "language": "javascript",
            "creatorName": "Jane Smith",
        },
    )
    interview_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/interviews/{interview_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == interview_id
    assert data["title"] == "Test Interview"
    assert data["language"] == "javascript"


def test_get_interview_not_found(client):
    """Test getting a non-existent interview."""
    fake_id = str(uuid4())
    response = client.get(f"/api/v1/interviews/{fake_id}")
    
    assert response.status_code == 404


def test_create_interview_with_different_languages(client):
    """Test creating interviews with different programming languages."""
    languages = ["python", "javascript", "typescript", "java", "cpp", "go", "rust"]
    
    for lang in languages:
        response = client.post(
            "/api/v1/interviews",
            json={
                "title": f"{lang.upper()} Interview",
                "language": lang,
                "creatorName": "Test User",
            },
        )
        
        assert response.status_code == 201
        assert response.json()["language"] == lang
