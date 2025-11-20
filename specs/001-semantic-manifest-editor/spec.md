# Feature Specification: Semantic Manifest Editor

**Feature Branch**: `001-semantic-manifest-editor`
**Created**: 2025-11-20
**Status**: Draft
**Input**: User description: "Web interface for dynamically constructing semantic_manifest.json without requiring dbt build process"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Semantic Model (Priority: P1)

A data analyst needs to define a new semantic model for a data table by specifying its entities, dimensions, and measures through an interactive web interface, without writing YAML files or running dbt commands.

**Why this priority**: This is the foundational capability - users must be able to create semantic models before they can define metrics or query data. Without this, the feature delivers no value.

**Independent Test**: Can be fully tested by creating a semantic model with at least one entity, one dimension, and one measure, then validating that the generated JSON matches MetricFlow's semantic_manifest.json schema.

**Acceptance Scenarios**:

1. **Given** a user opens the editor, **When** they create a new semantic model with name, node relation details (alias, schema_name, database), and at least one entity, **Then** the system displays the model in the editor and includes it in the manifest JSON
2. **Given** a semantic model exists, **When** the user adds dimensions (time or categorical) using spreadsheet-like editing, **Then** each dimension appears in the model with name, type, and expression fields populated
3. **Given** a semantic model exists, **When** the user adds measures with aggregation types (sum, average, count, etc.), **Then** each measure appears in the model with correct aggregation and expression
4. **Given** a user has created a complete semantic model, **When** they request to view the generated JSON, **Then** the system displays valid semantic_manifest.json structure

---

### User Story 2 - Define Metrics from Measures (Priority: P2)

A data analyst needs to create metrics (simple, ratio, or derived) based on measures from semantic models, enabling business-level metric definitions without SQL knowledge.

**Why this priority**: Once semantic models exist, users need to create metrics for querying. This is the second essential capability that makes the models useful for analysis.

**Independent Test**: Can be fully tested by creating a simple metric referencing a measure, a ratio metric with numerator/denominator, and a derived metric with custom expression, then validating the metrics section of the generated JSON.

**Acceptance Scenarios**:

1. **Given** semantic models with measures exist, **When** user creates a simple metric selecting a measure, **Then** the metric appears with correct type and measure reference
2. **Given** multiple measures exist, **When** user creates a ratio metric selecting numerator and denominator measures, **Then** the metric displays the calculation and validates measure compatibility
3. **Given** existing metrics, **When** user creates a derived metric with a custom expression, **Then** the system validates the expression syntax and includes referenced metrics
4. **Given** a metric is created, **When** user edits the metric description or label, **Then** changes reflect immediately in both the editor and generated JSON

---

### User Story 3 - Import Existing Manifest (Priority: P3)

A user with an existing semantic_manifest.json file needs to import it into the editor to visualize, edit, and extend the semantic layer configuration.

**Why this priority**: Enables adoption for existing MetricFlow users and provides a migration path. Valuable but not required for MVP since users can start fresh.

**Independent Test**: Can be fully tested by uploading a valid semantic_manifest.json file and verifying all semantic models, measures, dimensions, and metrics appear correctly in the editor UI.

**Acceptance Scenarios**:

1. **Given** a user has a valid semantic_manifest.json file, **When** they upload it to the editor, **Then** all semantic models appear in the models list with their entities, dimensions, and measures
2. **Given** a manifest is imported, **When** the user views the metrics section, **Then** all metrics (simple, ratio, derived) display with their configurations
3. **Given** an imported manifest contains complex structures (non_additive_dimension, agg_time_dimension, filters), **When** displayed in the editor, **Then** all properties are visible and editable

---

### User Story 4 - Validate Manifest Structure (Priority: P2)

Users need real-time validation of their semantic manifest structure to catch errors before attempting to use it with MetricFlow, reducing iteration cycles.

**Why this priority**: Critical for user confidence and reducing errors, but depends on having semantic models/metrics created first (P1). Should be developed alongside or immediately after P1.

**Independent Test**: Can be fully tested by intentionally creating invalid configurations (missing required fields, invalid types, circular references) and verifying appropriate error messages appear.

**Acceptance Scenarios**:

1. **Given** a user is editing a semantic model, **When** they omit a required field like entity type or measure aggregation, **Then** the system displays an error indicator and descriptive message
2. **Given** a user creates a metric, **When** they reference a non-existent measure, **Then** the system shows a validation error with available measures
3. **Given** multiple validation errors exist, **When** the user requests the validation summary, **Then** all errors display with their locations and suggested fixes
4. **Given** a user fixes all validation errors, **When** they check validation status, **Then** the system confirms the manifest is valid and ready for export
5. **Given** a user requests database validation, **When** the backend validates expressions against the database schema, **Then** the system reports whether table and column references are valid

