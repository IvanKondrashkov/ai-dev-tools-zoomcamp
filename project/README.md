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

The frontend connects to the backend API. Make sure the backend is running before starting the frontend.

4. Open http://localhost:5173 in your browser

**Note:** The frontend requires the backend to be running. Make sure the backend is started before accessing the frontend.

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

### Running Frontend

The frontend connects to the backend API. Make sure the backend is running before starting the frontend.

**Optional: Create `frontend/.env` to customize API URLs:**
```env
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=localhost:8000
```

**Note:** If backend is not running, API calls will fail. Make sure backend is running on port 8000.

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

## API Endpoints

All endpoints are documented in `openapi.yaml`. Backend API endpoints use `/api` prefix:

### Resumes
- `GET /api/resumes/` - List all resumes
- `GET /api/resumes/{resume_id}` - Get a specific resume
- `POST /api/resumes/` - Upload a new resume
- `PUT /api/resumes/{resume_id}` - Update a resume
- `DELETE /api/resumes/{resume_id}` - Delete a resume

### Evaluations
- `GET /api/evaluations/resume/{resume_id}` - Get all evaluations for a resume
- `GET /api/evaluations/{evaluation_id}` - Get a specific evaluation by ID
- `POST /api/evaluations/` - Create a new evaluation

### Chat
- `GET /api/chat/resume/{resume_id}` - Get chat messages for a resume
- `WS /api/chat/ws/{resume_id}` - WebSocket endpoint for real-time chat

## Deployment to Render

The project includes configuration for deploying to Render.com:

### Files for Render Deployment

- `render.yaml` - Render service configuration
- `infra/Dockerfile.backend` - Backend Dockerfile for Render
- `infra/Dockerfile.frontend` - Frontend Dockerfile for Render
- `.dockerignore` - Files to exclude from Docker builds

### Deploy Steps

1. Push your code to GitHub
2. Connect your repository to Render
3. Render will automatically detect `render.yaml` and create services
4. Services will be deployed:
   - `resume-review-db` - PostgreSQL database
   - `resume-review-backend` - Backend API service
   - `resume-review-frontend` - Frontend web service

### Environment Variables

Backend automatically uses:
- `DATABASE_URL` - From Render database connection
- `CORS_ORIGINS` - Set to frontend URL
- `PORT` - Set by Render (defaults to 8000)

Frontend automatically uses:
- `VITE_WS_URL` - Backend WebSocket host (for chat)
- `VITE_API_URL` - Not set by default (uses relative paths `/api` through Nginx proxy)

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
