"""WebSocket endpoint for real-time updates."""
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status

from app.database import db
from app.services.websocket_manager import manager


router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/interviews/{interview_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    interview_id: UUID,
    participantId: UUID = Query(..., description="ID of the participant connecting"),
):
    """
    WebSocket connection for real-time updates.
    
    Establishes a WebSocket connection for real-time updates including:
    - Code changes from other participants
    - Participant join/leave events
    - Cursor position updates
    - Code execution results
    """
    # Check if interview exists
    interview = db.get_interview(interview_id)
    if not interview:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Interview not found")
        return
    
    # Check if participant exists
    participant = db.get_participant(interview_id, participantId)
    if not participant:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Participant not found")
        return
    
    # Accept connection
    await manager.connect(websocket, interview_id, participantId)
    
    try:
        # Keep connection alive and handle incoming messages
        while True:
            # Receive messages from client
            data = await websocket.receive_json()
            
            # Handle different event types
            event_type = data.get("event")
            
            if event_type == "code_update":
                # Broadcast code update to other participants
                await manager.broadcast(
                    interview_id,
                    {
                        "event": "code_changed",
                        "payload": {
                            "code": data.get("payload", {}).get("code", ""),
                            "updatedBy": str(participantId),
                        },
                    },
                    exclude_participant=participantId,
                )
            
            elif event_type == "cursor_update":
                # Broadcast cursor update to other participants
                payload = data.get("payload", {})
                await manager.broadcast(
                    interview_id,
                    {
                        "event": "cursor_moved",
                        "payload": {
                            "participantId": str(participantId),
                            "position": {
                                "line": payload.get("line", 0),
                                "column": payload.get("column", 0),
                            },
                        },
                    },
                    exclude_participant=participantId,
                )
    
    except WebSocketDisconnect:
        # Handle disconnection
        manager.disconnect(websocket, interview_id, participantId)
        
        # Mark participant as offline
        db.mark_participant_offline(interview_id, participantId)
        
        # Broadcast participant left event
        await manager.broadcast(
            interview_id,
            {
                "event": "participant_left",
                "payload": {"participantId": str(participantId)},
            },
        )
    
    except Exception as e:
        # Handle other errors
        manager.disconnect(websocket, interview_id, participantId)
        print(f"WebSocket error: {e}")
