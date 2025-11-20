# Quickstart Guide: Semantic Manifest Editor

**Feature**: 001-semantic-manifest-editor
**Date**: 2025-11-20
**Audience**: Developers implementing this feature

## Overview

This guide walks through the development workflow for building the Semantic Manifest Editor. It covers environment setup, running the development servers, and testing workflows.

## Prerequisites

- Python 3.12+ installed
- Node.js 18+ and npm installed
- Pants build system (already configured in project)
- Access to `/workspaces/bls_data_catalog/bls_data.duckdb` (existing test database)

## Project Structure Quick Reference

```
bls_data_catalog/
└── semantic_manifest_editor/
    ├── backend/                  # Python/FastAPI backend
    │   ├── api/                  # FastAPI routes and models
    │   ├── services/             # Business logic
    │   ├── config.py             # Configuration
    │   └── tests/                # Backend tests
    │
    └── frontend/                 # React/TypeScript frontend
        ├── src/
        │   ├── components/       # React components
        │   ├── services/         # API client, validation
        │   ├── hooks/            # Custom React hooks
        │   └── types/            # TypeScript types
        └── tests/                # Frontend tests
```

## Phase 1: Backend Setup

### 1. Create Backend Directory Structure

```bash
cd /workspaces/bls_data_catalog

# Create backend structure
mkdir -p bls_data_catalog/semantic_manifest_editor/backend/{api/routes,services,tests/{unit,integration,contract}}

# Create __init__.py files
touch bls_data_catalog/semantic_manifest_editor/backend/__init__.py
touch bls_data_catalog/semantic_manifest_editor/backend/api/__init__.py
touch bls_data_catalog/semantic_manifest_editor/backend/api/routes/__init__.py
touch bls_data_catalog/semantic_manifest_editor/backend/services/__init__.py
touch bls_data_catalog/semantic_manifest_editor/backend/tests/__init__.py
```

### 2. Install Backend Dependencies

Add to `bls_data_catalog/requirements.txt`:
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
duckdb>=0.9.0
python-multipart>=0.0.6
```

Install:
```bash
# Using Pants (if configured)
pants export ::

# Or using pip in virtualenv
source dist/export/python/virtualenvs/bls_data_catalog_env/3.12.12/bin/activate
pip install fastapi uvicorn pydantic duckdb python-multipart
```

### 3. Create Minimal FastAPI Application

Create `bls_data_catalog/semantic_manifest_editor/backend/api/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Semantic Manifest Editor API",
    version="1.0.0",
    description="API for creating and editing MetricFlow semantic_manifest.json files"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "service": "semantic-manifest-editor"}

@app.get("/api/v1/semantic-models")
async def list_semantic_models():
    # Placeholder - will implement full CRUD later
    return []

@app.get("/api/v1/metrics")
async def list_metrics():
    # Placeholder - will implement full CRUD later
    return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### 4. Run Backend Development Server

```bash
cd /workspaces/bls_data_catalog/bls_data_catalog/semantic_manifest_editor/backend

# Run directly with uvicorn
python -m uvicorn api.main:app --reload --port 8000

# Or using python
python api/main.py
```

Verify backend is running:
```bash
curl http://localhost:8000/api/v1/health
# Expected: {"status":"ok","service":"semantic-manifest-editor"}
```

## Phase 2: Frontend Setup

### 1. Initialize Frontend Project

```bash
cd /workspaces/bls_data_catalog/bls_data_catalog/semantic_manifest_editor

# Create React + TypeScript project with Vite
npm create vite@latest frontend -- --template react-ts

cd frontend
```

### 2. Install Frontend Dependencies

```bash
# Core dependencies
npm install

# State management
npm install zustand

# Data grid
npm install @tanstack/react-table

# Form management
npm install react-hook-form

# API client
npm install axios

# Development dependencies
npm install -D @types/node
```

### 3. Configure Vite Proxy

Edit `frontend/vite.config.ts`:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### 4. Create Basic Frontend Structure

```bash
cd /workspaces/bls_data_catalog/bls_data_catalog/semantic_manifest_editor/frontend/src

# Create directory structure
mkdir -p components/{SemanticModelEditor,MetricEditor,ManifestEditor,Validation,common}
mkdir -p services hooks types utils

# Create placeholder files
touch services/api.ts
touch types/manifest.ts
touch hooks/useManifest.ts
```

### 5. Create Minimal API Client

