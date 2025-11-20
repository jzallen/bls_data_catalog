# Semantic Manifest Editor - MVP

Web-based editor for creating and editing MetricFlow `semantic_manifest.json` files.

## Status: MVP In Progress

**Current Progress:**
- ✅ Phase 1: Setup (9/9 tasks)
- ✅ Phase 2: Foundational Infrastructure (11/11 tasks)
- ✅ Phase 3: Backend CRUD APIs (15/15 tasks)
- 🔄 Phase 3: Frontend UI (10/15 tasks)
- ⏳ Phase 6: Basic Export (0/6 tasks)
- ⏳ MVP Validation

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- DuckDB database at `/workspaces/bls_data_catalog/bls_data.duckdb`

### Backend Setup

```bash
cd semantic_manifest_editor/backend

# Install dependencies (using project virtualenv)
source /workspaces/bls_data_catalog/dist/export/python/virtualenvs/bls_data_catalog_env/3.12.12/bin/activate
pip install -r requirements.txt

# Run backend server
python -m uvicorn api.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Frontend Setup

```bash
cd semantic_manifest_editor/frontend

# Install dependencies
npm install

# Run frontend dev server
npm run dev
```

Frontend will be available at: http://localhost:5173

## Architecture

### Backend (FastAPI + Python)
- **API Routes**: RESTful endpoints for semantic models
- **Models**: Pydantic models matching MetricFlow schema
- **Validation**: Server-side validation with descriptive errors
- **Storage**: In-memory for MVP (will add database later)

### Frontend (React + TypeScript + Vite)
- **State Management**: Zustand for manifest state
- **API Client**: Axios for backend communication
- **Validation**: Client-side validation for immediate feedback
- **Storage**: LocalStorage for auto-save

## MVP Features

### ✅ Completed
1. Project structure and configuration
2. Backend API with semantic model CRUD
3. TypeScript types matching backend models
4. Basic React UI with state management
5. Validation infrastructure (client + server)

### 🔄 In Progress
6. Semantic model editor UI components
7. Entity/Dimension/Measure grid editors

### ⏳ Planned (MVP)
8. Export manifest as JSON
9. Validate against database schema

## API Endpoints

### Semantic Models
- `POST /api/semantic-models` - Create semantic model
- `GET /api/semantic-models` - List all models
- `GET /api/semantic-models/{id}` - Get specific model
- `PUT /api/semantic-models/{id}` - Update model
- `DELETE /api/semantic-models/{id}` - Delete model

### Entities/Dimensions/Measures
- `POST /api/semantic-models/{id}/entities` - Add entity
- `POST /api/semantic-models/{id}/dimensions` - Add dimension
- `POST /api/semantic-models/{id}/measures` - Add measure

### Health
- `GET /api/health` - Health check

## Development

### Backend Development

```bash
# Run with auto-reload
python api/main.py

# Or using uvicorn directly
uvicorn api.main:app --reload --port 8000
```

### Frontend Development

```bash
# Development server with hot reload
npm run dev

# Type checking
npm run type-check

# Build for production
npm run build
```

## Project Structure

```
semantic_manifest_editor/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── models.py            # Pydantic models
│   │   └── routes/
│   │       └── semantic_models.py   # CRUD endpoints
│   ├── services/
│   │   └── validator.py         # Validation logic
│   ├── config.py                # DuckDB configuration
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── App.tsx              # Main app component
    │   ├── main.tsx             # Entry point
    │   ├── types/
    │   │   └── manifest.ts      # TypeScript types
    │   ├── services/
    │   │   ├── api.ts           # API client
    │   │   └── storage.ts       # LocalStorage service
    │   ├── hooks/
    │   │   └── useManifest.ts   # Zustand store
    │   └── utils/
    │       └── validators.ts    # Client-side validation
    ├── package.json
    ├── vite.config.ts
    └── tsconfig.json
```

## Testing MVP

1. Start backend: `python api/main.py`
2. Start frontend: `npm run dev`
3. Open http://localhost:5173
4. API health check: http://localhost:8000/api/health

## Next Steps (Post-MVP)

- Add metrics creation (User Story 2)
- Add validation panel (User Story 4)
- Add import functionality (User Story 3)
- Add versioning and save/load
- Performance optimization
- Add tests

## References

- [MetricFlow Documentation](https://docs.getdbt.com/docs/build/about-metricflow)
- [Semantic Models](https://docs.getdbt.com/docs/build/semantic-models)
- Feature spec: `/specs/001-semantic-manifest-editor/spec.md`
- Implementation plan: `/specs/001-semantic-manifest-editor/plan.md`
