# HR Resume Review Platform

A real-time collaborative platform for HR teams to evaluate and review resumes. Built with React, FastAPI, and WebSockets.

## Development Approach

This project follows a **frontend-first development approach**:

1. **Frontend** - Built first with mock data
2. **OpenAPI Specs** - API contract defined in `openapi.yaml`
3. **Backend** - Implemented to match the OpenAPI specification

## Features

- 📄 **Resume Upload**: Upload resumes in PDF and TXT formats
- 🔄 **CRUD Operations**: Create, read, update, and delete resumes
- ⭐ **Evaluation System**: Rate and comment on resumes
- 💬 **Real-time Chat**: Discuss resumes with team members in real-time
- 🔄 **Real-time Updates**: See changes instantly across all connected users

## Tech Stack

### Frontend
- React 18
- Vite
- React Router
- Axios
- WebSocket API

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- WebSockets
- PyPDF2 (for PDF parsing)

## Project Structure

```
project/
├── frontend/              # Step 1: Frontend with mocks
│   ├── src/
│   │   ├── api/
│   │   │   ├── resumes.js    # API client (supports mocks)
│   │   │   └── mock.js        # Mock data for development
│   │   └── components/
│   └── package.json
├── openapi.yaml           # Step 2: API specification
├── backend/               # Step 3: Backend implementation
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   └── pyproject.toml
└── infra/                 # Infrastructure configuration
    ├── docker-compose.yml # Docker Compose configuration
    └── init-db/           # Database initialization scripts
        └── 01-init.sql    # SQL initialization script
```

## Getting Started

### Step 1: Frontend Development (with Mocks)

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server with mock data:
```bash
npm run dev
```

The frontend will use mock data by default (when `VITE_API_URL` is not set). To use mock data explicitly:
```bash
VITE_USE_MOCK=true npm run dev
```

4. Open http://localhost:5173 in your browser

The frontend works independently with mock data, allowing you to develop and test the UI without a backend.

### Step 2: OpenAPI Specification

The API contract is defined in `openapi.yaml`. This specification:
- Defines all endpoints, request/response schemas
- Serves as the contract between frontend and backend
- Can be used to generate API clients
- Can be viewed at http://localhost:8000/docs when backend is running

View the specification:
```bash
cat openapi.yaml
```

Or use tools like Swagger Editor to visualize it.

### Step 3: Backend Development

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies using `uv`:
```bash
uv sync
```

The `uv.toml` configuration file is already set up to suppress hardlink warnings on Windows.

3. Create a `.env` file (optional, for custom database configuration):
```bash
# Create .env file with your database settings
echo "DATABASE_URL=postgresql://resume_review:resume_review_password@localhost:5432/resume_review" > .env
```

**Note**: If `.env` is not created, the backend will use the default database URL from `app/database.py`.

4. Make sure PostgreSQL is running. You can use Docker Compose to start PostgreSQL:
```bash
cd ../infra
docker-compose up db -d
cd ../backend
```

5. Start the backend server:
```bash
uv run uvicorn app.main:app --reload
```

6. The API will be available at http://localhost:8000
7. API documentation (Swagger UI) at http://localhost:8000/docs

### Running Frontend with Real Backend

Once the backend is running, update frontend environment:

1. Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=localhost:8000
```

2. Restart the frontend dev server:
```bash
cd frontend
npm run dev
```

## Using Docker

### Option 1: Full Stack (Frontend + Backend + Database)

```bash
cd project/infra
docker-compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Note: Database initialization scripts in `infra/init-db/` will run automatically on first start.

### Option 2: Frontend Only (with Mocks)

```bash
cd frontend
npm install
npm run dev
```

## Frontend Routes

The frontend uses React Router for client-side routing (no `/api` prefix):

- `http://localhost:3000/` or `http://localhost:5173/` - Resume list page
- `http://localhost:3000/resume/{id}` or `http://localhost:5173/resume/{id}` - Resume detail page with chat and evaluations

## API Endpoints

All endpoints are documented in `openapi.yaml`. Backend API endpoints use `/api` prefix:

### Resumes
- `GET /api/resumes/` - List all resumes
- `GET /api/resumes/{id}` - Get a specific resume
- `POST /api/resumes/` - Upload a new resume
- `PUT /api/resumes/{id}` - Update a resume
- `DELETE /api/resumes/{id}` - Delete a resume

### Evaluations
- `GET /api/evaluations/resume/{resume_id}` - Get all evaluations for a resume
- `POST /api/evaluations/` - Create a new evaluation

### Chat
- `GET /api/chat/resume/{resume_id}` - Get chat messages for a resume
- `WS /api/chat/ws/{resume_id}` - WebSocket endpoint for real-time chat

## Development Workflow

1. **Frontend First**: Develop UI/UX with mock data
2. **Define API Contract**: Create/update `openapi.yaml`
3. **Implement Backend**: Build backend to match the spec
4. **Integration**: Connect frontend to real backend
5. **Testing**: Test end-to-end functionality

## Testing

### Backend Tests

#### Unit Tests
```bash
cd backend
uv sync --extra test
uv run pytest tests/unit -v
```

#### Integration Tests
```bash
cd backend
uv run pytest tests/integration -v
```

#### All Tests
```bash
cd backend
uv run pytest tests/ -v
```

#### With Coverage
```bash
cd backend
uv run pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests

#### Run Tests
```bash
cd frontend
npm install
npm test
```

#### Run Tests with UI
```bash
cd frontend
npm run test:ui
```

#### Run Tests with Coverage
```bash
cd frontend
npm run test:coverage
```

#### Watch Mode
```bash
cd frontend
npm test -- --watch
```

## Deployment

The application can be deployed to any platform that supports Docker containers:
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- Render
- Railway

Make sure to:
1. Set proper environment variables
2. Use a production database (PostgreSQL recommended)
3. Configure CORS settings for your domain
4. Set up proper file storage (S3, etc.) for production

## License

MIT
