# Collaborative Code Interview Backend

FastAPI backend for a real-time collaborative coding interview platform.

## Features

- ✅ RESTful API for interview management
- ✅ WebSocket support for real-time collaboration
- ✅ Code execution in 7 programming languages (Python, JavaScript, TypeScript, Java, C++, Go, Rust)
- ✅ Participant management with cursor tracking
- ✅ Mock database (easily replaceable with PostgreSQL/MongoDB)
- ✅ Comprehensive test suite (26 tests)

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management

### Installation

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest tests/ -v

# Start development server
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## API Endpoints

### Interviews
- `POST /api/v1/interviews` - Create new interview
- `GET /api/v1/interviews/{interviewId}` - Get interview details

### Participants
- `POST /api/v1/interviews/{interviewId}/join` - Join interview
- `PUT /api/v1/interviews/{interviewId}/participants/{participantId}/cursor` - Update cursor
- `POST /api/v1/interviews/{interviewId}/participants/{participantId}/leave` - Leave interview

### Code
- `PUT /api/v1/interviews/{interviewId}/code` - Update code
- `POST /api/v1/interviews/{interviewId}/execute` - Execute code

### WebSocket
- `GET /ws/interviews/{interviewId}?participantId={participantId}` - Real-time updates

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── database.py          # Mock database
│   ├── routers/             # API endpoints
│   └── services/            # Business logic
├── tests/                   # Test suite
└── pyproject.toml          # Dependencies
```

## Development

### Running Tests

```bash
# All tests
uv run pytest tests/ -v

# Specific test file
uv run pytest tests/test_interviews.py -v

# With coverage
uv run pytest tests/ --cov=app
```

### Adding Dependencies

```bash
# Add production dependency
uv add <package_name>

# Add development dependency
uv add --dev <package_name>
```

## Mock Services

### Database
Currently uses in-memory storage. To replace with a real database:
1. Install database driver (e.g., `uv add sqlalchemy asyncpg`)
2. Update `app/database.py` with database operations
3. Create migration scripts

### Code Execution
Currently simulates execution. For production:
- Use Docker containers for sandboxing
- Integrate with Judge0 or Piston API
- Implement AWS Lambda execution

### WebSocket
In-memory connection manager. For multi-instance deployments:
- Add Redis: `uv add redis`
- Implement Redis pub/sub for broadcasting

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation with:
- All endpoint details
- Request/response schemas
- Try-it-out functionality

## Testing

All 26 tests pass successfully, covering:
- Interview creation and retrieval
- Participant management
- Code updates and execution
- WebSocket connections
- Error handling

## License

MIT
