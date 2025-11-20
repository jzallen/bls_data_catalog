"""Validation service for semantic manifest structure."""
from typing import Any
from ..api.models import ValidationError, ValidationResult, SemanticModel


class ManifestValidator:
    """Validator for semantic manifest structure and business logic."""

    def validate_semantic_model(self, model: SemanticModel) -> ValidationResult:
        """Validate semantic model structure and constraints.

        Args:
            model: Semantic model to validate

        Returns:
            ValidationResult with any errors or warnings
        """
        errors: list[ValidationError] = []

        # Validate entities
        if not model.entities:
            errors.append(ValidationError(
                code="MISSING_ENTITIES",
                message="Semantic model must have at least one entity",
                location=f"semantic_models[{model.name}].entities",
                suggestion="Add at least one entity with type 'primary'"
            ))
        else:
            # Check for at least one primary entity
            primary_entities = [e for e in model.entities if e.type == "primary"]
            if not primary_entities:
                errors.append(ValidationError(
                    code="MISSING_PRIMARY_ENTITY",
                    message="Semantic model must have at least one primary entity",
                    location=f"semantic_models[{model.name}].entities",
                    suggestion="Set one entity type to 'primary'"
                ))

            # Check entity name uniqueness
            entity_names = [e.name for e in model.entities]
            if len(entity_names) != len(set(entity_names)):
                errors.append(ValidationError(
                    code="DUPLICATE_ENTITY_NAMES",
                    message="Entity names must be unique within semantic model",
                    location=f"semantic_models[{model.name}].entities",
                    suggestion="Ensure all entity names are unique"
                ))

        # Validate dimensions
        if model.dimensions:
            dimension_names = [d.name for d in model.dimensions]
            if len(dimension_names) != len(set(dimension_names)):
                errors.append(ValidationError(
                    code="DUPLICATE_DIMENSION_NAMES",
                    message="Dimension names must be unique within semantic model",
                    location=f"semantic_models[{model.name}].dimensions",
                    suggestion="Ensure all dimension names are unique"
                ))

            # Check time dimensions have time_granularity
            for dim in model.dimensions:
                if dim.type == "time" and not dim.type_params:
                    errors.append(ValidationError(
                        code="MISSING_TIME_GRANULARITY",
                        message=f"Time dimension '{dim.name}' missing type_params.time_granularity",
                        location=f"semantic_models[{model.name}].dimensions[{dim.name}]",
                        suggestion="Add type_params with time_granularity (day, week, month, quarter, year)"
                    ))

        # Validate measures
        if model.measures:
            measure_names = [m.name for m in model.measures]
            if len(measure_names) != len(set(measure_names)):
                errors.append(ValidationError(
                    code="DUPLICATE_MEASURE_NAMES",
                    message="Measure names must be unique within semantic model",
                    location=f"semantic_models[{model.name}].measures",
                    suggestion="Ensure all measure names are unique"
                ))

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors
        )

    def validate_manifest(self, manifest: dict[str, Any]) -> ValidationResult:
        """Validate complete manifest structure.

        Args:
            manifest: Full manifest dictionary

        Returns:
            ValidationResult with any errors or warnings
        """
        errors: list[ValidationError] = []

        # Check semantic models
        if "semantic_models" not in manifest:
            errors.append(ValidationError(
                code="MISSING_SEMANTIC_MODELS",
                message="Manifest must contain 'semantic_models' array",
                location="root",
                suggestion="Add semantic_models array to manifest"
            ))
        else:
            # Check semantic model name uniqueness
            model_names = [m.get("name") for m in manifest["semantic_models"]]
            if len(model_names) != len(set(model_names)):
                errors.append(ValidationError(
                    code="DUPLICATE_MODEL_NAMES",
                    message="Semantic model names must be unique across manifest",
                    location="semantic_models",
                    suggestion="Ensure all semantic model names are unique"
                ))

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors
        )
