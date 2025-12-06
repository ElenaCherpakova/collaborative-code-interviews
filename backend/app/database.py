"""Mock database implementation using in-memory storage."""
import random
from threading import Lock
from typing import Optional
from uuid import UUID

from app.models import Interview, Participant, CodeExecution


class MockDatabase:
    """Thread-safe in-memory database for interviews."""
    
    def __init__(self):
        self._interviews: dict[UUID, Interview] = {}
        self._lock = Lock()
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
    
    def create_interview(self, interview: Interview) -> Interview:
        """Create a new interview."""
        with self._lock:
            self._interviews[interview.id] = interview
            return interview
    
    def get_interview(self, interview_id: UUID) -> Optional[Interview]:
        """Get an interview by ID."""
        with self._lock:
            return self._interviews.get(interview_id)
    
    def update_interview(self, interview_id: UUID, interview: Interview) -> Optional[Interview]:
        """Update an existing interview."""
        with self._lock:
            if interview_id not in self._interviews:
                return None
            self._interviews[interview_id] = interview
            return interview
    
    def add_participant(self, interview_id: UUID, participant: Participant) -> Optional[Interview]:
        """Add a participant to an interview."""
        with self._lock:
            interview = self._interviews.get(interview_id)
            if not interview:
                return None
            
            # Assign a color if not already set
            if not participant.color or participant.color == "#000000":
                used_colors = {p.color for p in interview.participants}
                participant.color = self._get_random_color(used_colors)
            
            interview.participants.append(participant)
            return interview
    
    def get_participant(self, interview_id: UUID, participant_id: UUID) -> Optional[Participant]:
        """Get a participant from an interview."""
        with self._lock:
            interview = self._interviews.get(interview_id)
            if not interview:
                return None
            
            for participant in interview.participants:
                if participant.id == participant_id:
                    return participant
            return None
    
    def update_participant_cursor(
        self, 
        interview_id: UUID, 
        participant_id: UUID, 
        line: int, 
        column: int
    ) -> Optional[Participant]:
        """Update a participant's cursor position."""
        with self._lock:
            interview = self._interviews.get(interview_id)
            if not interview:
                return None
            
            for participant in interview.participants:
                if participant.id == participant_id:
                    from app.models import CursorPosition
                    participant.cursor_position = CursorPosition(line=line, column=column)
                    return participant
            return None
    
    def mark_participant_offline(self, interview_id: UUID, participant_id: UUID) -> Optional[Participant]:
        """Mark a participant as offline."""
        with self._lock:
            interview = self._interviews.get(interview_id)
            if not interview:
                return None
            
            for participant in interview.participants:
                if participant.id == participant_id:
                    participant.is_online = False
                    return participant
            return None
    
    def update_code(self, interview_id: UUID, code: str) -> Optional[Interview]:
        """Update the code in an interview."""
        with self._lock:
            interview = self._interviews.get(interview_id)
            if not interview:
                return None
            
            interview.code = code
            return interview
    
    def add_execution(self, interview_id: UUID, execution: CodeExecution) -> Optional[Interview]:
        """Add a code execution to an interview."""
        with self._lock:
            interview = self._interviews.get(interview_id)
            if not interview:
                return None
            
            interview.executions.append(execution)
            return interview


# Global database instance
db = MockDatabase()
