# Implementation Plan: Semantic Manifest Editor

**Branch**: `001-semantic-manifest-editor` | **Date**: 2025-11-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-semantic-manifest-editor/spec.md`

## Summary

Build a web-based editor for creating and editing MetricFlow semantic_manifest.json files without requiring dbt builds. The editor provides an interactive interface for defining semantic models (entities, dimensions, measures) and metrics (simple, ratio, derived) with real-time validation. Backend API validates expressions against actual database schemas using managed credentials.

**Primary Value**: Enables data analysts to create and maintain semantic layers through a user-friendly web interface instead of manually editing YAML files and running dbt commands.

## Technical Context

**Language/Version**: Python 3.12 (backend), JavaScript/TypeScript (frontend - framework TBD in research)
**Primary Dependencies**:
- Backend: FastAPI, DuckDB Python connector, MetricFlow schema validator
- Frontend: React (per user input), state management library TBD, data grid library TBD

**Storage**:
- DuckDB file for validation queries (hardcoded path for MVP)
- Browser LocalStorage for auto-save/work-in-progress (5-10MB limit)
- File system for manifest persistence (future: database backend)

**Testing**:
- Backend: pytest with FastAPI TestClient
- Frontend: Testing framework TBD (React Testing Library or Jest)
- Contract tests between frontend and API

**Target Platform**:
- Frontend: Modern web browsers (Chrome, Firefox, Safari, Edge) - desktop/laptop 1280x720+
- Backend: Linux server (containerized deployment TBD)

**Project Type**: Web application (separate frontend and backend)

**Performance Goals**:
- Frontend rendering: 60 FPS for UI interactions
- Validation feedback: <500ms latency
- Database validation: <3 seconds for 20 dimensions/measures
- Import processing: <30 seconds for manifests with 10 semantic models
- Support 50 semantic models and 200 metrics without degradation

**Constraints**:
- Exported JSON must exactly match MetricFlow semantic_manifest.json schema
- Backend manages database credentials (not exposed to frontend)
- MVP uses hardcoded DuckDB connection string
- Browser LocalStorage limited to 5-10MB for auto-save
- No authentication/authorization in MVP
- Single-user editing (no real-time collaboration)

**Scale/Scope**:
- Target users: Data analysts, analytics engineers (< 100 concurrent users for MVP)
- Typical manifest: 5-20 semantic models, 10-50 metrics
- Large manifest support: Up to 50 semantic models, 200 metrics

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: Project constitution is currently a template placeholder. Using standard web application best practices:

### Standard Web Application Gates

- **Separation of Concerns**: ✅ PASS
  - Frontend handles UI and client-side state management
  - Backend handles validation, database access, and credential management
  - Clear API contract between layers

- **Testability**: ✅ PASS
  - Backend API endpoints independently testable via FastAPI TestClient
  - Frontend components testable in isolation
  - Contract tests validate API integration
  - Database validation testable against sample DuckDB file

- **Data Integrity**: ✅ PASS
  - JSON schema validation for semantic_manifest structure
  - Uniqueness constraints for names (models, metrics, entities, dimensions, measures)
  - Referential integrity checks (metrics reference valid measures)
  - Circular dependency detection for derived metrics

- **Security**: ⚠️ DEFERRED (MVP Scope)
  - No authentication/authorization in MVP (documented scope constraint)
  - Database credentials managed by backend (not exposed to frontend)
  - Input validation for user-supplied expressions
  - Future: Add user authentication, role-based access, audit logging

- **Performance**: ✅ PASS
  - Client-side validation for immediate feedback
  - Debounced/throttled API calls for database validation
  - Efficient state management for large manifests
  - LocalStorage for auto-save without server round trips

## Project Structure

### Documentation (this feature)

```text
specs/001-semantic-manifest-editor/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── api.openapi.yaml # REST API contract
│   └── manifest.schema.json # Semantic manifest JSON schema
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend)
bls_data_catalog/
├── semantic_manifest_editor/    # New feature directory
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── main.py          # FastAPI application entry
│   │   │   ├── models.py        # Pydantic models for API
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── semantic_models.py
│   │   │   │   ├── metrics.py
│   │   │   │   ├── validation.py
│   │   │   │   └── manifest.py  # Import/export endpoints
│   │   │   └── dependencies.py  # Shared dependencies
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── manifest_builder.py   # Construct semantic_manifest.json
│   │   │   ├── validator.py          # JSON schema + business logic validation
│   │   │   ├── db_validator.py       # Database schema validation via DuckDB
│   │   │   └── schema_loader.py      # Load MetricFlow schema definitions
│   │   ├── config.py            # Configuration (database connection, etc.)
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── conftest.py
│   │       ├── contract/
│   │       │   └── test_api_contract.py
│   │       ├── integration/
│   │       │   ├── test_manifest_builder.py
│   │       │   └── test_db_validator.py
│   │       └── unit/
│   │           ├── test_routes.py
│   │           ├── test_validator.py
│   │           └── test_models.py
│   │
│   └── frontend/
│       ├── package.json
│       ├── tsconfig.json
│       ├── vite.config.ts       # or webpack/similar
│       ├── public/
│       ├── src/
│       │   ├── main.tsx         # Application entry
│       │   ├── App.tsx
│       │   ├── components/
│       │   │   ├── SemanticModelEditor/
│       │   │   │   ├── SemanticModelEditor.tsx
│       │   │   │   ├── EntitiesGrid.tsx
│       │   │   │   ├── DimensionsGrid.tsx
│       │   │   │   └── MeasuresGrid.tsx
│       │   │   ├── MetricEditor/
│       │   │   │   ├── MetricEditor.tsx
│       │   │   │   ├── SimpleMetricForm.tsx
│       │   │   │   ├── RatioMetricForm.tsx
│       │   │   │   └── DerivedMetricForm.tsx
│       │   │   ├── ManifestEditor/
│       │   │   │   ├── ManifestEditor.tsx
│       │   │   │   ├── ModelsList.tsx
│       │   │   │   ├── MetricsList.tsx
│       │   │   │   └── JSONViewer.tsx
│       │   │   ├── Validation/
│       │   │   │   ├── ValidationPanel.tsx
│       │   │   │   └── ErrorDisplay.tsx
│       │   │   └── common/
│       │   │       ├── DataGrid.tsx
│       │   │       ├── Button.tsx
│       │   │       └── Select.tsx
│       │   ├── services/
│       │   │   ├── api.ts           # API client
│       │   │   ├── validation.ts    # Client-side validation
│       │   │   └── storage.ts       # LocalStorage helpers
│       │   ├── hooks/
│       │   │   ├── useManifest.ts   # Manifest state management
│       │   │   ├── useValidation.ts
│       │   │   └── useAutoSave.ts
│       │   ├── types/
│       │   │   └── manifest.ts      # TypeScript types for manifest
│       │   └── utils/
│       │       ├── manifestBuilder.ts
│       │       └── validators.ts
│       └── tests/
│           ├── components/
│           ├── services/
│           └── integration/

# Shared/existing structure
bls_data_catalog/
├── bls_data.duckdb              # Existing - used for validation
├── scripts/                     # Existing scripts
├── tests/                       # Existing tests
└── ...                          # Other existing project files
```

**Structure Decision**: Web application with separate frontend and backend directories. The feature is self-contained within `semantic_manifest_editor/` to avoid mixing with existing dbt/MetricFlow project structure. Frontend uses modern build tooling (Vite or similar) for React development. Backend uses FastAPI following existing Python project patterns (Pants build system).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

No constitution violations. Standard web application architecture with clear separation of concerns.

