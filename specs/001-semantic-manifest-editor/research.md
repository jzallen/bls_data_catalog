# Research & Technology Decisions: Semantic Manifest Editor

**Feature**: 001-semantic-manifest-editor
**Date**: 2025-11-20
**Phase**: 0 - Research & Outline

## Overview

This document captures technology decisions, best practices research, and alternatives considered for the Semantic Manifest Editor implementation.

## Frontend Framework & Tooling

### Decision: React + TypeScript + Vite

**Rationale**:
- **React**: User explicitly requested React in the original feature description. React excels at managing complex nested state (semantic manifest structure) and has mature ecosystem for data-heavy applications
- **TypeScript**: Type safety for complex manifest structure, better IDE support, catches errors at compile time
- **Vite**: Fast development builds, modern ESM-based tooling, simpler configuration than Webpack

**Alternatives Considered**:
- **Vue.js**: Simpler learning curve but less ecosystem support for data grid components
- **Angular**: Too heavyweight for this use case, steeper learning curve
- **Svelte**: Good performance but smaller ecosystem and less community support for complex data editing

### Decision: State Management - Zustand

**Rationale**:
- Lightweight compared to Redux (no boilerplate)
- Simple API for managing manifest state
- Built-in middleware for persistence (LocalStorage)
- Good TypeScript support
- Suitable for moderate complexity (not over-engineered for this use case)

**Alternatives Considered**:
- **Redux Toolkit**: More powerful but adds complexity and boilerplate unnecessary for single-user editing
- **Context API**: Would require multiple contexts, prop drilling, and manual optimization
- **Jotai/Recoil**: Atomic state management good for small pieces, less intuitive for large interconnected objects like manifests

### Decision: Data Grid - TanStack Table v8

**Rationale**:
- Headless UI - full control over styling and behavior
- Excellent TypeScript support
- Handles inline editing, sorting, filtering out of the box
- Lightweight compared to AG Grid
- Active maintenance and good documentation
- Free and open source

**Alternatives Considered**:
- **AG Grid**: Very feature-rich but heavy bundle size, commercial license for some features
- **react-data-grid**: Good but less flexible, smaller community
- **Material-UI DataGrid**: Tied to Material-UI design system, less customizable

### Decision: Form Management - React Hook Form

**Rationale**:
- Minimal re-renders (better performance for large forms)
- Built-in validation support
- Simple API for nested fields (needed for semantic models)
- Small bundle size
- Excellent TypeScript support

**Alternatives Considered**:
- **Formik**: More popular but slower performance, more re-renders
- **Manual state management**: Too much boilerplate, error-prone
- **Controlled components**: Performance issues with large forms

### Decision: Build Tool - Vite

**Rationale**:
- Fast HMR (Hot Module Replacement) during development
- ESM-based for modern browsers
- Simple configuration
- Built-in TypeScript support
- Growing ecosystem and adoption

**Alternatives Considered**:
- **Create React App**: Slower build times, uses Webpack, less flexible
- **Next.js**: SSR features unnecessary, adds complexity
- **Webpack**: More configuration required, slower dev builds

## Backend Framework & Libraries

### Decision: FastAPI

**Rationale**:
- Modern async Python framework
- Automatic OpenAPI/Swagger documentation
- Excellent Pydantic integration for data validation
- Fast performance (ASGI-based)
- Type hints enable better IDE support and validation
- Easy testing with TestClient

**Alternatives Considered**:
- **Flask**: Synchronous, less built-in validation, more boilerplate
- **Django**: Too heavyweight, includes ORM and admin UI we don't need
- **Django REST Framework**: Good but Django overhead unnecessary

### Decision: Validation - Pydantic v2

**Rationale**:
- Built-in to FastAPI
- Excellent for JSON schema validation
- Type-safe data models
- Can generate JSON schemas for frontend
- Version 2 has significant performance improvements

**Alternatives Considered**:
- **Marshmallow**: Good but not as integrated with FastAPI
- **JSON Schema + jsonschema library**: More manual work, less type safety
- **Cerberus**: Less actively maintained, not as powerful

### Decision: Database Client - DuckDB Python

**Rationale**:
- Native Python support
- Fast analytical queries for schema validation
- File-based (matches MVP requirement)
- SQL standard compliance
- Can query CSV/Parquet directly if needed

**Alternatives Considered**:
- **SQLite**: Less optimized for analytical queries
- **PostgreSQL**: Would require running database server, overkill for validation
- **Direct SQL parsing**: Complex, error-prone, reinventing the wheel

### Decision: Testing - pytest + pytest-asyncio

**Rationale**:
- Standard Python testing framework
- Good FastAPI integration via TestClient
- Fixtures for setup/teardown
- Async support via pytest-asyncio
- Parametrized tests for validation scenarios

**Alternatives Considered**:
- **unittest**: More verbose, less flexible
- **nose**: Deprecated, unmaintained
- **pytest-bdd**: BDD not needed for this use case

