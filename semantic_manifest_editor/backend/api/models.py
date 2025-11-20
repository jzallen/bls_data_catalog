"""Pydantic models for Semantic Manifest Editor API."""
from datetime import datetime
from typing import Any, Literal, Optional
from uuid import uuid4
from pydantic import BaseModel, Field


# Base Models for Semantic Manifest

class NodeRelation(BaseModel):
    """Database location information for a semantic model."""
    alias: str = Field(..., description="Table/view alias")
    schema_name: str = Field(..., description="Database schema name")
    database: str = Field(..., description="Database name")
    relation_name: Optional[str] = Field(None, description="Full qualified name")


class Entity(BaseModel):
    """Joinable key in a semantic model."""
    name: str = Field(..., description="Unique name within semantic model")
    type: Literal["primary", "foreign", "unique"] = Field(..., description="Entity type")
    expr: Optional[str] = Field(None, description="SQL expression (defaults to name)")
    description: Optional[str] = None
    role: Optional[str] = None
    label: Optional[str] = None


class DimensionTypeParams(BaseModel):
    """Type parameters for time dimensions."""
    time_granularity: Literal["day", "week", "month", "quarter", "year"] = Field(..., description="Time granularity")
    validity_params: Optional[dict[str, Any]] = None


class Dimension(BaseModel):
    """Attribute for grouping or filtering."""
    name: str = Field(..., description="Unique name within semantic model")
    type: Literal["time", "categorical"] = Field(..., description="Dimension type")
    expr: str = Field(..., description="SQL expression")
    description: Optional[str] = None
    type_params: Optional[DimensionTypeParams] = Field(None, description="Required for time dimensions")
    is_partition: Optional[bool] = None
    label: Optional[str] = None


class Measure(BaseModel):
    """Aggregatable metric component."""
    name: str = Field(..., description="Unique name within semantic model")
    agg: Literal["sum", "average", "count", "min", "max", "count_distinct"] = Field(..., description="Aggregation type")
    expr: Optional[str] = Field(None, description="SQL expression (defaults to name)")
    description: Optional[str] = None
    create_metric: Optional[bool] = Field(None, description="Auto-create simple metric")
    agg_time_dimension: Optional[str] = Field(None, description="Specific time dimension for aggregation")
    label: Optional[str] = None


class SemanticModel(BaseModel):
    """Data table or view with semantic layer definition."""
    name: str = Field(..., description="Unique identifier for the semantic model")
    description: Optional[str] = None
    node_relation: NodeRelation = Field(..., description="Database table/view location")
    entities: list[Entity] = Field(default_factory=list, description="At least one entity required")
    dimensions: list[Dimension] = Field(default_factory=list)
    measures: list[Measure] = Field(default_factory=list)
    primary_entity: Optional[str] = Field(None, description="Name of the primary entity")
    label: Optional[str] = None


# Error Response Models

class ValidationError(BaseModel):
    """Error information for validation failures."""
    severity: Literal["error", "warning", "info"] = "error"
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    location: str = Field(..., description="JSON path to error location")
    suggestion: Optional[str] = Field(None, description="Suggested fix")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ValidationResult(BaseModel):
    """Overall validation state."""
    valid: bool
    errors: list[ValidationError] = Field(default_factory=list)
    warnings: list[ValidationError] = Field(default_factory=list)
