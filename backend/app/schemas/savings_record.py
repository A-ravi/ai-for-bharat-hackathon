"""Pydantic schemas for SavingsRecord model."""
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime, date
from uuid import UUID
from typing import Optional


class SavingsRecordBase(BaseModel):
    """Base schema for SavingsRecord with common fields."""
    period_start: date = Field(
        ...,
        description="Start date of the savings calculation period",
        examples=["2024-01-01"]
    )
    period_end: date = Field(
        ...,
        description="End date of the savings calculation period",
        examples=["2024-01-31"]
    )
    water_saved_liters: float = Field(
        ...,
        ge=0.0,
        description="Amount of water saved in liters",
        examples=[5000.0, 12500.0]
    )
    cost_saved_rupees: float = Field(
        ...,
        ge=0.0,
        description="Cost saved in rupees (₹2-5 per 1000 liters)",
        examples=[25.0, 62.5]
    )
    traditional_usage_liters: float = Field(
        ...,
        ge=0.0,
        description="Estimated traditional water usage in liters",
        examples=[15000.0, 25000.0]
    )
    actual_usage_liters: float = Field(
        ...,
        ge=0.0,
        description="Actual water usage with Jal Sathi in liters",
        examples=[10000.0, 12500.0]
    )

    @model_validator(mode="after")
    def validate_period(self):
        """Validate that period_end is after period_start."""
        if self.period_end <= self.period_start:
            raise ValueError("period_end must be after period_start")
        return self

    @model_validator(mode="after")
    def validate_savings_calculation(self):
        """Validate that savings calculation is consistent."""
        expected_savings = self.traditional_usage_liters - self.actual_usage_liters
        
        # Allow for small floating point differences
        if abs(expected_savings - self.water_saved_liters) > 0.01:
            raise ValueError(
                f"water_saved_liters ({self.water_saved_liters}) must equal "
                f"traditional_usage_liters ({self.traditional_usage_liters}) - "
                f"actual_usage_liters ({self.actual_usage_liters})"
            )
        
        return self

    @model_validator(mode="after")
    def validate_cost_calculation(self):
        """Validate that cost savings are within expected range (₹2-5 per 1000L)."""
        if self.water_saved_liters > 0:
            # Calculate cost per 1000 liters
            cost_per_1000L = (self.cost_saved_rupees / self.water_saved_liters) * 1000
            
            # Allow for reasonable range (₹2-5 per 1000 liters as per requirements)
            if cost_per_1000L < 2.0 or cost_per_1000L > 5.0:
                raise ValueError(
                    f"Cost savings rate ({cost_per_1000L:.2f} ₹/1000L) must be "
                    f"between ₹2 and ₹5 per 1000 liters (Requirement 4.2)"
                )
        
        return self

    @field_validator("water_saved_liters", "traditional_usage_liters", "actual_usage_liters")
    @classmethod
    def validate_water_amounts(cls, v: float) -> float:
        """Validate water amounts are non-negative."""
        if v < 0.0:
            raise ValueError("Water amounts cannot be negative")
        return v

    @field_validator("cost_saved_rupees")
    @classmethod
    def validate_cost(cls, v: float) -> float:
        """Validate cost is non-negative."""
        if v < 0.0:
            raise ValueError("Cost cannot be negative")
        return v


class SavingsRecordCreate(SavingsRecordBase):
    """Schema for creating a new SavingsRecord."""
    field_id: UUID = Field(..., description="ID of the field for this savings record")


class SavingsRecordUpdate(BaseModel):
    """Schema for updating an existing SavingsRecord."""
    period_start: Optional[date] = Field(None, description="Period start date")
    period_end: Optional[date] = Field(None, description="Period end date")
    water_saved_liters: Optional[float] = Field(
        None,
        ge=0.0,
        description="Water saved in liters"
    )
    cost_saved_rupees: Optional[float] = Field(
        None,
        ge=0.0,
        description="Cost saved in rupees"
    )
    traditional_usage_liters: Optional[float] = Field(
        None,
        ge=0.0,
        description="Traditional usage in liters"
    )
    actual_usage_liters: Optional[float] = Field(
        None,
        ge=0.0,
        description="Actual usage in liters"
    )

    @field_validator("water_saved_liters", "traditional_usage_liters", "actual_usage_liters")
    @classmethod
    def validate_water_amounts(cls, v: Optional[float]) -> Optional[float]:
        """Validate water amounts if provided."""
        if v is not None and v < 0.0:
            raise ValueError("Water amounts cannot be negative")
        return v

    @field_validator("cost_saved_rupees")
    @classmethod
    def validate_cost(cls, v: Optional[float]) -> Optional[float]:
        """Validate cost if provided."""
        if v is not None and v < 0.0:
            raise ValueError("Cost cannot be negative")
        return v


class SavingsRecordResponse(SavingsRecordBase):
    """Schema for SavingsRecord responses."""
    id: UUID = Field(..., description="Unique savings record identifier")
    field_id: UUID = Field(..., description="ID of the field for this savings record")
    calculated_at: datetime = Field(..., description="Calculation timestamp")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174004",
                "field_id": "123e4567-e89b-12d3-a456-426614174001",
                "period_start": "2024-01-01",
                "period_end": "2024-01-31",
                "water_saved_liters": 5000.0,
                "cost_saved_rupees": 15.0,
                "traditional_usage_liters": 15000.0,
                "actual_usage_liters": 10000.0,
                "calculated_at": "2024-02-01T00:00:00Z"
            }
        }
    }


class SavingsSummary(BaseModel):
    """Schema for aggregated savings summary."""
    total_water_saved_liters: float = Field(
        ...,
        description="Total water saved across all periods"
    )
    total_cost_saved_rupees: float = Field(
        ...,
        description="Total cost saved across all periods"
    )
    average_savings_percentage: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Average percentage of water saved"
    )
    number_of_periods: int = Field(
        ...,
        ge=0,
        description="Number of calculation periods"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_water_saved_liters": 15000.0,
                "total_cost_saved_rupees": 45.0,
                "average_savings_percentage": 33.3,
                "number_of_periods": 3
            }
        }
    }
