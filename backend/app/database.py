"""Database configuration and operations using SQLAlchemy."""
import os
import random
from typing import Optional, Generator
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.db_models import Base, InterviewModel, ParticipantModel, CodeExecutionModel
from app.models import Interview, Participant, CodeExecution, CursorPosition


# Database URL from environment variable, defaults to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./interviews.db")

# Create engine
# For SQLite, we need check_same_thread=False to allow usage across threads
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DatabaseManager:
    """Database manager for interview operations."""
    
    def __init__(self, session: Session):
        self.session = session
        self._participant_colors = [
            "#22d3ee", "#a855f7", "#f97316", "#10b981",
            "#ef4444", "#3b82f6", "#eab308", "#ec4899"
        ]
    
    def _get_random_color(self, used_colors: set[str]) -> str:
        """Get a random color that hasn't been used yet."""
        available = [c for c in self._participant_colors if c not in used_colors]
        if not available:
            available = self._participant_colors
        return random.choice(available)
    
    def _to_pydantic_participant(self, db_participant: ParticipantModel) -> Participant:
        """Convert SQLAlchemy Participant to Pydantic model."""
        cursor_position = None
        if db_participant.cursor_line is not None and db_participant.cursor_column is not None:
            cursor_position = CursorPosition(
                line=db_participant.cursor_line,
                column=db_participant.cursor_column
            )
        
        return Participant(
            id=db_participant.id,
            name=db_participant.name,
            role=db_participant.role,
            is_online=db_participant.is_online,
            cursor_position=cursor_position,
            color=db_participant.color
        )
    
    def _to_pydantic_execution(self, db_execution: CodeExecutionModel) -> CodeExecution:
        """Convert SQLAlchemy CodeExecution to Pydantic model."""
        return CodeExecution(
            id=db_execution.id,
            code=db_execution.code,
            language=db_execution.language,
            output=db_execution.output,
            error=db_execution.error,
            executed_at=db_execution.executed_at,
            executed_by=db_execution.executed_by
        )
    
    def _to_pydantic_interview(self, db_interview: InterviewModel) -> Interview:
        """Convert SQLAlchemy Interview to Pydantic model."""
        return Interview(
            id=db_interview.id,
            title=db_interview.title,
            code=db_interview.code,
            language=db_interview.language,
            participants=[self._to_pydantic_participant(p) for p in db_interview.participants],
            executions=[self._to_pydantic_execution(e) for e in db_interview.executions],
            created_at=db_interview.created_at,
            shareable_link=db_interview.shareable_link
        )
    
    def create_interview(self, interview: Interview) -> Interview:
        """Create a new interview."""
        # Create interview model
        db_interview = InterviewModel(
            id=interview.id,
            title=interview.title,
            code=interview.code,
            language=interview.language,
            created_at=interview.created_at,
            shareable_link=interview.shareable_link
        )
        
        # Add participants
        for participant in interview.participants:
            db_participant = ParticipantModel(
                id=participant.id,
                interview_id=interview.id,
                name=participant.name,
                role=participant.role,
                is_online=participant.is_online,
                color=participant.color,
                cursor_line=participant.cursor_position.line if participant.cursor_position else None,
                cursor_column=participant.cursor_position.column if participant.cursor_position else None
            )
            db_interview.participants.append(db_participant)
        
        self.session.add(db_interview)
        self.session.commit()
        self.session.refresh(db_interview)
        
        return self._to_pydantic_interview(db_interview)
    
    def get_interview(self, interview_id: UUID) -> Optional[Interview]:
        """Get an interview by ID."""
        db_interview = self.session.query(InterviewModel).filter(
            InterviewModel.id == interview_id
        ).first()
        
        if not db_interview:
            return None
        
        return self._to_pydantic_interview(db_interview)
    
    def update_interview(self, interview_id: UUID, interview: Interview) -> Optional[Interview]:
        """Update an existing interview."""
        db_interview = self.session.query(InterviewModel).filter(
            InterviewModel.id == interview_id
        ).first()
        
        if not db_interview:
            return None
        
        db_interview.title = interview.title
        db_interview.code = interview.code
        db_interview.language = interview.language
        
        self.session.commit()
        self.session.refresh(db_interview)
        
        return self._to_pydantic_interview(db_interview)
    
    def add_participant(self, interview_id: UUID, participant: Participant) -> Optional[Interview]:
        """Add a participant to an interview."""
        db_interview = self.session.query(InterviewModel).filter(
            InterviewModel.id == interview_id
        ).first()
        
        if not db_interview:
            return None
        
        # Assign a color if not already set
        color = participant.color
        if not color or color == "#000000":
            used_colors = {p.color for p in db_interview.participants}
            color = self._get_random_color(used_colors)
        
        db_participant = ParticipantModel(
            id=participant.id,
            interview_id=interview_id,
            name=participant.name,
            role=participant.role,
            is_online=participant.is_online,
            color=color,
            cursor_line=participant.cursor_position.line if participant.cursor_position else None,
            cursor_column=participant.cursor_position.column if participant.cursor_position else None
        )
        
        self.session.add(db_participant)
        self.session.commit()
        self.session.refresh(db_interview)
        
        return self._to_pydantic_interview(db_interview)
    
    def get_participant(self, interview_id: UUID, participant_id: UUID) -> Optional[Participant]:
        """Get a participant from an interview."""
        db_participant = self.session.query(ParticipantModel).filter(
            ParticipantModel.interview_id == interview_id,
            ParticipantModel.id == participant_id
        ).first()
        
        if not db_participant:
            return None
        
        return self._to_pydantic_participant(db_participant)
    
    def update_participant_cursor(
        self,
        interview_id: UUID,
        participant_id: UUID,
        line: int,
        column: int
    ) -> Optional[Participant]:
        """Update a participant's cursor position."""
        db_participant = self.session.query(ParticipantModel).filter(
            ParticipantModel.interview_id == interview_id,
            ParticipantModel.id == participant_id
        ).first()
        
        if not db_participant:
            return None
        
        db_participant.cursor_line = line
        db_participant.cursor_column = column
        
        self.session.commit()
        self.session.refresh(db_participant)
        
        return self._to_pydantic_participant(db_participant)
    
    def mark_participant_offline(self, interview_id: UUID, participant_id: UUID) -> Optional[Participant]:
        """Mark a participant as offline."""
        db_participant = self.session.query(ParticipantModel).filter(
            ParticipantModel.interview_id == interview_id,
            ParticipantModel.id == participant_id
        ).first()
        
        if not db_participant:
            return None
        
        db_participant.is_online = False
        
        self.session.commit()
        self.session.refresh(db_participant)
        
        return self._to_pydantic_participant(db_participant)
    
    def update_code(self, interview_id: UUID, code: str) -> Optional[Interview]:
        """Update the code in an interview."""
        db_interview = self.session.query(InterviewModel).filter(
            InterviewModel.id == interview_id
        ).first()
        
        if not db_interview:
            return None
        
        db_interview.code = code
        
        self.session.commit()
        self.session.refresh(db_interview)
        
        return self._to_pydantic_interview(db_interview)
    
    def add_execution(self, interview_id: UUID, execution: CodeExecution) -> Optional[Interview]:
        """Add a code execution to an interview."""
        db_interview = self.session.query(InterviewModel).filter(
            InterviewModel.id == interview_id
        ).first()
        
        if not db_interview:
            return None
        
        db_execution = CodeExecutionModel(
            id=execution.id,
            interview_id=interview_id,
            code=execution.code,
            language=execution.language,
            output=execution.output,
            error=execution.error,
            executed_at=execution.executed_at,
            executed_by=execution.executed_by
        )
        
        self.session.add(db_execution)
        self.session.commit()
        self.session.refresh(db_interview)
        
        return self._to_pydantic_interview(db_interview)


# For backward compatibility with existing code that uses db directly
# This will be replaced with dependency injection
class LegacyDatabaseWrapper:
    """Wrapper to maintain backward compatibility."""
    
    def __getattribute__(self, name):
        if name.startswith('_'):
            return object.__getattribute__(self, name)
        
        # Create a new session for each operation
        session = SessionLocal()
        try:
            manager = DatabaseManager(session)
            method = getattr(manager, name)
            
            # If it's a callable, wrap it to ensure session cleanup
            if callable(method):
                def wrapped(*args, **kwargs):
                    try:
                        result = method(*args, **kwargs)
                        return result
                    finally:
                        session.close()
                return wrapped
            else:
                session.close()
                return method
        except Exception:
            session.close()
            raise


db = LegacyDatabaseWrapper()

