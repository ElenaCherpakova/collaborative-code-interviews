"""Interview management endpoints."""
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.database import db
from app.models import (
    CreateInterviewRequest,
    Interview,
    Participant,
    ParticipantRole,
    ErrorResponse,
)


router = APIRouter(prefix="/interviews", tags=["Interviews"])


@router.post(
    "",
    response_model=Interview,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_interview(request: CreateInterviewRequest) -> Interview:
    """
    Create a new interview session.
    
    Creates a new collaborative coding interview session with the creator as the first participant.
    """
    # Create the creator as the first participant
    creator = Participant(
        name=request.creator_name,
        role=ParticipantRole.INTERVIEWER,
        is_online=True,
        color="#22d3ee",  # Default color, will be assigned by database
    )
    
    # Create the interview
    interview = Interview(
        title=request.title,
        language=request.language,
        code="",  # Start with empty code
        participants=[creator],
        executions=[],
        shareable_link="",  # Will be set below
    )
    
    # Update shareable link with actual ID (point to frontend)
    # In production, this should come from environment variable
    frontend_url = "http://localhost:8080"  # Vite dev server port
    interview.shareable_link = f"{frontend_url}/interview/{interview.id}"
    
    # Save to database
    created_interview = db.create_interview(interview)
    
    return created_interview


@router.get(
    "/{interview_id}",
    response_model=Interview,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def get_interview(interview_id: UUID) -> Interview:
    """
    Get interview by ID.
    
    Retrieves an existing interview session with all participants and code.
    """
    interview = db.get_interview(interview_id)
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Interview not found", "code": "NOT_FOUND"},
        )
    
    return interview
