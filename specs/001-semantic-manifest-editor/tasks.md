# Tasks: Semantic Manifest Editor

**Input**: Design documents from `/specs/001-semantic-manifest-editor/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the feature specification, therefore test tasks are excluded. Focus is on implementation and validation through manual testing per acceptance scenarios.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `bls_data_catalog/semantic_manifest_editor/backend/` and `bls_data_catalog/semantic_manifest_editor/frontend/`
- Paths shown below follow plan.md structure for web application

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure: bls_data_catalog/semantic_manifest_editor/backend/{api/routes,services,tests/{unit,integration,contract}}
- [ ] T002 Create frontend directory structure: bls_data_catalog/semantic_manifest_editor/frontend/src/{components,services,hooks,types,utils}
- [ ] T003 [P] Initialize backend with FastAPI dependencies in bls_data_catalog/semantic_manifest_editor/backend/requirements.txt
- [ ] T004 [P] Initialize frontend with Vite+React+TypeScript using npm create vite in bls_data_catalog/semantic_manifest_editor/frontend/
- [ ] T005 [P] Configure Vite proxy for /api requests in bls_data_catalog/semantic_manifest_editor/frontend/vite.config.ts
- [ ] T006 [P] Install Zustand for state management in bls_data_catalog/semantic_manifest_editor/frontend/package.json
- [ ] T007 [P] Install TanStack Table for data grids in bls_data_catalog/semantic_manifest_editor/frontend/package.json
- [ ] T008 [P] Install React Hook Form in bls_data_catalog/semantic_manifest_editor/frontend/package.json
- [ ] T009 [P] Configure CORS middleware in bls_data_catalog/semantic_manifest_editor/backend/api/main.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 Create Pydantic base models for semantic manifest in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T011 Create TypeScript manifest types in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T012 [P] Implement MetricFlow schema loader service in bls_data_catalog/semantic_manifest_editor/backend/services/schema_loader.py
- [ ] T013 [P] Create DuckDB connection configuration in bls_data_catalog/semantic_manifest_editor/backend/config.py
- [ ] T014 [P] Implement base validation service with JSON schema validation in bls_data_catalog/semantic_manifest_editor/backend/services/validator.py
- [ ] T015 [P] Create API client service in bls_data_catalog/semantic_manifest_editor/frontend/src/services/api.ts
- [ ] T016 [P] Implement client-side validation utilities in bls_data_catalog/semantic_manifest_editor/frontend/src/utils/validators.ts
- [ ] T017 Create Zustand store for manifest state in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useManifest.ts
- [ ] T018 [P] Create error response models in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T019 [P] Implement LocalStorage service for auto-save in bls_data_catalog/semantic_manifest_editor/frontend/src/services/storage.ts
- [ ] T020 Create FastAPI app entry point with health check endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create New Semantic Model (Priority: P1) 🎯 MVP

**Goal**: Enable users to create semantic models with entities, dimensions, and measures through spreadsheet-like editing

**Independent Test**: Create a semantic model with 1 entity, 3 dimensions, and 5 measures in under 10 minutes, then export valid semantic_manifest.json that passes MetricFlow CLI validation

### Backend Implementation for US1

- [ ] T021 [P] [US1] Create NodeRelation Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T022 [P] [US1] Create Entity Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T023 [P] [US1] Create Dimension Pydantic model with type_params in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T024 [P] [US1] Create Measure Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T025 [P] [US1] Create SemanticModel Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T026 [US1] Implement POST /semantic-models endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/semantic_models.py
- [ ] T027 [US1] Implement GET /semantic-models endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/semantic_models.py
- [ ] T028 [US1] Implement GET /semantic-models/{modelId} endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/semantic_models.py
- [ ] T029 [US1] Implement PUT /semantic-models/{modelId} endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/semantic_models.py
- [ ] T030 [US1] Implement DELETE /semantic-models/{modelId} endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/semantic_models.py
- [ ] T031 [US1] Implement POST /semantic-models/{modelId}/entities endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/semantic_models.py
- [ ] T032 [US1] Implement POST /semantic-models/{modelId}/dimensions endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/semantic_models.py
- [ ] T033 [US1] Implement POST /semantic-models/{modelId}/measures endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/semantic_models.py
- [ ] T034 [US1] Implement semantic model validation logic (name uniqueness, required fields) in bls_data_catalog/semantic_manifest_editor/backend/services/validator.py
- [ ] T035 [US1] Register semantic model routes in bls_data_catalog/semantic_manifest_editor/backend/api/main.py

### Frontend Implementation for US1

- [ ] T036 [P] [US1] Create TypeScript types for NodeRelation in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T037 [P] [US1] Create TypeScript types for Entity with EntityType enum in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T038 [P] [US1] Create TypeScript types for Dimension with DimensionType and TimeGranularity enums in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T039 [P] [US1] Create TypeScript types for Measure with AggregationType enum in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T040 [P] [US1] Create TypeScript types for SemanticModel in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T041 [US1] Add semantic model CRUD methods to API client in bls_data_catalog/semantic_manifest_editor/frontend/src/services/api.ts
- [ ] T042 [US1] Create SemanticModelEditor component with form for name and node_relation in bls_data_catalog/semantic_manifest_editor/frontend/src/components/SemanticModelEditor/SemanticModelEditor.tsx
- [ ] T043 [US1] Create EntitiesGrid component using TanStack Table with inline editing in bls_data_catalog/semantic_manifest_editor/frontend/src/components/SemanticModelEditor/EntitiesGrid.tsx
- [ ] T044 [US1] Create DimensionsGrid component using TanStack Table with type_params handling in bls_data_catalog/semantic_manifest_editor/frontend/src/components/SemanticModelEditor/DimensionsGrid.tsx
- [ ] T045 [US1] Create MeasuresGrid component using TanStack Table with aggregation type selector in bls_data_catalog/semantic_manifest_editor/frontend/src/components/SemanticModelEditor/MeasuresGrid.tsx
- [ ] T046 [US1] Implement client-side validation for semantic model fields in bls_data_catalog/semantic_manifest_editor/frontend/src/utils/validators.ts
- [ ] T047 [US1] Add semantic model state management to Zustand store in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useManifest.ts
- [ ] T048 [US1] Create ModelsList component to display all semantic models in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/ModelsList.tsx
- [ ] T049 [US1] Create JSONViewer component to show generated manifest structure in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/JSONViewer.tsx
- [ ] T050 [US1] Integrate SemanticModelEditor into main App component in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create semantic models with entities, dimensions, and measures, and view the generated JSON

---

## Phase 4: User Story 2 - Define Metrics from Measures (Priority: P2)

**Goal**: Enable users to create simple, ratio, and derived metrics from semantic model measures

**Independent Test**: Create a simple metric, ratio metric (unemployment rate), and derived metric with custom expression, verify all appear in generated JSON with correct type_params

### Backend Implementation for US2

- [ ] T051 [P] [US2] Create MeasureReference Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T052 [P] [US2] Create SimpleMetricParams Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T053 [P] [US2] Create RatioMetricParams Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T054 [P] [US2] Create DerivedMetricParams Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T055 [P] [US2] Create Metric Pydantic model with discriminated union for type_params in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T056 [US2] Implement POST /metrics endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/metrics.py
- [ ] T057 [US2] Implement GET /metrics endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/metrics.py
- [ ] T058 [US2] Implement GET /metrics/{metricId} endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/metrics.py
- [ ] T059 [US2] Implement PUT /metrics/{metricId} endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/metrics.py
- [ ] T060 [US2] Implement DELETE /metrics/{metricId} endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/metrics.py
- [ ] T061 [US2] Implement metric validation (name uniqueness, measure references exist, no circular dependencies) in bls_data_catalog/semantic_manifest_editor/backend/services/validator.py
- [ ] T062 [US2] Register metric routes in bls_data_catalog/semantic_manifest_editor/backend/api/main.py

### Frontend Implementation for US2

- [ ] T063 [P] [US2] Create TypeScript types for MeasureReference in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T064 [P] [US2] Create TypeScript types for Metric with MetricType enum and type_params variants in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T065 [US2] Add metric CRUD methods to API client in bls_data_catalog/semantic_manifest_editor/frontend/src/services/api.ts
- [ ] T066 [US2] Create MetricEditor component with type selector in bls_data_catalog/semantic_manifest_editor/frontend/src/components/MetricEditor/MetricEditor.tsx
- [ ] T067 [US2] Create SimpleMetricForm component with measure selector dropdown in bls_data_catalog/semantic_manifest_editor/frontend/src/components/MetricEditor/SimpleMetricForm.tsx
- [ ] T068 [US2] Create RatioMetricForm component with numerator and denominator selectors in bls_data_catalog/semantic_manifest_editor/frontend/src/components/MetricEditor/RatioMetricForm.tsx
- [ ] T069 [US2] Create DerivedMetricForm component with expression editor in bls_data_catalog/semantic_manifest_editor/frontend/src/components/MetricEditor/DerivedMetricForm.tsx
- [ ] T070 [US2] Implement client-side metric validation (measure references, expression syntax) in bls_data_catalog/semantic_manifest_editor/frontend/src/utils/validators.ts
- [ ] T071 [US2] Add metric state management to Zustand store in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useManifest.ts
- [ ] T072 [US2] Create MetricsList component to display all metrics in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/MetricsList.tsx
- [ ] T073 [US2] Integrate MetricEditor into main App component in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can create semantic models and metrics

---

## Phase 5: User Story 4 - Validate Manifest Structure (Priority: P2)

**Goal**: Provide real-time validation with descriptive error messages and optional database schema validation

**Independent Test**: Create semantic model with missing required field (e.g., entity type), verify error appears with location and suggestion; trigger database validation and verify table/column existence checks

### Backend Implementation for US4

- [ ] T074 [P] [US4] Create ValidationError Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T075 [P] [US4] Create ValidationResult Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T076 [US4] Implement POST /validation/schema endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/validation.py
- [ ] T077 [US4] Implement manifest structure validation logic (required fields, uniqueness constraints) in bls_data_catalog/semantic_manifest_editor/backend/services/validator.py
- [ ] T078 [US4] Implement circular dependency detection for derived metrics in bls_data_catalog/semantic_manifest_editor/backend/services/validator.py
- [ ] T079 [US4] Implement POST /validation/database endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/validation.py
- [ ] T080 [US4] Create database validator service with DuckDB queries in bls_data_catalog/semantic_manifest_editor/backend/services/db_validator.py
- [ ] T081 [US4] Implement table existence validation using information_schema in bls_data_catalog/semantic_manifest_editor/backend/services/db_validator.py
- [ ] T082 [US4] Implement column existence validation using information_schema in bls_data_catalog/semantic_manifest_editor/backend/services/db_validator.py
- [ ] T083 [US4] Register validation routes in bls_data_catalog/semantic_manifest_editor/backend/api/main.py

### Frontend Implementation for US4

- [ ] T084 [P] [US4] Create TypeScript types for ValidationError in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T085 [P] [US4] Create TypeScript types for ValidationResult in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T086 [US4] Add validation API methods to client in bls_data_catalog/semantic_manifest_editor/frontend/src/services/api.ts
- [ ] T087 [US4] Create useValidation hook with debounced validation in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useValidation.ts
- [ ] T088 [US4] Create ErrorDisplay component showing error location and suggestion in bls_data_catalog/semantic_manifest_editor/frontend/src/components/Validation/ErrorDisplay.tsx
- [ ] T089 [US4] Create ValidationPanel component with error summary in bls_data_catalog/semantic_manifest_editor/frontend/src/components/Validation/ValidationPanel.tsx
- [ ] T090 [US4] Add inline validation error indicators to grid components in bls_data_catalog/semantic_manifest_editor/frontend/src/components/SemanticModelEditor/
- [ ] T091 [US4] Implement real-time validation trigger on field changes in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useManifest.ts
- [ ] T092 [US4] Add database validation button and status indicator in bls_data_catalog/semantic_manifest_editor/frontend/src/components/Validation/ValidationPanel.tsx
- [ ] T093 [US4] Integrate ValidationPanel into main App component in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx

**Checkpoint**: Validation should work for both client and server side with clear error messages

---

## Phase 6: User Story 5 - Export and Save Manifest (Priority: P2)

**Goal**: Enable users to export semantic_manifest.json and save/load different versions

**Independent Test**: Create semantic model and metric, export manifest, verify it passes MetricFlow CLI; save version, reload page, verify saved version loads correctly

### Backend Implementation for US5

- [ ] T094 [P] [US5] Create Manifest Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T095 [P] [US5] Create ManifestVersion Pydantic model in bls_data_catalog/semantic_manifest_editor/backend/api/models.py
- [ ] T096 [US5] Implement manifest builder service to construct semantic_manifest.json in bls_data_catalog/semantic_manifest_editor/backend/services/manifest_builder.py
- [ ] T097 [US5] Implement POST /manifest/import endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/manifest.py
- [ ] T098 [US5] Implement GET /manifest/export endpoint with JSON download in bls_data_catalog/semantic_manifest_editor/backend/api/routes/manifest.py
- [ ] T099 [US5] Implement POST /manifest/save endpoint for versioning in bls_data_catalog/semantic_manifest_editor/backend/api/routes/manifest.py
- [ ] T100 [US5] Implement GET /manifest/versions endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/manifest.py
- [ ] T101 [US5] Implement GET /manifest/versions/{versionId} endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/manifest.py
- [ ] T102 [US5] Implement DELETE /manifest/versions/{versionId} endpoint in bls_data_catalog/semantic_manifest_editor/backend/api/routes/manifest.py
- [ ] T103 [US5] Add project_configuration generation in manifest builder in bls_data_catalog/semantic_manifest_editor/backend/services/manifest_builder.py
- [ ] T104 [US5] Register manifest routes in bls_data_catalog/semantic_manifest_editor/backend/api/main.py

### Frontend Implementation for US5

- [ ] T105 [P] [US5] Create TypeScript types for Manifest in bls_data_catalog/semantic_manifest_editor/frontend/src/types/manifest.ts
- [ ] T106 [US5] Add manifest import/export/save API methods to client in bls_data_catalog/semantic_manifest_editor/frontend/src/services/api.ts
- [ ] T107 [US5] Implement export manifest function with file download in bls_data_catalog/semantic_manifest_editor/frontend/src/utils/manifestBuilder.ts
- [ ] T108 [US5] Implement import manifest file upload handler in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/ManifestEditor.tsx
- [ ] T109 [US5] Create useAutoSave hook with LocalStorage persistence in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useAutoSave.ts
- [ ] T110 [US5] Implement auto-save every 30 seconds in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useAutoSave.ts
- [ ] T111 [US5] Create save version dialog component in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/SaveVersionDialog.tsx
- [ ] T112 [US5] Create versions list component with load/delete actions in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/VersionsList.tsx
- [ ] T113 [US5] Add export and save buttons to toolbar in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx
- [ ] T114 [US5] Implement manifest state hydration from LocalStorage on app load in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useManifest.ts

**Checkpoint**: Export/save/load functionality complete - manifests persist and can be transferred to MetricFlow

---

## Phase 7: User Story 3 - Import Existing Manifest (Priority: P3)

**Goal**: Enable users to upload and edit existing semantic_manifest.json files

**Independent Test**: Upload valid semantic_manifest.json with 10 semantic models, verify all models/metrics load correctly in editor UI and are editable

### Frontend Implementation for US3

- [ ] T115 [US3] Implement JSON file parser with schema validation in bls_data_catalog/semantic_manifest_editor/frontend/src/utils/manifestBuilder.ts
- [ ] T116 [US3] Handle complex structures (non_additive_dimension, agg_time_dimension) in parser in bls_data_catalog/semantic_manifest_editor/frontend/src/utils/manifestBuilder.ts
- [ ] T117 [US3] Implement manifest version detection in bls_data_catalog/semantic_manifest_editor/frontend/src/utils/manifestBuilder.ts
- [ ] T118 [US3] Add file upload UI component with drag-drop in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/ImportDialog.tsx
- [ ] T119 [US3] Handle import errors with user-friendly messages in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/ImportDialog.tsx
- [ ] T120 [US3] Populate Zustand store from imported manifest in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useManifest.ts
- [ ] T121 [US3] Add import button to toolbar in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx

**Checkpoint**: Import functionality complete - existing manifests can be loaded and edited

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T122 [P] Add undo/redo functionality using Zustand temporal middleware in bls_data_catalog/semantic_manifest_editor/frontend/src/hooks/useManifest.ts
- [ ] T123 [P] Implement duplicate semantic model feature in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/ModelsList.tsx
- [ ] T124 [P] Implement duplicate metric feature in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/MetricsList.tsx
- [ ] T125 [P] Add keyboard shortcuts for common operations in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx
- [ ] T126 [P] Optimize rendering for large manifests (50+ models) with virtualization in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/ModelsList.tsx
- [ ] T127 [P] Add loading states and progress indicators in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx
- [ ] T128 [P] Implement debounced search/filter for models and metrics in bls_data_catalog/semantic_manifest_editor/frontend/src/components/ManifestEditor/
- [ ] T129 [P] Add toast notifications for user actions in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx
- [ ] T130 [P] Create comprehensive error boundary in bls_data_catalog/semantic_manifest_editor/frontend/src/App.tsx
- [ ] T131 [P] Add metadata and config property editors in bls_data_catalog/semantic_manifest_editor/frontend/src/components/SemanticModelEditor/
- [ ] T132 Optimize API payload sizes for large manifests in bls_data_catalog/semantic_manifest_editor/backend/api/routes/
- [ ] T133 Add connection pooling for DuckDB in bls_data_catalog/semantic_manifest_editor/backend/config.py
- [ ] T134 Implement caching for database schema validation results in bls_data_catalog/semantic_manifest_editor/backend/services/db_validator.py
- [ ] T135 Add comprehensive logging for backend operations in bls_data_catalog/semantic_manifest_editor/backend/api/
- [ ] T136 Create user documentation in bls_data_catalog/semantic_manifest_editor/README.md
- [ ] T137 Validate against quickstart.md scenarios in bls_data_catalog/semantic_manifest_editor/
- [ ] T138 Performance testing for SC-007 (50 models, 200 metrics) in bls_data_catalog/semantic_manifest_editor/
- [ ] T139 Security review for input validation and SQL injection prevention in bls_data_catalog/semantic_manifest_editor/backend/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 1 (P1) can start first - highest priority, no dependencies
  - User Story 2 (P2) can start after Foundational - depends on US1 for measure references
  - User Story 4 (P2) can start after Foundational - validates work from US1 and US2
  - User Story 5 (P2) can start after Foundational - exports work from US1 and US2
  - User Story 3 (P3) can start after Foundational - imports manifests for editing
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Create Semantic Models**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2) - Define Metrics**: Should start after US1 complete (needs measures from semantic models)
- **User Story 4 (P2) - Validation**: Can develop in parallel with US1/US2, integrates with both
- **User Story 5 (P2) - Export/Save**: Can develop in parallel with US1/US2, integrates with both
- **User Story 3 (P3) - Import**: Can start after Foundational, best after US1/US2 to test importing edited manifests

### Recommended Execution Order

1. **MVP Path** (fastest to demo):
   - Phase 1: Setup
   - Phase 2: Foundational
   - Phase 3: User Story 1 (create semantic models)
   - Phase 6: User Story 5 (export manifest) - just export functionality
   - **STOP - Validate MVP**: Can create and export semantic models

2. **Full Feature Path**:
   - Continue from MVP
   - Phase 4: User Story 2 (metrics)
   - Phase 5: User Story 4 (validation)
   - Complete Phase 6: User Story 5 (save/versions)
   - Phase 7: User Story 3 (import)
   - Phase 8: Polish

### Within Each User Story

- Backend models before services
- Backend services before routes
- Backend routes registered before frontend starts
- Frontend types before components
- Frontend API client before components
- Frontend components before integration
- Core functionality before polish features

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T003, T004 can run in parallel (backend and frontend initialization)
- T005-T009 can run in parallel (configuration tasks for both frontend and backend)

**Foundational Phase (Phase 2)**:
- T010-T011 can run in parallel (backend and frontend models)
- T012-T016 can run in parallel (backend services)
- T018-T019 can run in parallel (error handling and storage)

**User Story 1 Backend**:
- T021-T025 can run in parallel (all Pydantic models)

**User Story 1 Frontend**:
- T036-T040 can run in parallel (all TypeScript types)

**User Story 2 Backend**:
- T051-T055 can run in parallel (all metric-related Pydantic models)

**User Story 2 Frontend**:
- T063-T064 can run in parallel (metric TypeScript types)

**User Story 4 Backend**:
- T074-T075 can run in parallel (validation models)

**User Story 5 Backend**:
- T094-T095 can run in parallel (manifest models)

**Polish Phase (Phase 8)**:
- T122-T131 can run in parallel (all frontend polish tasks)
- T132-T135 can run in parallel (all backend optimization tasks)

**Different User Stories**:
Once Foundational (Phase 2) is complete:
- US4 (Validation) and US5 (Export/Save) can be developed in parallel
- US1 (Models) should complete before US2 (Metrics) starts
- US3 (Import) can be developed in parallel with US2, US4, US5

---

## Parallel Example: User Story 1 Backend Models

```bash
# Launch all Pydantic models for User Story 1 together:
Task: "Create NodeRelation Pydantic model in backend/api/models.py"
Task: "Create Entity Pydantic model in backend/api/models.py"
Task: "Create Dimension Pydantic model in backend/api/models.py"
Task: "Create Measure Pydantic model in backend/api/models.py"
Task: "Create SemanticModel Pydantic model in backend/api/models.py"
```

## Parallel Example: User Story 1 Frontend Types

```bash
# Launch all TypeScript types for User Story 1 together:
Task: "Create TypeScript types for NodeRelation in frontend/src/types/manifest.ts"
Task: "Create TypeScript types for Entity in frontend/src/types/manifest.ts"
Task: "Create TypeScript types for Dimension in frontend/src/types/manifest.ts"
Task: "Create TypeScript types for Measure in frontend/src/types/manifest.ts"
Task: "Create TypeScript types for SemanticModel in frontend/src/types/manifest.ts"
```

---

## Implementation Strategy

### MVP First (User Story 1 + Basic Export Only)

1. Complete Phase 1: Setup → ~9 tasks → Project structure ready
2. Complete Phase 2: Foundational → ~11 tasks → Foundation ready (CRITICAL)
3. Complete Phase 3: User Story 1 → ~30 tasks → Can create semantic models
4. Complete Phase 6: T097-T098, T105-T107 → ~6 tasks → Can export manifest
5. **STOP and VALIDATE**: Test User Story 1 + export independently
6. Deploy/demo if ready - **Core value delivered**: Create and export semantic models

**MVP Delivers**: Users can create semantic models with entities, dimensions, measures and export valid semantic_manifest.json files for use with MetricFlow CLI. Estimated: ~56 tasks.

### Incremental Delivery

1. **Foundation** (Phase 1 + 2): ~20 tasks → Foundation ready
2. **MVP** (Phase 3 + partial Phase 6): ~36 tasks → Create and export semantic models
3. **Metrics** (Phase 4): ~23 tasks → Add metric creation capability
4. **Validation** (Phase 5): ~20 tasks → Add validation feedback
5. **Full Persistence** (complete Phase 6): ~8 tasks → Add save/load versions
6. **Import** (Phase 7): ~7 tasks → Add import existing manifests
7. **Polish** (Phase 8): ~18 tasks → Optimize and enhance UX

Each increment adds value without breaking previous functionality.

### Parallel Team Strategy

With 3 developers after Foundational phase:

**Week 1-2**:
- Developer A: User Story 1 (semantic models) - Priority P1
- Developer B: User Story 5 (export/save infrastructure) - P2
- Developer C: User Story 4 (validation infrastructure) - P2

**Week 3-4**:
- Developer A: User Story 2 (metrics) - needs US1 complete
- Developer B: Complete User Story 5 (versions, import integration)
- Developer C: Complete User Story 4 (database validation)

**Week 5**:
- Developer A: User Story 3 (import) - P3
- Developer B: Polish phase (undo/redo, optimization)
- Developer C: Polish phase (performance, security)

---

## Task Count Summary

- **Phase 1 (Setup)**: 9 tasks
- **Phase 2 (Foundational)**: 11 tasks
- **Phase 3 (US1 - Semantic Models)**: 30 tasks (15 backend + 15 frontend)
- **Phase 4 (US2 - Metrics)**: 23 tasks (12 backend + 11 frontend)
- **Phase 5 (US4 - Validation)**: 20 tasks (10 backend + 10 frontend)
- **Phase 6 (US5 - Export/Save)**: 21 tasks (11 backend + 10 frontend)
- **Phase 7 (US3 - Import)**: 7 tasks (all frontend)
- **Phase 8 (Polish)**: 18 tasks

**Total**: 139 tasks

**MVP Scope** (US1 + basic export): ~56 tasks
**Full Feature**: 139 tasks

**Parallel Opportunities**: ~45 tasks marked [P] can run in parallel within their phases

---

## Notes

- [P] tasks = different files or independent sections, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable per acceptance scenarios in spec.md
- Tests are NOT included as they were not requested in the feature specification
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently using acceptance scenarios
- Follow quickstart.md for development environment setup and workflows
- Reference data-model.md for entity definitions and validation rules
- Reference contracts/api.openapi.yaml for complete API specifications
