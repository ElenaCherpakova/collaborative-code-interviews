"""WebSocket connection manager for real-time updates."""
from typing import Dict, Set
from uuid import UUID
from fastapi import WebSocket


class ConnectionManager:
    """Manages WebSocket connections for interviews."""
    
    def __init__(self):
        # interview_id -> set of (websocket, participant_id)
        self.active_connections: Dict[UUID, Set[tuple[WebSocket, UUID]]] = {}
    
    async def connect(self, websocket: WebSocket, interview_id: UUID, participant_id: UUID):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        
        if interview_id not in self.active_connections:
            self.active_connections[interview_id] = set()
        
        self.active_connections[interview_id].add((websocket, participant_id))
    
    def disconnect(self, websocket: WebSocket, interview_id: UUID, participant_id: UUID):
        """Remove a WebSocket connection."""
        if interview_id in self.active_connections:
            self.active_connections[interview_id].discard((websocket, participant_id))
            
            # Clean up empty interview rooms
            if not self.active_connections[interview_id]:
                del self.active_connections[interview_id]
    
    async def broadcast(self, interview_id: UUID, message: dict, exclude_participant: UUID | None = None):
        """Broadcast a message to all participants in an interview."""
        if interview_id not in self.active_connections:
            return
        
        disconnected = []
        for websocket, participant_id in self.active_connections[interview_id]:
            # Skip the participant who triggered the event if specified
            if exclude_participant and participant_id == exclude_participant:
                continue
            
            try:
                await websocket.send_json(message)
            except Exception:
                # Mark for removal if send fails
                disconnected.append((websocket, participant_id))
        
        # Remove disconnected clients
        for websocket, participant_id in disconnected:
            self.disconnect(websocket, interview_id, participant_id)
    
    async def send_to_participant(self, interview_id: UUID, participant_id: UUID, message: dict):
        """Send a message to a specific participant."""
        if interview_id not in self.active_connections:
            return
        
        for websocket, pid in self.active_connections[interview_id]:
            if pid == participant_id:
                try:
                    await websocket.send_json(message)
                except Exception:
                    self.disconnect(websocket, interview_id, participant_id)
                break


# Global connection manager instance
manager = ConnectionManager()