Create `frontend/src/services/api.ts`:
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const semanticModelsApi = {
  list: () => apiClient.get('/semantic-models'),
  get: (id: string) => apiClient.get(`/semantic-models/${id}`),
  create: (data: any) => apiClient.post('/semantic-models', data),
  update: (id: string, data: any) => apiClient.put(`/semantic-models/${id}`, data),
  delete: (id: string) => apiClient.delete(`/semantic-models/${id}`),
};

export const metricsApi = {
  list: () => apiClient.get('/metrics'),
  get: (id: string) => apiClient.get(`/metrics/${id}`),
  create: (data: any) => apiClient.post('/metrics', data),
  update: (id: string, data: any) => apiClient.put(`/metrics/${id}`, data),
  delete: (id: string) => apiClient.delete(`/metrics/${id}`),
};

export const validationApi = {
  validateSchema: (manifest: any) => apiClient.post('/validation/schema', manifest),
  validateDatabase: (modelId: string) =>
    apiClient.post('/validation/database', { semantic_model_id: modelId }),
};

export const manifestApi = {
  import: (manifest: any) => apiClient.post('/manifest/import', manifest),
  export: () => apiClient.get('/manifest/export'),
  save: (name: string, manifest: any) =>
    apiClient.post('/manifest/save', { name, manifest }),
  listVersions: () => apiClient.get('/manifest/versions'),
};
```

### 6. Update App.tsx

Replace `frontend/src/App.tsx`:
```typescript
import { useEffect, useState } from 'react';
import { semanticModelsApi, metricsApi } from './services/api';

function App() {
  const [semanticModels, setSemanticModels] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [modelsRes, metricsRes] = await Promise.all([
          semanticModelsApi.list(),
          metricsApi.list(),
        ]);
        setSemanticModels(modelsRes.data);
        setMetrics(metricsRes.data);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="App">
      <h1>Semantic Manifest Editor</h1>
      <div>
        <h2>Semantic Models: {semanticModels.length}</h2>
        <h2>Metrics: {metrics.length}</h2>
      </div>
    </div>
  );
}

export default App;
```

### 7. Run Frontend Development Server

```bash
cd /workspaces/bls_data_catalog/bls_data_catalog/semantic_manifest_editor/frontend

npm run dev
```

Frontend should be available at: http://localhost:5173

## Phase 3: Integration Testing

### 1. Test Backend API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# List semantic models (empty initially)
curl http://localhost:8000/api/v1/semantic-models

# List metrics (empty initially)
curl http://localhost:8000/api/v1/metrics
```

### 2. Test Frontend-Backend Integration

1. Open browser to http://localhost:5173
2. Open browser DevTools console
3. Check for API requests to `/api/v1/semantic-models` and `/api/v1/metrics`
4. Verify "Semantic Models: 0" and "Metrics: 0" displayed

## Phase 4: Development Workflow

### Backend Development

1. **Add Pydantic Models** (`backend/api/models.py`):
   - Define request/response models matching OpenAPI spec
   - Use Pydantic v2 for validation

2. **Implement Services** (`backend/services/`):
   - `manifest_builder.py`: Build semantic_manifest.json from individual models
   - `validator.py`: JSON schema and business logic validation
   - `db_validator.py`: Database schema validation using DuckDB

3. **Create Routes** (`backend/api/routes/`):
   - Implement CRUD endpoints for semantic models
   - Implement CRUD endpoints for metrics
   - Implement validation endpoints
   - Implement manifest import/export

4. **Write Tests**:
   - Unit tests for services (`tests/unit/`)
   - Integration tests for routes (`tests/integration/`)
   - Contract tests for API (`tests/contract/`)

### Frontend Development

1. **Create TypeScript Types** (`src/types/manifest.ts`):
   - Mirror backend Pydantic models
   - Include editor-specific metadata

2. **Build Components**:
   - Start with `SemanticModelEditor` (P1 user story)
   - Add `EntitiesGrid`, `DimensionsGrid`, `MeasuresGrid`
   - Build `MetricEditor` for simple/ratio/derived metrics
   - Create `ValidationPanel` and `JSONViewer`

3. **Implement State Management**:
   - Create Zustand store for manifest state
   - Add undo/redo functionality
   - Implement auto-save to LocalStorage

4. **Write Tests**:
   - Component tests with React Testing Library
   - Integration tests for user flows
   - API client tests with mocked responses

## Phase 5: Testing Workflow

### Backend Tests

```bash
cd /workspaces/bls_data_catalog

# Run all backend tests
pants test bls_data_catalog/semantic_manifest_editor/backend/tests::

# Run specific test file
pants test bls_data_catalog/semantic_manifest_editor/backend/tests/unit/test_validator.py

# Run with coverage
pants test --coverage bls_data_catalog/semantic_manifest_editor/backend/tests::
```

