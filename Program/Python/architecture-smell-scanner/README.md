# Architecture Smell Scanner

A comprehensive web application for analyzing codebases to identify and track architecture issues.

## Features

- **Multi-Language Support**: Analyze Python, Java, JavaScript, and TypeScript codebases
- **Architecture Smell Detection**: 
  - Circular Dependencies
  - God Class/Module Detection
  - Feature Envy
  - Shotgun Surgery
  - Duplicate Code
- **Health Score Tracking**: 0-100 health score with trend visualization
- **Team Collaboration**: Add collaborators to share project insights
- **Report Export**: PDF reports and CSV trend data export

## Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL
- Redis (for async task queue)
- Celery (background worker)

### Frontend
- React 18 + TypeScript
- Zustand (state management)
- Tailwind CSS
- ECharts (visualization)
- React Router v6

## Quick Start

### Using Docker Compose

```bash
cd docker
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1

### Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Architecture Smells Detected

| Smell Type | Severity | Description |
|------------|----------|-------------|
| CircularDependency | Critical | Module A imports B, B imports A |
| GodClass | High | Class > 500 lines or > 30 methods |
| FeatureEnvy | Medium | Class more interested in another class's data |
| ShotgunSurgery | Medium | One change requires multiple modifications |
| DuplicateCode | Low | Code blocks with > 80% similarity |

## Health Score Calculation

- Start: 100 points
- Critical: -15 points each
- High: -8 points each
- Medium: -3 points each
- Low: -1 point each

Minimum score: 0

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Projects
- `GET /api/v1/projects/` - List user's projects
- `POST /api/v1/projects/` - Create new project
- `GET /api/v1/projects/{id}` - Get project details
- `PATCH /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project
- `POST /api/v1/projects/{id}/upload` - Upload code snapshot
- `POST /api/v1/projects/{id}/collaborators` - Add collaborator
- `GET /api/v1/projects/{id}/collaborators` - List collaborators

### Scans
- `POST /api/v1/scans/` - Start a new scan
- `GET /api/v1/scans/{id}` - Get scan details with smells
- `GET /api/v1/scans/project/{id}` - List project's scans
- `GET /api/v1/scans/project/{id}/trends` - Get health trend data
- `GET /api/v1/scans/{id}/smells` - Get smells with filters

## License

MIT