---

### User Story 5 - Export and Save Manifest (Priority: P2)

Users need to export the generated semantic_manifest.json file and save different versions for use with MetricFlow queries or future editing sessions.

**Why this priority**: Essential for actually using the created semantic layer, but only valuable after models and metrics are created (P1). Should be developed alongside P4.

**Independent Test**: Can be fully tested by creating a semantic model and metric, exporting the JSON, and successfully using it with the MetricFlow CLI to execute a query.

**Acceptance Scenarios**:

1. **Given** a user has created semantic models and metrics, **When** they request to export the manifest, **Then** the system downloads a valid semantic_manifest.json file
2. **Given** a manifest is exported, **When** used with MetricFlow CLI commands, **Then** the CLI successfully parses the manifest and executes queries
3. **Given** a user wants to save their work, **When** they request to save the current state, **Then** the system stores the manifest with a timestamp and user identifier
4. **Given** saved manifests exist, **When** the user views their saved versions, **Then** they can see timestamps, load previous versions, or delete old versions

---

### Edge Cases

- What happens when a user attempts to create a metric referencing measures from different semantic models that cannot be joined?
- How does the system handle invalid expressions in dimension or measure definitions?
- What happens when a user imports a manifest with a schema version different from what the editor supports?
- How does the system handle very large manifests with 50+ semantic models and 200+ metrics?
- What happens when a user creates circular dependencies in derived metrics (metric A references metric B which references metric A)?
- What happens when a user's browser crashes or loses connection during editing?
- How does the system handle special characters or reserved keywords in entity/dimension/measure names?
- What happens when database validation fails because the referenced table or column doesn't exist?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create new semantic models with name, description, and node relation details (alias, schema_name, database)
- **FR-002**: System MUST allow users to add, edit, and delete entities with name, type (primary, foreign, unique), and expression fields
- **FR-003**: System MUST allow users to add, edit, and delete dimensions with name, type (time, categorical), and expression fields
- **FR-004**: System MUST allow users to add, edit, and delete measures with name, aggregation type (sum, average, count, min, max), expression, and optional description
- **FR-005**: System MUST validate that time dimensions include time_granularity parameter
- **FR-006**: System MUST allow users to create simple metrics by selecting a measure from available semantic models
- **FR-007**: System MUST allow users to create ratio metrics by selecting numerator and denominator measures
- **FR-008**: System MUST allow users to create derived metrics by writing custom expressions referencing other metrics
- **FR-009**: System MUST validate metric expressions syntax before allowing save
- **FR-010**: System MUST allow users to export the complete semantic_manifest.json file matching MetricFlow's schema
- **FR-011**: System MUST allow users to import existing semantic_manifest.json files and populate the editor
- **FR-012**: System MUST display real-time validation errors with descriptive messages and error locations
- **FR-013**: System MUST allow users to view the raw JSON structure at any time during editing
- **FR-014**: System MUST persist user's work in progress to prevent data loss
- **FR-015**: System MUST support undo/redo operations for editing actions
- **FR-016**: System MUST allow users to duplicate existing semantic models or metrics as templates
- **FR-017**: System MUST validate that entity, dimension, and measure names are unique within a semantic model
- **FR-018**: System MUST validate that semantic model names and metric names are unique within the manifest
- **FR-019**: System MUST display available measures when creating metrics to prevent reference errors
- **FR-020**: System MUST support adding metadata and configuration properties to semantic models and metrics
- **FR-021**: System MUST validate dimension and measure expressions against actual database tables and columns when validation is requested
- **FR-022**: System MUST use backend-managed database credentials for validation without exposing connection details to the frontend
- **FR-023**: System MUST support hardcoded DuckDB connection for MVP validation testing

### Key Entities