### Frontend Tests

```bash
cd /workspaces/bls_data_catalog/bls_data_catalog/semantic_manifest_editor/frontend

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run tests in watch mode
npm test -- --watch
```

### Manual Testing Checklist

**P1 - Create Semantic Model**:
- [ ] Create new semantic model with name, node relation
- [ ] Add at least one entity (primary type)
- [ ] Add dimensions (time and categorical)
- [ ] Add measures with aggregation types
- [ ] View generated JSON structure
- [ ] Export semantic_manifest.json file

**P2 - Validation**:
- [ ] Client-side validation shows errors immediately
- [ ] Server-side validation returns structured errors
- [ ] Database validation checks table/column existence
- [ ] Validation panel displays all errors with locations

**P2 - Metrics**:
- [ ] Create simple metric from a measure
- [ ] Create ratio metric with numerator/denominator
- [ ] Create derived metric with custom expression
- [ ] Edit metric properties

**P3 - Import**:
- [ ] Upload existing semantic_manifest.json
- [ ] All models and metrics load correctly
- [ ] Can edit imported manifest

## Common Development Tasks

### Adding a New API Endpoint

1. Define Pydantic model in `backend/api/models.py`
2. Implement service logic in `backend/services/`
3. Create route in `backend/api/routes/`
4. Add route to FastAPI app in `backend/api/main.py`
5. Write tests in `backend/tests/`
6. Update OpenAPI spec in `specs/001-semantic-manifest-editor/contracts/api.openapi.yaml`

### Adding a New React Component

1. Create component file in `frontend/src/components/`
2. Define TypeScript types/props
3. Implement component logic
4. Write tests in `frontend/tests/components/`
5. Import and use in parent component

### Database Validation Development

```python
# Example: backend/services/db_validator.py
import duckdb

class DatabaseValidator:
    def __init__(self, db_path: str):
        self.conn = duckdb.connect(db_path, read_only=True)

    def validate_table_exists(self, schema: str, table: str) -> bool:
        result = self.conn.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ? AND table_name = ?",
            [schema, table]
        ).fetchone()
        return result[0] > 0

    def validate_column_exists(self, schema: str, table: str, column: str) -> bool:
        result = self.conn.execute(
            "SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = ? AND table_name = ? AND column_name = ?",
            [schema, table, column]
        ).fetchone()
        return result[0] > 0
```

## Debugging Tips

### Backend Debugging

```bash
# Enable FastAPI debug logging
export LOG_LEVEL=DEBUG

# Run with debugger
python -m debugpy --listen 5678 --wait-for-client -m uvicorn api.main:app --reload
```

### Frontend Debugging

- Use React DevTools browser extension
- Check Network tab for API requests
- Use Redux DevTools for Zustand (with middleware)
- Add `console.log` in useEffect hooks to trace state changes

### Database Queries

```bash
# Connect to DuckDB directly
duckdb /workspaces/bls_data_catalog/bls_data.duckdb

# Check available tables
SHOW TABLES;

# View table schema
DESCRIBE stg_us_employment;

# Test validation query
SELECT * FROM information_schema.columns WHERE table_name = 'stg_us_employment';
```

## Next Steps

After completing the quickstart:

1. Review `data-model.md` for complete entity definitions
2. Review `contracts/api.openapi.yaml` for full API specification
3. Implement P1 user stories first (create semantic models)
4. Add validation (P2) alongside P1
5. Implement metrics (P2) after models are stable
6. Add import/export functionality (P3)

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **TanStack Table**: https://tanstack.com/table/latest
- **Zustand**: https://github.com/pmndrs/zustand
- **MetricFlow**: https://docs.getdbt.com/docs/build/metricflow
- **DuckDB**: https://duckdb.org/docs/

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (needs 3.12+)
- Verify dependencies: `pip list | grep fastapi`
- Check port 8000 not in use: `lsof -i :8000`

### Frontend won't start
- Check Node version: `node --version` (needs 18+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check port 5173 not in use: `lsof -i :5173`

### CORS errors
- Verify backend CORS middleware includes frontend origin (http://localhost:5173)
- Check Vite proxy configuration points to correct backend port
- Try hard refresh in browser (Ctrl+Shift+R)

### Database validation fails
- Check DuckDB file exists: `ls -lh /workspaces/bls_data_catalog/bls_data.duckdb`
- Verify read permissions
- Test connection: `duckdb /workspaces/bls_data_catalog/bls_data.duckdb "SELECT 1"`
