"""Pydantic schemas for Jal Sathi API."""
from app.schemas.farmer import (
    FarmerBase,
    FarmerCreate,
    FarmerUpdate,
    FarmerResponse,
    FarmerWithFields,
)
from app.schemas.field import (
    FieldBase,
    FieldCreate,
    FieldUpdate,
    FieldResponse,
)
from app.schemas.recommendation import (
    RecommendationBase,
    RecommendationCreate,
    RecommendationUpdate,
    RecommendationResponse,
)
from app.schemas.irrigation_activity import (
    IrrigationActivityBase,
    IrrigationActivityCreate,
    IrrigationActivityUpdate,
    IrrigationActivityResponse,
)
from app.schemas.savings_record import (
    SavingsRecordBase,
    SavingsRecordCreate,
    SavingsRecordUpdate,
    SavingsRecordResponse,
    SavingsSummary,
)

__all__ = [
    # Farmer schemas
    "FarmerBase",
    "FarmerCreate",
    "FarmerUpdate",
    "FarmerResponse",
    "FarmerWithFields",
    # Field schemas
    "FieldBase",
    "FieldCreate",
    "FieldUpdate",
    "FieldResponse",
    # Recommendation schemas
    "RecommendationBase",
    "RecommendationCreate",
    "RecommendationUpdate",
    "RecommendationResponse",
    # IrrigationActivity schemas
    "IrrigationActivityBase",
    "IrrigationActivityCreate",
    "IrrigationActivityUpdate",
    "IrrigationActivityResponse",
    # SavingsRecord schemas
    "SavingsRecordBase",
    "SavingsRecordCreate",
    "SavingsRecordUpdate",
    "SavingsRecordResponse",
    "SavingsSummary",
]
