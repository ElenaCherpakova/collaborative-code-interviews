"""Integration tests for interview lifecycle."""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db_models import InterviewModel

def test_interview_lifecycle_with_persistence(client):
    """
    Test the full lifecycle of an interview with persistence verification.
    
    Flow:
    1. Create an interview
    2. Join with a new participant
    3. multiple participants join
    4. Update code
    5. Verify data exists in real DB file
    6. Verify data persists across new sessions
    """
    # 1. Create Interview
    create_response = client.post(
        "/api/v1/interviews",
        json={
            "title": "Integration Test Interview",
            "language": "python",
            "creatorName": "Host User"
        }
    )
    assert create_response.status_code == 201
    interview_data = create_response.json()
    interview_id = interview_data["id"]
    
    assert interview_data["title"] == "Integration Test Interview"
    assert len(interview_data["participants"]) == 1
    host_id = interview_data["participants"][0]["id"]
    
    # 2. Join Interview
    join_response = client.post(
        f"/api/v1/interviews/{interview_id}/join",
        json={
            "participantName": "Candidate User",
            "role": "candidate"
        }
    )
    assert join_response.status_code == 200
    join_data = join_response.json()
    candidate_id = join_data["participant"]["id"]
    
    assert len(join_data["interview"]["participants"]) == 2
    
    # 3. Update Code
    new_code = "def solution():\n    return 'tested'"
    update_response = client.put(
        f"/api/v1/interviews/{interview_id}/code",
        json={
            "code": new_code,
            "participantId": candidate_id
        }
    )
    assert update_response.status_code == 204
    
    # 4. Verify data via API
    get_response = client.get(f"/api/v1/interviews/{interview_id}")
    assert get_response.status_code == 200
    current_data = get_response.json()
    assert current_data["code"] == new_code
    assert len(current_data["participants"]) == 2
    
    # 5. Verify Persistence (Direct DB Access)
    # Check that file exists
    assert os.path.exists("test_integration.db")
    
    # Create a completely new engine/session to verify persistence
    # avoiding any shared in-memory state from the app
    verify_engine = create_engine("sqlite:///./test_integration.db")
    VerifySession = sessionmaker(bind=verify_engine)
    session = VerifySession()
    
    try:
        # Check if interview exists (the ID is stored as CHAR(36) in SQLite but mapped to UUID in Python)
        # We can query by ID directly since SQLAlchemy handles the type conversion via our GUID type
        db_interview = session.query(InterviewModel).filter_by(id=interview_id).first()
        
        assert db_interview is not None, f"Interview with ID {interview_id} not found in persistent DB"
        assert str(db_interview.id) == interview_id
        assert db_interview.title == "Integration Test Interview"
        assert db_interview.code == new_code
        
        # Check participants
        assert len(db_interview.participants) == 2
        participant_names = [p.name for p in db_interview.participants]
        assert "Host User" in participant_names
        assert "Candidate User" in participant_names
        
    finally:
        session.close()


