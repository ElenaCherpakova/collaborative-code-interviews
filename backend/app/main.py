"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import interviews, participants, code, websocket


# Create FastAPI application
app = FastAPI(
    title="Collaborative Code Interview API",
    description=(
        "Backend API for a real-time collaborative coding interview platform. "
        "Supports multiple programming languages, real-time code collaboration, "
        "code execution, and participant management."
    ),
    version="1.0.0",
    contact={"name": "API Support"},
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(interviews.router, prefix="/api/v1")
app.include_router(participants.router, prefix="/api/v1")
app.include_router(code.router, prefix="/api/v1")
app.include_router(websocket.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Collaborative Code Interview API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
