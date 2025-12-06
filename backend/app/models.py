"""Pydantic models matching OpenAPI schemas."""
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class ProgrammingLanguage(str, Enum):
    """Supported programming languages."""
    
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    PYTHON = "python"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"


class ParticipantRole(str, Enum):
    """Role of the participant in the interview."""
    
    INTERVIEWER = "interviewer"
    CANDIDATE = "candidate"


class CursorPosition(BaseModel):
    """Cursor position in the code editor."""
    
    line: int = Field(..., ge=0, description="Line number (0-indexed)")
    column: int = Field(..., ge=0, description="Column number (0-indexed)")


class Participant(BaseModel):
    """Participant in an interview session."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the participant")
    name: str = Field(..., min_length=1, max_length=100, description="Display name of the participant")
    role: ParticipantRole
    is_online: bool = Field(default=True, description="Whether the participant is currently connected", serialization_alias="isOnline")
    cursor_position: Optional[CursorPosition] = Field(default=None, serialization_alias="cursorPosition")
    color: str = Field(..., pattern=r"^#[0-9a-fA-F]{6}$", description="Hex color code for participant's cursor/avatar")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "John Doe",
                "role": "interviewer",
                "isOnline": True,
                "cursorPosition": {"line": 10, "column": 5},
                "color": "#22d3ee"
            }
        }
    }


class CodeExecution(BaseModel):
    """Record of code execution."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for this execution")
    code: str = Field(..., description="The code that was executed")
    language: ProgrammingLanguage
    output: str = Field(default="", description="Standard output from code execution")
    error: Optional[str] = Field(default=None, description="Error message if execution failed")
    executed_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when code was executed", serialization_alias="executedAt")
    executed_by: UUID = Field(..., description="ID of participant who executed the code", serialization_alias="executedBy")


class Interview(BaseModel):
    """Interview session."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the interview")
    title: str = Field(..., min_length=1, max_length=200, description="Title of the interview session")
    code: str = Field(default="", description="Current code content")
    language: ProgrammingLanguage
    participants: list[Participant] = Field(default_factory=list, description="List of all participants in the interview")
    executions: list[CodeExecution] = Field(default_factory=list, description="History of code executions")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when interview was created", serialization_alias="createdAt")
    shareable_link: str = Field(..., description="Shareable link to join the interview", serialization_alias="shareableLink")


# Request/Response Models

class CreateInterviewRequest(BaseModel):
    """Request to create a new interview."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Title for the interview session")
    language: ProgrammingLanguage
    creator_name: str = Field(..., min_length=1, max_length=100, description="Name of the person creating the interview", alias="creatorName")
    
    model_config = {"populate_by_name": True}


class JoinInterviewRequest(BaseModel):
    """Request to join an existing interview."""
    
    participant_name: str = Field(..., min_length=1, max_length=100, description="Name of the person joining", alias="participantName")
    role: ParticipantRole
    
    model_config = {"populate_by_name": True}


class JoinInterviewResponse(BaseModel):
    """Response when joining an interview."""
    
    interview: Interview
    participant: Participant = Field(..., description="The newly created participant object")


class UpdateCodeRequest(BaseModel):
    """Request to update code in an interview."""
    
    code: str = Field(..., description="Updated code content")
    participant_id: UUID = Field(..., description="ID of participant making the update", alias="participantId")
    
    model_config = {"populate_by_name": True}


class ExecuteCodeRequest(BaseModel):
    """Request to execute code."""
    
    code: str = Field(..., description="Code to execute")
    language: ProgrammingLanguage
    participant_id: UUID = Field(..., description="ID of participant executing the code", alias="participantId")
    
    model_config = {"populate_by_name": True}


class ExecuteCodeResponse(BaseModel):
    """Response from code execution."""
    
    output: str = Field(..., description="Standard output from execution")
    error: Optional[str] = Field(default=None, description="Error message if execution failed")
    execution_time: float = Field(..., description="Execution time in milliseconds", alias="executionTime")
    
    model_config = {"populate_by_name": True}


class ErrorResponse(BaseModel):
    """Error response."""
    
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(default=None, description="Error code for programmatic handling")
    details: Optional[dict] = Field(default=None, description="Additional error details")
