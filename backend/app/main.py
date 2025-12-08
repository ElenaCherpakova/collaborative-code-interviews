"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import interviews, participants, code, websocket
from app.database import init_db
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



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


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Collaborative Code Interview API",
        "version": "1.0.0",
        "docs": "/docs",
        "deploy_mode": "unified" if os.path.exists(STATIC_DIR) else "api_only"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Mount static files if directory exists (for production/docker)
STATIC_DIR = "/app/static"
if os.path.exists(STATIC_DIR):
    # Mount assets (JS/CSS/images)
    app.mount("/assets", StaticFiles(directory=f"{STATIC_DIR}/assets"), name="assets")
    
    # Catch-all route for SPA - must be last
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow API routes to pass through (though they should be matched above)
        if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
             return {"error": "Not Found", "path": full_path}
             
        # Serve index.html for all other routes
        return FileResponse(f"{STATIC_DIR}/index.html")

