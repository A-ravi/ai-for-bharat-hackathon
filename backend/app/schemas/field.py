"""Pydantic schemas for Field model."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from uuid import UUID
from typing import Optional


class FieldBase(BaseModel):
    """Base schema for Field with common fields."""
    crop_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Type of crop being grown",
        examples=["wheat", "rice", "cotton", "sugarcane"]
    )
    field_size_acres: float = Field(
        ...,
        gt=0.1,
        le=50.0,
        description="Field size in acres (0.1 to 50)",
        examples=[2.5, 10.0, 15.5]
    )
    location_lat: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Latitude coordinate",
        examples=[28.6139, 19.0760]
    )
    location_lng: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Longitude coordinate",
        examples=[77.2090, 72.8777]
    )
    pincode: str = Field(
        ...,
        min_length=6,
        max_length=10,
        description="Postal code for the field location",
        examples=["110001", "400001"]
    )
    irrigation_method: str = Field(
        ...,
        description="Irrigation method used (drip, sprinkler, flood)",
        examples=["drip", "sprinkler", "flood"]
    )
    planting_date: date = Field(
        ...,
        description="Date when the crop was planted",
        examples=["2024-01-15"]
    )

    @field_validator("field_size_acres")
    @classmethod
    def validate_field_size(cls, v: float) -> float:
        """Validate field size is within acceptable range (Requirement 1.5)."""
        if v < 0.1:
            raise ValueError("Field size must be at least 0.1 acres")
        if v > 50.0:
            raise ValueError("Field size must not exceed 50 acres")
        return v

    @field_validator("irrigation_method")
    @classmethod
    def validate_irrigation_method(cls, v: str) -> str:
        """Validate irrigation method is supported."""
        valid_methods = {"drip", "sprinkler", "flood"}
        if v.lower() not in valid_methods:
            raise ValueError(
                f"Irrigation method must be one of: {', '.join(valid_methods)}"
            )
        return v.lower()

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, v: str) -> str:
        """Validate pincode format."""
        cleaned = v.replace(" ", "").replace("-", "")
        if not cleaned.isdigit():
            raise ValueError("Pincode must contain only digits")
        if len(cleaned) != 6:
            raise ValueError("Indian pincode must be exactly 6 digits")
        return cleaned

    @field_validator("location_lat")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        """Validate latitude is within India's approximate bounds."""
        # India's latitude range: approximately 8°N to 37°N
        if v < 6.0 or v > 38.0:
            raise ValueError(
                "Latitude must be within India's approximate bounds (6°N to 38°N)"
            )
        return v

    @field_validator("location_lng")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        """Validate longitude is within India's approximate bounds."""
        # India's longitude range: approximately 68°E to 97°E
        if v < 66.0 or v > 99.0:
            raise ValueError(
                "Longitude must be within India's approximate bounds (66°E to 99°E)"
            )
        return v


class FieldCreate(FieldBase):
    """Schema for creating a new Field."""
    farmer_id: UUID = Field(..., description="ID of the farmer who owns this field")


class FieldUpdate(BaseModel):
    """Schema for updating an existing Field."""
    crop_type: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        description="Type of crop being grown"
    )
    field_size_acres: Optional[float] = Field(
        None,
        gt=0.1,
        le=50.0,
        description="Field size in acres"
    )
    location_lat: Optional[float] = Field(
        None,
        ge=-90.0,
        le=90.0,
        description="Latitude coordinate"
    )
    location_lng: Optional[float] = Field(
        None,
        ge=-180.0,
        le=180.0,
        description="Longitude coordinate"
    )
    pincode: Optional[str] = Field(
        None,
        min_length=6,
        max_length=10,
        description="Postal code"
    )
    irrigation_method: Optional[str] = Field(
        None,
        description="Irrigation method"
    )
    planting_date: Optional[date] = Field(
        None,
        description="Planting date"
    )

    @field_validator("field_size_acres")
    @classmethod
    def validate_field_size(cls, v: Optional[float]) -> Optional[float]:
        """Validate field size if provided."""
        if v is not None:
            if v < 0.1 or v > 50.0:
                raise ValueError("Field size must be between 0.1 and 50 acres")
        return v

    @field_validator("irrigation_method")
    @classmethod
    def validate_irrigation_method(cls, v: Optional[str]) -> Optional[str]:
        """Validate irrigation method if provided."""
        if v is not None:
            valid_methods = {"drip", "sprinkler", "flood"}
            if v.lower() not in valid_methods:
                raise ValueError(
                    f"Irrigation method must be one of: {', '.join(valid_methods)}"
                )
            return v.lower()
        return v

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, v: Optional[str]) -> Optional[str]:
        """Validate pincode if provided."""
        if v is not None:
            cleaned = v.replace(" ", "").replace("-", "")
            if not cleaned.isdigit() or len(cleaned) != 6:
                raise ValueError("Indian pincode must be exactly 6 digits")
            return cleaned
        return v


class FieldResponse(FieldBase):
    """Schema for Field responses."""
    id: UUID = Field(..., description="Unique field identifier")
    farmer_id: UUID = Field(..., description="ID of the farmer who owns this field")
    created_at: datetime = Field(..., description="Field creation timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "farmer_id": "123e4567-e89b-12d3-a456-426614174000",
                "crop_type": "wheat",
                "field_size_acres": 5.5,
                "location_lat": 28.6139,
                "location_lng": 77.2090,
                "pincode": "110001",
                "irrigation_method": "drip",
                "planting_date": "2024-01-15",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    }