## API Design Patterns

### Decision: RESTful API

**Rationale**:
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Stateless (matches single-user editing requirement)
- Easy to test and debug
- Good tooling support (OpenAPI, Swagger)
- Simple for frontend consumption

**Alternatives Considered**:
- **GraphQL**: Overkill for simple CRUD operations, adds complexity
- **gRPC**: Binary protocol, harder to debug, unnecessary performance optimization
- **WebSockets**: Not needed for single-user editing, adds complexity

### Decision: API Structure - Resource-based

**Rationale**:
- Logical grouping by entity type (semantic_models, metrics, validation)
- Clear endpoint hierarchy
- Matches semantic manifest structure
- Easy to understand and document

**Endpoint Structure**:
```
POST   /api/v1/semantic-models          # Create semantic model
GET    /api/v1/semantic-models/:id       # Get semantic model
PUT    /api/v1/semantic-models/:id       # Update semantic model
DELETE /api/v1/semantic-models/:id       # Delete semantic model
POST   /api/v1/semantic-models/:id/entities
POST   /api/v1/semantic-models/:id/dimensions
POST   /api/v1/semantic-models/:id/measures

POST   /api/v1/metrics                   # Create metric
GET    /api/v1/metrics/:id               # Get metric
PUT    /api/v1/metrics/:id               # Update metric
DELETE /api/v1/metrics/:id               # Delete metric

POST   /api/v1/validation/schema         # Validate manifest structure
POST   /api/v1/validation/database       # Validate against database

POST   /api/v1/manifest/import           # Import semantic_manifest.json
GET    /api/v1/manifest/export           # Export semantic_manifest.json
POST   /api/v1/manifest/save             # Save work in progress
GET    /api/v1/manifest/versions         # List saved versions
```

**Alternatives Considered**:
- **Action-based URLs** (/api/v1/validate-schema): Less RESTful, harder to reason about
- **Flat structure** (/api/v1/entities): Loses relationship context
- **GraphQL mutations**: Overkill, adds complexity

## Validation Strategy

### Decision: Two-tier Validation

**Tier 1 - Client-side (Immediate)**:
- Field-level validation (required fields, data types)
- Name uniqueness within semantic model
- Basic expression syntax checking
- Implemented in TypeScript using Zod or custom validators

**Tier 2 - Server-side (On-demand)**:
- Full JSON schema validation
- Cross-model validation (metric references valid measures)
- Circular dependency detection
- Database schema validation (table/column existence)
- Implemented in Python using Pydantic + custom validators

**Rationale**:
- Client-side provides immediate feedback (<500ms)
- Server-side ensures data integrity and database correctness
- Separates concerns: UI responsiveness vs. data correctness
- Reduces server load (only validate when user requests)

**Alternatives Considered**:
- **Client-only validation**: Can't validate against database, less secure
- **Server-only validation**: Too slow, poor UX
- **Real-time server validation**: Too many API calls, performance issues

## Data Persistence Strategy

### Decision: LocalStorage + File Export (MVP)

**MVP Approach**:
- **Auto-save**: LocalStorage every 30 seconds
- **Manual save**: User-triggered save creates timestamped version
- **Export**: Download semantic_manifest.json file
- **Import**: Upload semantic_manifest.json file

**Rationale**:
- Simple implementation, no database required
- Works offline (good for local development)
- LocalStorage limit (5-10MB) sufficient for typical manifests
- Aligns with MVP scope (single-user editing)

**Future Enhancement**:
- Backend database (PostgreSQL/DynamoDB) for multi-user support
- Version control integration (Git)
- Cloud storage sync

**Alternatives Considered**:
- **IndexedDB**: More complex API, unnecessary for JSON storage
- **Backend-only storage**: Requires server for every edit, slower UX
- **File system API**: Limited browser support, security concerns

## MetricFlow Schema Integration

### Decision: Hardcoded Schema Definition + Version Detection

**Rationale**:
- Parse existing semantic_manifest.json to extract schema structure
- Hardcode MetricFlow schema as TypeScript types and Pydantic models
- Include version detection to handle schema evolution
- Document schema version compatibility

**Implementation**:
- Extract types from `/bls_data_catalog/target/semantic_manifest.json`
- Create TypeScript types in `frontend/src/types/manifest.ts`
- Create Pydantic models in `backend/api/models.py`
- Version check on import/export

**Alternatives Considered**:
- **Dynamic schema generation**: Complex, error-prone, unnecessary
- **MetricFlow API integration**: Adds external dependency, may not exist
- **Manual YAML parsing**: Bypasses MetricFlow entirely, different from spec

## Error Handling & User Feedback

### Decision: Structured Error Messages + Error Boundary

**Frontend**:
- Error boundary for React component errors
- Toast notifications for transient errors
- Inline validation errors with suggestions
- Validation panel for aggregate error view

