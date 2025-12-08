"""SQLAlchemy ORM models for database tables."""
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Boolean,
    Integer,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import TypeDecorator, CHAR
import uuid

from app.models import ProgrammingLanguage, ParticipantRole


# Custom UUID type that works with both PostgreSQL and SQLite
class GUID(TypeDecorator):
    """Platform-independent GUID type.
    
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36), storing as stringified hex values.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PostgreSQLUUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            else:
                return value


Base = declarative_base()


class InterviewModel(Base):
    """SQLAlchemy model for Interview table."""
    
    __tablename__ = "interviews"
    
    id = Column(GUID, primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    code = Column(Text, default="", nullable=False)
    language = Column(SQLEnum(ProgrammingLanguage), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    shareable_link = Column(String(500), nullable=False)
    
    # Relationships
    participants = relationship(
        "ParticipantModel",
        back_populates="interview",
        cascade="all, delete-orphan",
        lazy="joined"
    )
    executions = relationship(
        "CodeExecutionModel",
        back_populates="interview",
        cascade="all, delete-orphan",
        lazy="joined"
    )
    
    def __repr__(self):
        return f"<Interview(id={self.id}, title={self.title})>"


class ParticipantModel(Base):
    """SQLAlchemy model for Participant table."""
    
    __tablename__ = "participants"
    
    id = Column(GUID, primary_key=True, default=uuid4)
    interview_id = Column(GUID, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    role = Column(SQLEnum(ParticipantRole), nullable=False)
    is_online = Column(Boolean, default=True, nullable=False)
    color = Column(String(7), nullable=False)
    cursor_line = Column(Integer, nullable=True)
    cursor_column = Column(Integer, nullable=True)
    
    # Relationship
    interview = relationship("InterviewModel", back_populates="participants")
    
    def __repr__(self):
        return f"<Participant(id={self.id}, name={self.name}, role={self.role})>"


class CodeExecutionModel(Base):
    """SQLAlchemy model for CodeExecution table."""
    
    __tablename__ = "code_executions"
    
    id = Column(GUID, primary_key=True, default=uuid4)
    interview_id = Column(GUID, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    code = Column(Text, nullable=False)
    language = Column(SQLEnum(ProgrammingLanguage), nullable=False)
    output = Column(Text, default="", nullable=False)
    error = Column(Text, nullable=True)
    executed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    executed_by = Column(GUID, nullable=False)
    
    # Relationship
    interview = relationship("InterviewModel", back_populates="executions")
    
    def __repr__(self):
        return f"<CodeExecution(id={self.id}, language={self.language})>"
