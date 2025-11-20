"""Routes for semantic models CRUD operations."""
from typing import List
from fastapi import APIRouter, HTTPException
from ..models import SemanticModel, Entity, Dimension, Measure, ValidationResult
from ...services.validator import ManifestValidator

router = APIRouter(prefix="/semantic-models", tags=["semantic-models"])

# In-memory storage for MVP (will be replaced with database)
_semantic_models: dict[str, SemanticModel] = {}

validator = ManifestValidator()


@router.post("", response_model=SemanticModel, status_code=201)
async def create_semantic_model(model: SemanticModel):
    """Create a new semantic model (T026)."""
    # Validate model
    validation_result = validator.validate_semantic_model(model)
    if not validation_result.valid:
        raise HTTPException(
            status_code=400,
            detail={"errors": [e.dict() for e in validation_result.errors]}
        )

    # Check for duplicate name
    if model.name in _semantic_models:
        raise HTTPException(
            status_code=409,
            detail=f"Semantic model with name '{model.name}' already exists"
        )

    _semantic_models[model.name] = model
    return model


@router.get("", response_model=List[SemanticModel])
async def list_semantic_models():
    """List all semantic models (T027)."""
    return list(_semantic_models.values())


@router.get("/{model_id}", response_model=SemanticModel)
async def get_semantic_model(model_id: str):
    """Get a specific semantic model (T028)."""
    if model_id not in _semantic_models:
        raise HTTPException(status_code=404, detail=f"Semantic model '{model_id}' not found")
    return _semantic_models[model_id]


@router.put("/{model_id}", response_model=SemanticModel)
async def update_semantic_model(model_id: str, model: SemanticModel):
    """Update an existing semantic model (T029)."""
    if model_id not in _semantic_models:
        raise HTTPException(status_code=404, detail=f"Semantic model '{model_id}' not found")

    # Validate model
    validation_result = validator.validate_semantic_model(model)
    if not validation_result.valid:
        raise HTTPException(
            status_code=400,
            detail={"errors": [e.dict() for e in validation_result.errors]}
        )

    # If name changed, check for duplicates
    if model.name != model_id and model.name in _semantic_models:
        raise HTTPException(
            status_code=409,
            detail=f"Semantic model with name '{model.name}' already exists"
        )

    # Remove old entry if name changed
    if model.name != model_id:
        del _semantic_models[model_id]

    _semantic_models[model.name] = model
    return model


@router.delete("/{model_id}", status_code=204)
async def delete_semantic_model(model_id: str):
    """Delete a semantic model (T030)."""
    if model_id not in _semantic_models:
        raise HTTPException(status_code=404, detail=f"Semantic model '{model_id}' not found")
    del _semantic_models[model_id]


@router.post("/{model_id}/entities", response_model=Entity, status_code=201)
async def add_entity(model_id: str, entity: Entity):
    """Add an entity to a semantic model (T031)."""
    if model_id not in _semantic_models:
        raise HTTPException(status_code=404, detail=f"Semantic model '{model_id}' not found")

    model = _semantic_models[model_id]

    # Check for duplicate entity name
    if any(e.name == entity.name for e in model.entities):
        raise HTTPException(
            status_code=409,
            detail=f"Entity with name '{entity.name}' already exists in model"
        )

    model.entities.append(entity)
    return entity


@router.post("/{model_id}/dimensions", response_model=Dimension, status_code=201)
async def add_dimension(model_id: str, dimension: Dimension):
    """Add a dimension to a semantic model (T032)."""
    if model_id not in _semantic_models:
        raise HTTPException(status_code=404, detail=f"Semantic model '{model_id}' not found")

    model = _semantic_models[model_id]

    # Check for duplicate dimension name
    if any(d.name == dimension.name for d in model.dimensions):
        raise HTTPException(
            status_code=409,
            detail=f"Dimension with name '{dimension.name}' already exists in model"
        )

    model.dimensions.append(dimension)
    return dimension


@router.post("/{model_id}/measures", response_model=Measure, status_code=201)
async def add_measure(model_id: str, measure: Measure):
    """Add a measure to a semantic model (T033)."""
    if model_id not in _semantic_models:
        raise HTTPException(status_code=404, detail=f"Semantic model '{model_id}' not found")

    model = _semantic_models[model_id]

    # Check for duplicate measure name
    if any(m.name == measure.name for m in model.measures):
        raise HTTPException(
            status_code=409,
            detail=f"Measure with name '{measure.name}' already exists in model"
        )

    model.measures.append(measure)
    return measure