- **Semantic Model**: Represents a data table/view with its semantic layer definition, including name, database location, entities, dimensions, measures, and optional default settings
- **Entity**: Represents a joinable key in the semantic model with name, type (primary, foreign, unique), and expression that maps to a column
- **Dimension**: Represents an attribute for grouping or filtering with name, type (time or categorical), expression, and time granularity for time dimensions
- **Measure**: Represents an aggregatable metric component with name, aggregation type, expression, and optional description
- **Metric**: Represents a business metric with name, type (simple, ratio, derived), description, and type-specific parameters (measure reference, numerator/denominator, or expression)
- **Manifest**: The complete semantic layer configuration containing all semantic models and metrics

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a complete semantic model with 1 entity, 3 dimensions, and 5 measures in under 10 minutes
- **SC-002**: Users can define a ratio metric (e.g., unemployment rate) in under 2 minutes after measures exist
- **SC-003**: The editor displays validation feedback within 500 milliseconds of user input
- **SC-004**: 95% of exported manifests successfully pass MetricFlow CLI validation on first attempt
- **SC-005**: Users can import and edit an existing semantic_manifest.json with 10 semantic models in under 30 seconds load time
- **SC-006**: Zero data loss occurs during editing sessions (auto-save and recovery mechanisms work)
- **SC-007**: Users can navigate and edit manifests with up to 50 semantic models and 200 metrics without performance degradation
- **SC-008**: Validation errors provide actionable guidance, enabling users to fix issues without external documentation in 90% of cases
- **SC-009**: Database validation completes within 3 seconds for semantic models with up to 20 dimensions and measures

## Assumptions *(mandatory)*

### Technical Assumptions

- Users have access to a modern web browser (Chrome, Firefox, Safari, Edge) with JavaScript enabled
- The semantic_manifest.json schema follows MetricFlow's documented structure (project_configuration, semantic_models, metrics)
- Database credentials are managed by the backend system and retrieved as secrets (not stored in the frontend or manifest)
- For MVP, a hardcoded connection to a local DuckDB file will be used for validation testing
- Users understand basic data modeling concepts (tables, columns, joins, aggregations)

### Business Assumptions

- Users are data analysts, analytics engineers, or BI developers familiar with semantic layer concepts
- Primary use case is creating and maintaining semantic layers for MetricFlow-based analytics platforms
- Users prefer interactive web interfaces over editing YAML/JSON files directly
- The editor will initially support single-user editing (no real-time collaboration required in MVP)
- Users will manually transfer exported semantic_manifest.json files to their MetricFlow environment

### Data Assumptions

- Semantic manifest structures remain backward compatible with minor MetricFlow version updates
- Typical manifests contain 5-20 semantic models with 10-50 metrics
- Time dimensions use standard granularities (day, week, month, quarter, year)
- Measure aggregations follow standard SQL aggregation functions

## Constraints *(mandatory)*

### Technical Constraints

- Editor frontend handles manifest construction and editing (semantic models, dimensions, measures, metrics)
- Backend API handles database credential management and validation queries
- For MVP, validation uses a hardcoded DuckDB connection string to local file (future: dropdown to select from available credential secrets)
- Exported JSON must conform exactly to MetricFlow's semantic_manifest.json schema
- Import functionality must handle both single semantic models and complete manifests
- Browser local storage limits may restrict the size of manifests that can be auto-saved (typical 5-10MB limit)

### Scope Constraints

- Editor does not manage or store database credentials (backend handles credential retrieval from secrets)
- MVP uses hardcoded DuckDB connection for validation (future: credential selection dropdown)
- Editor does not provide comprehensive query testing (validation focuses on schema correctness)
- Editor does not provide data lineage visualization or impact analysis
- Editor does not include user authentication or multi-user collaboration features in MVP
- Editor does not support version control integration (Git) in initial release
- Editor does not provide AI-assisted metric suggestions or auto-generation

### User Experience Constraints

- Interface must be usable on desktop/laptop screens (minimum 1280x720 resolution)
- Spreadsheet-like editing should support keyboard navigation and standard shortcuts
- Validation must not block user input (warnings/errors display but don't prevent editing)

## Dependencies & Integrations *(mandatory)*

### External Dependencies

- MetricFlow semantic_manifest.json schema specification (must stay synchronized with MetricFlow releases)
- JSON Schema standard for validation rules
- DuckDB database file for MVP validation testing
- Backend API for database credential management (future enhancement)

### Integration Points

- **Input**: Users can upload semantic_manifest.json files from their MetricFlow projects
- **Output**: Users export semantic_manifest.json files for use with MetricFlow CLI or integrations
- **Validation**: Backend API validates expressions against database schema using managed credentials (MVP: hardcoded DuckDB connection)

### Future Integration Opportunities

- Credential selection dropdown to choose from available database secrets
- MetricFlow CLI integration for in-browser query testing
- Version control system integration (GitHub, GitLab)
- Cloud storage integration for manifest persistence
- Analytics platform integration (dbt Cloud, Looker, Tableau)
