# Data Model: Semantic Manifest Editor

**Feature**: 001-semantic-manifest-editor
**Date**: 2025-11-20
**Phase**: 1 - Design & Contracts

## Overview

This document defines the data structures for the Semantic Manifest Editor. The model closely follows MetricFlow's `semantic_manifest.json` schema while adding editor-specific metadata for UI state management.

## Core Entities

### Manifest

The root container for the entire semantic layer configuration.

**Fields**:
- `semantic_models`: Array of SemanticModel - Collection of semantic models
- `metrics`: Array of Metric - Collection of metrics
- `project_configuration`: ProjectConfiguration - MetricFlow project settings
- `saved_queries`: Array (optional) - Pre-defined saved queries

**Editor Metadata** (not exported):
- `version`: String - Editor version that created this manifest
- `created_at`: DateTime - When manifest was created
- `modified_at`: DateTime - Last modification timestamp
- `validation_status`: ValidationStatus - Current validation state

**Relationships**:
- Contains multiple SemanticModel entities
- Contains multiple Metric entities
- Metrics reference Measures from SemanticModels

**Validation Rules**:
- Semantic model names must be unique across manifest
- Metric names must be unique across manifest
- All metric measure references must resolve to existing measures

### SemanticModel

Represents a data table or view with its semantic layer definition.

**Fields**:
- `name`: String (required) - Unique identifier for the semantic model
- `description`: String (optional) - Human-readable description
- `node_relation`: NodeRelation (required) - Database table/view location
- `defaults`: ModelDefaults (optional) - Default time dimension and other settings
- `entities`: Array of Entity (required) - At least one entity required
- `dimensions`: Array of Dimension (optional) - Attributes for grouping/filtering
- `measures`: Array of Measure (optional) - Aggregatable metrics
- `primary_entity`: String (optional) - Name of the primary entity
- `label`: String (optional) - Display label
- `metadata`: Object (optional) - Additional metadata
- `config`: Object (optional) - Configuration options

**Editor Metadata** (not exported):
- `id`: UUID - Internal identifier for editor operations
- `expanded`: Boolean - UI expansion state
- `validation_errors`: Array of ValidationError - Current errors

**Relationships**:
- Contains multiple Entity, Dimension, and Measure objects
- Referenced by Metric objects

**Validation Rules**:
- Name must be unique within manifest
- Must have at least one Entity
- Entity names must be unique within semantic model
- Dimension names must be unique within semantic model
- Measure names must be unique within semantic model
- Primary entity (if specified) must match an entity name

**State Transitions**:
```
[New] → [Editing] → [Valid] ⟷ [Invalid]
                ↓
            [Deleted]
```

### NodeRelation

Database location information for a semantic model.

**Fields**:
- `alias`: String (required) - Table/view alias
- `schema_name`: String (required) - Database schema name
- `database`: String (required) - Database name
- `relation_name`: String (optional) - Full qualified name (auto-generated)

**Validation Rules**:
- All fields required (alias, schema_name, database)
- Characters must be valid SQL identifiers

### Entity

Represents a joinable key in the semantic model.

**Fields**:
- `name`: String (required) - Unique name within semantic model
- `type`: EntityType (required) - One of: primary, foreign, unique
- `expr`: String (optional) - SQL expression (defaults to name)
- `description`: String (optional) - Human-readable description
- `role`: String (optional) - Entity role for joins
- `label`: String (optional) - Display label
- `metadata`: Object (optional) - Additional metadata
- `config`: Object (optional) - Configuration options

**Validation Rules**:
- Name must be unique within semantic model
- Type must be one of: primary, foreign, unique
- At least one primary entity required per semantic model
- Expression must be valid SQL column reference

### Dimension

Represents an attribute for grouping or filtering.

**Fields**:
- `name`: String (required) - Unique name within semantic model
- `type`: DimensionType (required) - One of: time, categorical
- `expr`: String (required) - SQL expression
- `description`: String (optional) - Human-readable description
- `type_params`: DimensionTypeParams (conditional) - Required for time dimensions
- `is_partition`: Boolean (optional) - Whether dimension is a partition key
- `label`: String (optional) - Display label
- `metadata`: Object (optional) - Additional metadata
- `config`: Object (optional) - Configuration options

**DimensionTypeParams** (for time dimensions):
- `time_granularity`: TimeGranularity (required) - One of: day, week, month, quarter, year
- `validity_params`: Object (optional) - Validity window parameters

**Validation Rules**:
- Name must be unique within semantic model
- Type must be categorical or time
- Time dimensions MUST include time_granularity in type_params
- Expression must be valid SQL

### Measure

Represents an aggregatable metric component.

