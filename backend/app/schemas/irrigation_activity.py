"""Pydantic schemas for IrrigationActivity model."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from uuid import UUID
from typing import Optional


class IrrigationActivityBase(BaseModel):
    """Base schema for IrrigationActivity with common fields."""
    date: date = Field(
        ...,
        description="Date when irrigation was performed",
        examples=["2024-01-20"]
    )
    amount_mm: float = Field(
        ...,
        ge=0.0,
        le=200.0,
        description="Amount of water applied in millimeters (0-200mm)",
        examples=[25.0, 30.5]
    )
    method: str = Field(
        ...,
        description="Irrigation method used (drip, sprinkler, flood)",
        examples=["drip", "sprinkler"]
    )
    farmer_reported: bool = Field(
        default=False,
        description="Whether this activity was reported by the farmer"
    )
    cost_rupees: float = Field(
        ...,
        ge=0.0,
        description="Cost of irrigation in rupees",
        examples=[150.0, 200.5]
    )

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: str) -> str:
        """Validate irrigation method is supported."""
        valid_methods = {"drip", "sprinkler", "flood"}
        if v.lower() not in valid_methods:
            raise ValueError(
                f"Irrigation method must be one of: {', '.join(valid_methods)}"
            )
        return v.lower()

    @field_validator("amount_mm")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        """Validate water amount is reasonable."""
        if v < 0.0:
            raise ValueError("Water amount cannot be negative")
        if v > 200.0:
            raise ValueError("Water amount exceeds reasonable maximum (200mm)")
        return v

    @field_validator("cost_rupees")
    @classmethod
    def validate_cost(cls, v: float) -> float:
        """Validate cost is non-negative."""
        if v < 0.0:
            raise ValueError("Cost cannot be negative")
        return v


class IrrigationActivityCreate(IrrigationActivityBase):
    """Schema for creating a new IrrigationActivity."""
    field_id: UUID = Field(..., description="ID of the field where irrigation was performed")


class IrrigationActivityUpdate(BaseModel):
    """Schema for updating an existing IrrigationActivity."""
    date: Optional[date] = Field(None, description="Irrigation date")
    amount_mm: Optional[float] = Field(
        None,
        ge=0.0,
        le=200.0,
        description="Water amount in millimeters"
    )
    method: Optional[str] = Field(None, description="Irrigation method")
    farmer_reported: Optional[bool] = Field(
        None,
        description="Whether farmer reported"
    )
    cost_rupees: Optional[float] = Field(
        None,
        ge=0.0,
        description="Cost in rupees"
    )

    @field_validator("method")
    @classmethod
    def validate_method(cls, v: Optional[str]) -> Optional[str]:
        """Validate irrigation method if provided."""
        if v is not None:
            valid_methods = {"drip", "sprinkler", "flood"}
            if v.lower() not in valid_methods:
                raise ValueError(
                    f"Irrigation method must be one of: {', '.join(valid_methods)}"
                )
            return v.lower()
        return v

    @field_validator("amount_mm")
    @classmethod
    def validate_amount(cls, v: Optional[float]) -> Optional[float]:
        """Validate water amount if provided."""
        if v is not None:
            if v < 0.0 or v > 200.0:
                raise ValueError("Water amount must be between 0 and 200mm")
        return v

    @field_validator("cost_rupees")
    @classmethod
    def validate_cost(cls, v: Optional[float]) -> Optional[float]:
        """Validate cost if provided."""
        if v is not None:
            if v < 0.0:
                raise ValueError("Cost cannot be negative")
        return v


class IrrigationActivityResponse(IrrigationActivityBase):
    """Schema for IrrigationActivity responses."""
    id: UUID = Field(..., description="Unique irrigation activity identifier")
    field_id: UUID = Field(..., description="ID of the field where irrigation was performed")
    created_at: datetime = Field(..., description="Activity creation timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174003",
                "field_id": "123e4567-e89b-12d3-a456-426614174001",
                "date": "2024-01-20",
                "amount_mm": 25.0,
                "method": "drip",
                "farmer_reported": True,
                "cost_rupees": 150.0,
                "created_at": "2024-01-20T18:30:00Z"
            }
        }
    }
