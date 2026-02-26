"""Pydantic schemas for Farmer model."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from uuid import UUID
from typing import Optional


class FarmerBase(BaseModel):
    """Base schema for Farmer with common fields."""
    phone_number: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Farmer's phone number (10-15 digits)",
        examples=["+919876543210", "9876543210"]
    )
    preferred_language: str = Field(
        default="en",
        min_length=2,
        max_length=10,
        description="Preferred language code (hi, en, mr, gu, pa, ta, te, kn)",
        examples=["hi", "en", "mr"]
    )
    sms_enabled: bool = Field(
        default=True,
        description="Whether SMS notifications are enabled"
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: str) -> str:
        """Validate phone number format."""
        # Remove common prefixes and spaces
        cleaned = v.replace("+91", "").replace("-", "").replace(" ", "")
        
        # Check if it contains only digits
        if not cleaned.isdigit():
            raise ValueError("Phone number must contain only digits (with optional +91 prefix)")
        
        # Check length (Indian phone numbers are 10 digits)
        if len(cleaned) != 10:
            raise ValueError("Phone number must be exactly 10 digits (excluding country code)")
        
        return v

    @field_validator("preferred_language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        """Validate language code is supported."""
        supported_languages = {"hi", "en", "mr", "gu", "pa", "ta", "te", "kn"}
        if v not in supported_languages:
            raise ValueError(
                f"Language must be one of: {', '.join(supported_languages)}"
            )
        return v


class FarmerCreate(FarmerBase):
    """Schema for creating a new Farmer."""
    pass


class FarmerUpdate(BaseModel):
    """Schema for updating an existing Farmer."""
    phone_number: Optional[str] = Field(
        None,
        min_length=10,
        max_length=15,
        description="Farmer's phone number"
    )
    preferred_language: Optional[str] = Field(
        None,
        min_length=2,
        max_length=10,
        description="Preferred language code"
    )
    sms_enabled: Optional[bool] = Field(
        None,
        description="Whether SMS notifications are enabled"
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format if provided."""
        if v is None:
            return v
        
        cleaned = v.replace("+91", "").replace("-", "").replace(" ", "")
        
        if not cleaned.isdigit():
            raise ValueError("Phone number must contain only digits (with optional +91 prefix)")
        
        if len(cleaned) != 10:
            raise ValueError("Phone number must be exactly 10 digits (excluding country code)")
        
        return v

    @field_validator("preferred_language")
    @classmethod
    def validate_language(cls, v: Optional[str]) -> Optional[str]:
        """Validate language code if provided."""
        if v is None:
            return v
        
        supported_languages = {"hi", "en", "mr", "gu", "pa", "ta", "te", "kn"}
        if v not in supported_languages:
            raise ValueError(
                f"Language must be one of: {', '.join(supported_languages)}"
            )
        return v


class FarmerResponse(FarmerBase):
    """Schema for Farmer responses."""
    id: UUID = Field(..., description="Unique farmer identifier")
    created_at: datetime = Field(..., description="Account creation timestamp")
    last_active: datetime = Field(..., description="Last activity timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "phone_number": "+919876543210",
                "preferred_language": "hi",
                "sms_enabled": True,
                "created_at": "2024-01-15T10:30:00Z",
                "last_active": "2024-01-20T08:15:00Z"
            }
        }
    }


class FarmerWithFields(FarmerResponse):
    """Schema for Farmer with related fields."""
    from app.schemas.field import FieldResponse
    from typing import List
    
    fields: List["FieldResponse"] = Field(
        default_factory=list,
        description="List of fields owned by the farmer"
    )