**Backend**:
- HTTP status codes (400 for validation, 500 for server errors)
- Structured error response format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "location": "semantic_models[0].measures[2].agg",
        "message": "Missing required field: agg",
        "suggestion": "Valid aggregation types: sum, average, count, min, max"
      }
    ]
  }
}
```

**Rationale**:
- Clear error messages improve UX (SC-008: 90% can fix without docs)
- Location path helps users find the issue
- Suggestions guide users to correct solution
- Structured format easy to parse and display

**Alternatives Considered**:
- **Simple error strings**: Less helpful, harder to locate issues
- **Error codes only**: Requires documentation lookup
- **No suggestions**: Users have to guess correct values

## Performance Optimization

### Decision: Debouncing + Memoization + Lazy Loading

**Frontend Optimizations**:
- **Debounce validation**: 300ms delay before client-side validation
- **Throttle API calls**: Max 1 database validation per 3 seconds
- **Memoization**: React.memo for grid rows, useMemo for expensive calculations
- **Lazy loading**: Code split by route, load grids on demand
- **Virtualization**: Virtual scrolling for large lists (50+ models)

**Backend Optimizations**:
- **Connection pooling**: Reuse DuckDB connections
- **Caching**: Cache database schema for 5 minutes
- **Batch validation**: Validate multiple items in single request
- **Async processing**: Use FastAPI async for I/O operations

**Rationale**:
- Meets performance goals (SC-003: <500ms validation, SC-009: <3s DB validation)
- Prevents unnecessary API calls
- Handles large manifests (SC-007: 50 models, 200 metrics)

**Alternatives Considered**:
- **No optimization**: Would fail performance requirements
- **Web Workers**: Complex for minimal benefit in this use case
- **Server-side caching only**: Frontend still slow without client optimization

## Development Environment

### Decision: Vite Dev Server + FastAPI Uvicorn

**Setup**:
- **Frontend**: `npm run dev` starts Vite on port 5173
- **Backend**: `uvicorn main:app --reload` on port 8000
- **Proxy**: Vite proxies `/api` requests to FastAPI
- **CORS**: FastAPI CORS middleware for development

**Rationale**:
- Fast development reload (Vite HMR, Uvicorn reload)
- Simple setup, minimal configuration
- Matches production deployment pattern

**Alternatives Considered**:
- **Monorepo tools** (Nx, Turborepo): Overkill for two projects
- **Docker Compose**: Good for production, slower dev experience
- **Separate ports without proxy**: Requires CORS, more configuration

## Testing Strategy

### Decision: Unit + Integration + Contract Tests

**Frontend Tests**:
- **Unit**: Component tests with React Testing Library
- **Integration**: User flow tests (create model → add dimension → export)
- **Contract**: API client tests with mocked responses

**Backend Tests**:
- **Unit**: Service layer tests (validator, manifest_builder)
- **Integration**: API endpoint tests with TestClient
- **Contract**: OpenAPI schema validation

**Test Coverage Goals**:
- Backend: >80% coverage for services and validators
- Frontend: >70% coverage for components and hooks
- 100% coverage for validation logic (critical path)

**Rationale**:
- Confidence in refactoring
- Catch regressions early
- Contract tests ensure frontend/backend compatibility

**Alternatives Considered**:
- **E2E only** (Playwright, Cypress): Slow, brittle, hard to debug
- **Unit tests only**: Miss integration issues
- **No tests**: High risk of bugs, hard to refactor

## Deployment Considerations (Future)

### Research: Container-based Deployment

**Likely Approach**:
- **Frontend**: Static build served by nginx or CDN
- **Backend**: FastAPI in Docker container
- **DuckDB**: Mount as volume or persistent storage

**Not implementing in MVP** but researched for future:
- Kubernetes for scaling
- CI/CD pipeline (GitHub Actions)
- Monitoring and logging (Prometheus, Grafana)

## Summary of Key Decisions

| Category | Decision | Rationale |
|----------|----------|-----------|
| Frontend Framework | React + TypeScript + Vite | User requirement, strong ecosystem, fast builds |
| State Management | Zustand | Lightweight, simple API, good for moderate complexity |
| Data Grid | TanStack Table v8 | Headless, flexible, excellent TypeScript support |
| Backend Framework | FastAPI | Modern, fast, automatic docs, Pydantic integration |
| Database | DuckDB Python | File-based, fast analytical queries, matches MVP |
| Validation | Two-tier (client + server) | Balance speed and correctness |
| API Design | RESTful, resource-based | Standard, simple, well-documented |
| Persistence | LocalStorage + file export | MVP simplicity, no server required |
| Testing | pytest (backend), RTL (frontend) | Standard tools, good support |

All decisions prioritize:
1. **MVP simplicity** (single-user, no auth, local data)
2. **Performance** (meet SC-003, SC-009 criteria)
3. **User experience** (SC-001, SC-002, SC-008 criteria)
4. **Future extensibility** (clear paths to multi-user, cloud storage, auth)
