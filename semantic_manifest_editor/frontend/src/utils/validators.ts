/**
 * Client-side validation utilities
 */
import type { SemanticModel, Entity, Dimension, Measure, ValidationError } from '../types/manifest';

export class ClientValidator {
  /**
   * Validate semantic model on client side for immediate feedback
   */
  static validateSemanticModel(model: Partial<SemanticModel>): ValidationError[] {
    const errors: ValidationError[] = [];

    // Name validation
    if (!model.name || model.name.trim() === '') {
      errors.push({
        severity: 'error',
        code: 'MISSING_NAME',
        message: 'Semantic model name is required',
        location: 'name',
        suggestion: 'Enter a unique name for this semantic model',
        timestamp: new Date().toISOString(),
      });
    }

    // Node relation validation
    if (!model.node_relation) {
      errors.push({
        severity: 'error',
        code: 'MISSING_NODE_RELATION',
        message: 'Node relation is required',
        location: 'node_relation',
        suggestion: 'Specify the database table location',
        timestamp: new Date().toISOString(),
      });
    } else {
      if (!model.node_relation.alias) {
        errors.push({
          severity: 'error',
          code: 'MISSING_ALIAS',
          message: 'Table alias is required',
          location: 'node_relation.alias',
          timestamp: new Date().toISOString(),
        });
      }
      if (!model.node_relation.schema_name) {
        errors.push({
          severity: 'error',
          code: 'MISSING_SCHEMA',
          message: 'Schema name is required',
          location: 'node_relation.schema_name',
          timestamp: new Date().toISOString(),
        });
      }
      if (!model.node_relation.database) {
        errors.push({
          severity: 'error',
          code: 'MISSING_DATABASE',
          message: 'Database name is required',
          location: 'node_relation.database',
          timestamp: new Date().toISOString(),
        });
      }
    }

    // Entities validation
    if (!model.entities || model.entities.length === 0) {
      errors.push({
        severity: 'error',
        code: 'MISSING_ENTITIES',
        message: 'At least one entity is required',
        location: 'entities',
        suggestion: 'Add a primary entity',
        timestamp: new Date().toISOString(),
      });
    } else {
      const hasPrimary = model.entities.some(e => e.type === 'primary');
      if (!hasPrimary) {
        errors.push({
          severity: 'error',
          code: 'MISSING_PRIMARY_ENTITY',
          message: 'At least one primary entity is required',
          location: 'entities',
          suggestion: 'Set one entity type to primary',
          timestamp: new Date().toISOString(),
        });
      }
    }

    return errors;
  }

  /**
   * Validate entity
   */
  static validateEntity(entity: Partial<Entity>): ValidationError[] {
    const errors: ValidationError[] = [];

    if (!entity.name || entity.name.trim() === '') {
      errors.push({
        severity: 'error',
        code: 'MISSING_ENTITY_NAME',
        message: 'Entity name is required',
        location: 'name',
        timestamp: new Date().toISOString(),
      });
    }

    if (!entity.type) {
      errors.push({
        severity: 'error',
        code: 'MISSING_ENTITY_TYPE',
        message: 'Entity type is required',
        location: 'type',
        suggestion: 'Select primary, foreign, or unique',
        timestamp: new Date().toISOString(),
      });
    }

    return errors;
  }

  /**
   * Validate dimension
   */
  static validateDimension(dimension: Partial<Dimension>): ValidationError[] {
    const errors: ValidationError[] = [];

    if (!dimension.name || dimension.name.trim() === '') {
      errors.push({
        severity: 'error',
        code: 'MISSING_DIMENSION_NAME',
        message: 'Dimension name is required',
        location: 'name',
        timestamp: new Date().toISOString(),
      });
    }

    if (!dimension.type) {
      errors.push({
        severity: 'error',
        code: 'MISSING_DIMENSION_TYPE',
        message: 'Dimension type is required',
        location: 'type',
        timestamp: new Date().toISOString(),
      });
    }

    if (!dimension.expr || dimension.expr.trim() === '') {
      errors.push({
        severity: 'error',
        code: 'MISSING_DIMENSION_EXPR',
        message: 'Dimension expression is required',
        location: 'expr',
        timestamp: new Date().toISOString(),
      });
    }

    if (dimension.type === 'time' && !dimension.type_params?.time_granularity) {
      errors.push({
        severity: 'error',
        code: 'MISSING_TIME_GRANULARITY',
        message: 'Time dimensions require time_granularity',
        location: 'type_params.time_granularity',
        suggestion: 'Select day, week, month, quarter, or year',
        timestamp: new Date().toISOString(),
      });
    }

    return errors;
  }

  /**
   * Validate measure
   */
  static validateMeasure(measure: Partial<Measure>): ValidationError[] {
    const errors: ValidationError[] = [];

    if (!measure.name || measure.name.trim() === '') {
      errors.push({
        severity: 'error',
        code: 'MISSING_MEASURE_NAME',
        message: 'Measure name is required',
        location: 'name',
        timestamp: new Date().toISOString(),
      });
    }

    if (!measure.agg) {
      errors.push({
        severity: 'error',
        code: 'MISSING_AGGREGATION',
        message: 'Aggregation type is required',
        location: 'agg',
        suggestion: 'Select sum, count, average, min, max, or count_distinct',
        timestamp: new Date().toISOString(),
      });
    }

    return errors;
  }
}
