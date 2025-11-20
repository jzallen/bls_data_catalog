/**
 * TypeScript types for Semantic Manifest Editor
 * Mirrors backend Pydantic models
 */

export type EntityType = 'primary' | 'foreign' | 'unique';
export type DimensionType = 'time' | 'categorical';
export type TimeGranularity = 'day' | 'week' | 'month' | 'quarter' | 'year';
export type AggregationType = 'sum' | 'average' | 'count' | 'min' | 'max' | 'count_distinct';

export interface NodeRelation {
  alias: string;
  schema_name: string;
  database: string;
  relation_name?: string;
}

export interface Entity {
  name: string;
  type: EntityType;
  expr?: string;
  description?: string;
  role?: string;
  label?: string;
}

export interface DimensionTypeParams {
  time_granularity: TimeGranularity;
  validity_params?: Record<string, any>;
}

export interface Dimension {
  name: string;
  type: DimensionType;
  expr: string;
  description?: string;
  type_params?: DimensionTypeParams;
  is_partition?: boolean;
  label?: string;
}

export interface Measure {
  name: string;
  agg: AggregationType;
  expr?: string;
  description?: string;
  create_metric?: boolean;
  agg_time_dimension?: string;
  label?: string;
}

export interface SemanticModel {
  name: string;
  description?: string;
  node_relation: NodeRelation;
  entities: Entity[];
  dimensions: Dimension[];
  measures: Measure[];
  primary_entity?: string;
  label?: string;
}

export type ErrorSeverity = 'error' | 'warning' | 'info';

export interface ValidationError {
  severity: ErrorSeverity;
  code: string;
  message: string;
  location: string;
  suggestion?: string;
  timestamp: string;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationError[];
}