**Fields**:
- `name`: String (required) - Unique name within semantic model
- `agg`: AggregationType (required) - One of: sum, average, count, min, max, count_distinct
- `expr`: String (optional) - SQL expression (defaults to name)
- `description`: String (optional) - Human-readable description
- `create_metric`: Boolean (optional) - Whether to auto-create simple metric
- `agg_params`: Object (optional) - Aggregation parameters
- `non_additive_dimension`: Object (optional) - For semi-additive measures
- `agg_time_dimension`: String (optional) - Specific time dimension for aggregation
- `label`: String (optional) - Display label
- `metadata`: Object (optional) - Additional metadata
- `config`: Object (optional) - Configuration options

**Validation Rules**:
- Name must be unique within semantic model
- Aggregation type must be one of: sum, average, count, min, max, count_distinct
- Expression must be valid SQL
- agg_time_dimension (if specified) must reference existing dimension

### Metric

Represents a business metric calculated from measures.

**Fields**:
- `name`: String (required) - Unique metric name
- `type`: MetricType (required) - One of: simple, ratio, derived
- `description`: String (optional) - Human-readable description
- `type_params`: MetricTypeParams (required) - Type-specific parameters
- `filter`: Object (optional) - Filter conditions
- `label`: String (optional) - Display label
- `metadata`: Object (optional) - Additional metadata
- `config`: Object (optional) - Configuration options

**MetricTypeParams** (varies by type):

**Simple Metric**:
- `measure`: MeasureReference (required) - Reference to a single measure
  - `name`: String - Measure name
  - `filter`: Object (optional) - Filter for this measure
  - `alias`: String (optional) - Alias for the measure

**Ratio Metric**:
- `numerator`: MeasureReference (required) - Top of ratio
- `denominator`: MeasureReference (required) - Bottom of ratio

**Derived Metric**:
- `expr`: String (required) - SQL expression referencing other metrics
- `metrics`: Array of MetricReference (required) - Metrics used in expression

**Editor Metadata** (not exported):
- `id`: UUID - Internal identifier
- `validation_errors`: Array of ValidationError

**Validation Rules**:
- Name must be unique within manifest
- Type must be simple, ratio, or derived
- Simple metric: measure must reference existing measure
- Ratio metric: numerator and denominator must reference existing measures
- Derived metric: all referenced metrics must exist
- No circular dependencies (metric A references B references A)

**State Transitions**:
```
[New] → [Editing] → [Valid] ⟷ [Invalid]
                ↓
            [Deleted]
```

### ValidationError

Error information for validation failures.

**Fields**:
- `severity`: ErrorSeverity - One of: error, warning, info
- `code`: String - Error code (e.g., "MISSING_REQUIRED_FIELD")
- `message`: String - Human-readable error message
- `location`: String - JSON path to error location (e.g., "semantic_models[0].measures[2].agg")
- `suggestion`: String (optional) - Suggested fix
- `timestamp`: DateTime - When error was detected

**Example**:
```json
{
  "severity": "error",
  "code": "MISSING_REQUIRED_FIELD",
  "message": "Missing required field: agg",
  "location": "semantic_models[0].measures[2].agg",
  "suggestion": "Valid aggregation types: sum, average, count, min, max",
  "timestamp": "2025-11-20T15:30:00Z"
}
```

### ValidationStatus

Overall validation state for manifest or entity.

**Fields**:
- `status`: ValidationState - One of: valid, invalid, warning, pending
- `last_validated`: DateTime - When validation last ran
- `errors`: Array of ValidationError - Current errors
- `warnings`: Array of ValidationError - Current warnings

**State Transitions**:
```
[Pending] → [Validating] → [Valid]
                        ↘ [Invalid]
                        ↘ [Warning]
```

## Enumerations

### EntityType
```typescript
enum EntityType {
  PRIMARY = "primary",
  FOREIGN = "foreign",
  UNIQUE = "unique"
}
```

### DimensionType
```typescript
enum DimensionType {
  TIME = "time",
  CATEGORICAL = "categorical"
}
```

### TimeGranularity
```typescript
enum TimeGranularity {
  DAY = "day",
  WEEK = "week",
  MONTH = "month",
  QUARTER = "quarter",
  YEAR = "year"
}
```

### AggregationType
```typescript
enum AggregationType {
  SUM = "sum",
  AVERAGE = "average",
  COUNT = "count",
  MIN = "min",
  MAX = "max",
  COUNT_DISTINCT = "count_distinct"
}
```

### MetricType
```typescript
enum MetricType {
  SIMPLE = "simple",
  RATIO = "ratio",
  DERIVED = "derived"
}
```

