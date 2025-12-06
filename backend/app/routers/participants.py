"""Participant management endpoints."""
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.database import db
from app.models import (
    JoinInterviewRequest,
    JoinInterviewResponse,
    CursorPosition,
    Participant,
    ErrorResponse,
)
from app.services.websocket_manager import manager


router = APIRouter(prefix="/interviews", tags=["Participants"])


@router.post(
    "/{interview_id}/join",
    response_model=JoinInterviewResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def join_interview(interview_id: UUID, request: JoinInterviewRequest) -> JoinInterviewResponse:
    """
    Join an existing interview.
    
    Adds a new participant to an existing interview session.
    """
    # Check if interview exists
    interview = db.get_interview(interview_id)
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Interview not found", "code": "NOT_FOUND"},
        )
    
    # Create new participant
    participant = Participant(
        name=request.participant_name,
        role=request.role,
        is_online=True,
        color="#000000",  # Will be assigned by database
    )
    
    # Add participant to interview
    updated_interview = db.add_participant(interview_id, participant)
    
    if not updated_interview:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Failed to add participant", "code": "INTERNAL_ERROR"},
        )
    
    # Broadcast participant joined event via WebSocket
    await manager.broadcast(
        interview_id,
        {
            "event": "participant_joined",
            "payload": participant.model_dump(mode="json"),
        },
    )
    
    return JoinInterviewResponse(interview=updated_interview, participant=participant)


@router.put(
    "/{interview_id}/participants/{participant_id}/cursor",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_cursor_position(
    interview_id: UUID, participant_id: UUID, cursor: CursorPosition
):
    """
    Update participant cursor position.
    
    Updates the cursor position for real-time cursor tracking.
    """
    # Update cursor in database
    participant = db.update_participant_cursor(
        interview_id, participant_id, cursor.line, cursor.column
    )
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Participant not found", "code": "NOT_FOUND"},
        )
    
    # Broadcast cursor update via WebSocket
    await manager.broadcast(
        interview_id,
        {
            "event": "cursor_moved",
            "payload": {
                "participantId": str(participant_id),
                "position": cursor.model_dump(),
            },
        },
        exclude_participant=participant_id,
    )
    
    return None


@router.post(
    "/{interview_id}/participants/{participant_id}/leave",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def leave_interview(interview_id: UUID, participant_id: UUID):
    """
    Leave interview.
    
    Marks a participant as offline/left the interview.
    """
    # Mark participant as offline
    participant = db.mark_participant_offline(interview_id, participant_id)
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Participant not found", "code": "NOT_FOUND"},
        )
    
    # Broadcast participant left event via WebSocket
    await manager.broadcast(
        interview_id,
        {
            "event": "participant_left",
            "payload": {"participantId": str(participant_id)},
        },
    )
    
    return None
