"""Code management and execution endpoints."""
from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.database import db
from app.models import (
    UpdateCodeRequest,
    ExecuteCodeRequest,
    ExecuteCodeResponse,
    CodeExecution,
    ErrorResponse,
)
from app.services.code_executor import code_executor
from app.services.websocket_manager import manager


router = APIRouter(prefix="/interviews", tags=["Code"])


@router.put(
    "/{interview_id}/code",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def update_code(interview_id: UUID, request: UpdateCodeRequest):
    """
    Update code in interview.
    
    Updates the code content in real-time. Should be called frequently during collaborative editing.
    """
    # Check if interview exists
    interview = db.get_interview(interview_id)
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Interview not found", "code": "NOT_FOUND"},
        )
    
    # Check if participant exists
    participant = db.get_participant(interview_id, request.participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Participant not found", "code": "NOT_FOUND"},
        )
    
    # Update code in database
    updated_interview = db.update_code(interview_id, request.code)
    
    if not updated_interview:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Failed to update code", "code": "INTERNAL_ERROR"},
        )
    
    # Broadcast code change via WebSocket
    await manager.broadcast(
        interview_id,
        {
            "event": "code_changed",
            "payload": {
                "code": request.code,
                "updatedBy": str(request.participant_id),
            },
        },
        exclude_participant=request.participant_id,
    )
    
    return None


@router.post(
    "/{interview_id}/execute",
    response_model=ExecuteCodeResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def execute_code(interview_id: UUID, request: ExecuteCodeRequest) -> ExecuteCodeResponse:
    """
    Execute code.
    
    Executes the provided code in a sandboxed environment and returns the output.
    Supports multiple programming languages. Execution is limited to prevent abuse.
    """
    # Check if interview exists
    interview = db.get_interview(interview_id)
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Interview not found", "code": "NOT_FOUND"},
        )
    
    # Check if participant exists
    participant = db.get_participant(interview_id, request.participant_id)
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Participant not found", "code": "NOT_FOUND"},
        )
    
    # Execute code
    output, error, execution_time = await code_executor.execute(request.code, request.language)
    
    # Create execution record
    execution = CodeExecution(
        code=request.code,
        language=request.language,
        output=output,
        error=error,
        executed_by=request.participant_id,
    )
    
    # Add execution to interview history
    db.add_execution(interview_id, execution)
    
    # Broadcast execution result via WebSocket
    await manager.broadcast(
        interview_id,
        {
            "event": "execution_completed",
            "payload": execution.model_dump(mode="json"),
        },
    )
    
    return ExecuteCodeResponse(
        output=output,
        error=error,
        execution_time=execution_time,
    )