### ValidationState
```typescript
enum ValidationState {
  VALID = "valid",
  INVALID = "invalid",
  WARNING = "warning",
  PENDING = "pending"
}
```

### ErrorSeverity
```typescript
enum ErrorSeverity {
  ERROR = "error",
  WARNING = "warning",
  INFO = "info"
}
```

## Data Flow

### Create Semantic Model Flow

```
User Input (UI)
  ↓
SemanticModel {
  name: "us_employment"
  node_relation: { alias, schema, database }
  entities: []
  dimensions: []
  measures: []
}
  ↓
Client-side Validation
  ↓
API POST /semantic-models
  ↓
Server-side Validation (Pydantic)
  ↓
Manifest State Update
  ↓
Response with Validation Result
```

### Metric Creation Flow

```
User Selects Measures
  ↓
Metric {
  name: "unemployment_rate"
  type: "ratio"
  type_params: {
    numerator: { name: "unemployed" }
    denominator: { name: "labor_force" }
  }
}
  ↓
Client Validation (measures exist?)
  ↓
API POST /metrics
  ↓
Server Validation
  - Measures exist?
  - Measures from compatible models?
  - No circular dependencies?
  ↓
Manifest Update
```

### Database Validation Flow

```
User Triggers Validation
  ↓
API POST /validation/database
  {
    semantic_model_id: "uuid",
    check: ["entities", "dimensions", "measures"]
  }
  ↓
Backend Service
  - Connect to DuckDB
  - Query information_schema
  - Check table exists
  - Check columns exist
  - Validate data types
  ↓
Return Validation Result
  {
    status: "invalid",
    errors: [
      { location: "dimensions[0].expr", message: "Column 'foo' does not exist" }
    ]
  }
```

## Storage Model

### Browser LocalStorage Structure

```json
{
  "semantic-manifest-autosave": {
    "manifest": { /* full manifest object */ },
    "timestamp": "2025-11-20T15:30:00Z",
    "version": "1.0.0"
  },
  "semantic-manifest-versions": [
    {
      "id": "uuid-1",
      "name": "Version 1",
      "timestamp": "2025-11-20T14:00:00Z",
      "manifest": { /* full manifest */ }
    }
  ]
}
```

**Size Management**:
- Auto-save replaces previous auto-save
- Manual saves kept up to 10 versions
- Oldest versions pruned when approaching 5MB limit
- User warned if manifest exceeds reasonable size

### Export File Format

Standard `semantic_manifest.json` format matching MetricFlow specification:

```json
{
  "semantic_models": [ /* array of models */ ],
  "metrics": [ /* array of metrics */ ],
  "project_configuration": {
    "time_spine_table_configurations": [ /* time spine config */ ],
    "dsi_package_version": { /* version info */ }
  },
  "saved_queries": []
}
```

**Note**: Editor metadata (ids, validation_errors, UI state) is stripped during export.

## Entity Relationships Diagram

```
Manifest (1) ──contains──> (N) SemanticModel
Manifest (1) ──contains──> (N) Metric

SemanticModel (1) ──has──> (1) NodeRelation
SemanticModel (1) ──contains──> (N) Entity
SemanticModel (1) ──contains──> (N) Dimension
SemanticModel (1) ──contains──> (N) Measure

Metric (N) ──references──> (N) Measure  [via type_params]
Metric (N) ──references──> (N) Metric   [derived metrics only]

Entity, Dimension, Measure, Metric (N) ──has──> (N) ValidationError
Manifest, SemanticModel (1) ──has──> (1) ValidationStatus
```

## Validation Rules Summary

| Entity | Uniqueness Constraints | Required Fields | Cross-Entity Validations |
|--------|------------------------|-----------------|--------------------------|
| SemanticModel | name (manifest-wide) | name, node_relation, entities (at least 1) | - |
| Entity | name (within model) | name, type | At least one primary entity per model |
| Dimension | name (within model) | name, type, expr | Time dimensions need time_granularity |
| Measure | name (within model) | name, agg | agg_time_dimension must reference dimension |
| Metric | name (manifest-wide) | name, type, type_params | Measure references must exist; No circular dependencies |

## Performance Considerations

**In-Memory State**:
- Full manifest kept in memory (Zustand store)
- For large manifests (50+ models), use shallow equality checks
- Memoize derived state (e.g., list of all measures)

**Serialization**:
- JSON.stringify for export (<100ms for 50 models)
- JSON.parse for import (<100ms for 50 models)
- gzip compression for large manifests (optional)

**Validation Performance**:
- Client validation: Synchronous, <10ms per field
- Server validation: Async, <500ms for full manifest
- Database validation: Async, <3s for 20 dimensions/measures
