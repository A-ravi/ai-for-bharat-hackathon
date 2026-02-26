"""Pydantic schemas for Recommendation model."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from uuid import UUID
from typing import Optional, Dict, Any


class RecommendationBase(BaseModel):
    """Base schema for Recommendation with common fields."""
    date: date = Field(
        ...,
        description="Date for which the recommendation is made",
        examples=["2024-01-20"]
    )
    irrigate: bool = Field(
        ...,
        description="Whether irrigation is recommended (yes/no)"
    )
    amount_mm: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Recommended water amount in millimeters (0-100mm)",
        examples=[25.0, 30.5, 0.0]
    )
    timing: str = Field(
        ...,
        description="Optimal irrigation timing (morning, afternoon, evening)",
        examples=["morning", "evening"]
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the recommendation (0.0-1.0)",
        examples=[0.85, 0.92]
    )
    weather_data: Dict[str, Any] = Field(
        ...,
        description="Weather data used for the recommendation"
    )
    reasoning: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Explanation for the recommendation",
        examples=["Low soil moisture, no rain expected for 3 days"]
    )
    localized_message: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Recommendation message in farmer's preferred language",
        examples=["Kal shaam 25mm paani dein"]
    )

    @field_validator("timing")
    @classmethod
    def validate_timing(cls, v: str) -> str:
        """Validate timing is one of the supported values."""
        valid_timings = {"morning", "afternoon", "evening"}
        if v.lower() not in valid_timings:
            raise ValueError(
                f"Timing must be one of: {', '.join(valid_timings)}"
            )
        return v.lower()

    @field_validator("amount_mm")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        """Validate water amount is reasonable."""
        if v < 0.0:
            raise ValueError("Water amount cannot be negative")
        if v > 100.0:
            raise ValueError("Water amount exceeds reasonable maximum (100mm)")
        return v

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Validate confidence score is between 0 and 1."""
        if v < 0.0 or v > 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class RecommendationCreate(RecommendationBase):
    """Schema for creating a new Recommendation."""
    field_id: UUID = Field(..., description="ID of the field for this recommendation")


class RecommendationUpdate(BaseModel):
    """Schema for updating an existing Recommendation."""
    date: Optional[date] = Field(None, description="Recommendation date")
    irrigate: Optional[bool] = Field(None, description="Irrigation decision")
    amount_mm: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Water amount in millimeters"
    )
    timing: Optional[str] = Field(None, description="Irrigation timing")
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence score"
    )
    weather_data: Optional[Dict[str, Any]] = Field(None, description="Weather data")
    reasoning: Optional[str] = Field(
        None,
        min_length=10,
        max_length=500,
        description="Reasoning"
    )
    localized_message: Optional[str] = Field(
        None,
        min_length=10,
        max_length=500,
        description="Localized message"
    )

    @field_validator("timing")
    @classmethod
    def validate_timing(cls, v: Optional[str]) -> Optional[str]:
        """Validate timing if provided."""
        if v is not None:
            valid_timings = {"morning", "afternoon", "evening"}
            if v.lower() not in valid_timings:
                raise ValueError(
                    f"Timing must be one of: {', '.join(valid_timings)}"
                )
            return v.lower()
        return v

    @field_validator("amount_mm")
    @classmethod
    def validate_amount(cls, v: Optional[float]) -> Optional[float]:
        """Validate water amount if provided."""
        if v is not None:
            if v < 0.0 or v > 100.0:
                raise ValueError("Water amount must be between 0 and 100mm")
        return v

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: Optional[float]) -> Optional[float]:
        """Validate confidence if provided."""
        if v is not None:
            if v < 0.0 or v > 1.0:
                raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class RecommendationResponse(RecommendationBase):
    """Schema for Recommendation responses."""
    id: UUID = Field(..., description="Unique recommendation identifier")
    field_id: UUID = Field(..., description="ID of the field for this recommendation")
    created_at: datetime = Field(..., description="Recommendation creation timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "field_id": "123e4567-e89b-12d3-a456-426614174001",
                "date": "2024-01-20",
                "irrigate": True,
                "amount_mm": 25.0,
                "timing": "evening",
                "confidence": 0.85,
                "weather_data": {
                    "temperature": 28.5,
                    "humidity": 65,
                    "rainfall_probability": 10
                },
                "reasoning": "Low soil moisture, no rain expected for 3 days",
                "localized_message": "Kal shaam 25mm paani dein",
                "created_at": "2024-01-20T06:00:00Z"
            }
        }
    }
