# Collaborative Code Interview Platform

Real-time collaborative coding interview platform with FastAPI backend and React frontend.

## Quick Start

### Run Both Servers

```bash
npm run dev
```

This will start both the backend (port 8000) and frontend (port 5173) concurrently.

### Run Individually

**Backend only:**
```bash
npm run dev:backend
# or
cd backend && make dev
```

**Frontend only:**
```bash
npm run dev:frontend
# or
cd frontend && npm run dev
```

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   ├── tests/       # Backend tests
│   └── Makefile     # Backend commands
├── frontend/        # React frontend
│   ├── src/         # Source code
│   └── package.json
└── package.json     # Root package for running both
```

## Available Commands

### Root Level

- `npm run dev` - Run both frontend and backend
- `npm run dev:backend` - Run backend only
- `npm run dev:frontend` - Run frontend only
- `npm run test` - Run all tests (backend + frontend)
- `npm run seed` - Seed backend with sample data

### Backend (cd backend)

- `make dev` - Run development server
- `make test` - Run tests
- `make seed` - Seed database
- `make help` - See all available commands

### Frontend (cd frontend)

- `npm run dev` - Run development server
- `npm test` - Run tests
- `npm run build` - Build for production

## API Documentation

When the backend is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## Technologies

**Backend:**
- FastAPI
- Python 3.12+
- UV for dependency management
- Pytest for testing

**Frontend:**
- React 18
- TypeScript
- Vite
- Vitest for testing
- Monaco Editor for code editing

## Development

1. **Install dependencies:**
   ```bash
   # Backend
   cd backend && uv sync
   
   # Frontend
   cd frontend && npm install
   
   # Root (for concurrently)
   npm install
   ```

2. **Run development servers:**
   ```bash
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Testing

```bash
# All tests
npm run test

# Backend only
cd backend && make test

# Frontend only
cd frontend && npm test
```

## License

MIT
