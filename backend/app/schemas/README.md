# Pydantic Schemas Documentation

This directory contains Pydantic schemas for the Jal Sathi API. These schemas provide data validation, serialization, and deserialization for all API endpoints.

## Overview

Pydantic schemas serve as the contract between the API and clients, ensuring:
- **Data Validation**: Automatic validation of input data with detailed error messages
- **Type Safety**: Strong typing for all fields with Python type hints
- **Serialization**: Conversion between Python objects and JSON
- **Documentation**: Auto-generated API documentation with examples

## Schema Structure

Each model has three main schema types:

1. **Base Schema**: Common fields shared across create/update operations
2. **Create Schema**: Fields required when creating a new record
3. **Update Schema**: Optional fields for updating existing records
4. **Response Schema**: Fields returned in API responses (includes ID, timestamps)

## Schemas

### Farmer Schemas

Located in `farmer.py`

- **FarmerBase**: Base fields (phone_number, preferred_language, sms_enabled)
- **FarmerCreate**: Create a new farmer account
- **FarmerUpdate**: Update farmer profile (all fields optional)
- **FarmerResponse**: Farmer data in API responses
- **FarmerWithFields**: Farmer with related fields included

**Validation Rules:**
- Phone number: 10 digits (Indian format), optional +91 prefix
- Language: Must be one of: hi, en, mr, gu, pa, ta, te, kn
- SMS enabled: Boolean flag for notifications

**Example:**
```python
from app.schemas import FarmerCreate

farmer = FarmerCreate(
    phone_number="9876543210",
    preferred_language="hi",
    sms_enabled=True
)
```

### Field Schemas

Located in `field.py`

- **FieldBase**: Base field information
- **FieldCreate**: Create a new field
- **FieldUpdate**: Update field details
- **FieldResponse**: Field data in API responses

**Validation Rules:**
- Field size: 0.1 to 50 acres (Requirement 1.5)
- Latitude: 6°N to 38°N (India bounds)
- Longitude: 66°E to 99°E (India bounds)
- Pincode: Exactly 6 digits
- Irrigation method: drip, sprinkler, or flood
- Planting date: Valid date

**Example:**
```python
from app.schemas import FieldCreate
from uuid import uuid4
from datetime import date

field = FieldCreate(
    farmer_id=uuid4(),
    crop_type="wheat",
    field_size_acres=5.5,
    location_lat=28.6139,
    location_lng=77.2090,
    pincode="110001",
    irrigation_method="drip",
    planting_date=date(2024, 1, 15)
)
```

### Recommendation Schemas

Located in `recommendation.py`

- **RecommendationBase**: Base recommendation fields
- **RecommendationCreate**: Create a new recommendation
- **RecommendationUpdate**: Update recommendation
- **RecommendationResponse**: Recommendation in API responses

**Validation Rules:**
- Irrigate: Boolean (yes/no decision)
- Amount: 0-100mm water
- Timing: morning, afternoon, or evening
- Confidence: 0.0-1.0 score
- Weather data: JSON object
- Reasoning: 10-500 characters
- Localized message: 10-500 characters

**Example:**
```python
from app.schemas import RecommendationCreate
from datetime import date

rec = RecommendationCreate(
    field_id=uuid4(),
    date=date(2024, 1, 20),
    irrigate=True,
    amount_mm=25.0,
    timing="evening",
    confidence=0.85,
    weather_data={"temperature": 28.5, "humidity": 65},
    reasoning="Low soil moisture, no rain expected",
    localized_message="Kal shaam 25mm paani dein"
)
```

### IrrigationActivity Schemas

Located in `irrigation_activity.py`

- **IrrigationActivityBase**: Base activity fields
- **IrrigationActivityCreate**: Record irrigation activity
- **IrrigationActivityUpdate**: Update activity
- **IrrigationActivityResponse**: Activity in API responses

**Validation Rules:**
- Date: Valid date
- Amount: 0-200mm water
- Method: drip, sprinkler, or flood
- Farmer reported: Boolean flag
- Cost: Non-negative rupees

**Example:**
```python
from app.schemas import IrrigationActivityCreate

activity = IrrigationActivityCreate(
    field_id=uuid4(),
    date=date(2024, 1, 20),
    amount_mm=25.0,
    method="drip",
    farmer_reported=True,
    cost_rupees=150.0
)
```

### SavingsRecord Schemas

Located in `savings_record.py`

- **SavingsRecordBase**: Base savings fields
- **SavingsRecordCreate**: Create savings record
- **SavingsRecordUpdate**: Update savings record
- **SavingsRecordResponse**: Savings in API responses
- **SavingsSummary**: Aggregated savings summary

**Validation Rules:**
- Period: end_date must be after start_date
- Water saved: Must equal traditional_usage - actual_usage
- Cost rate: ₹2-5 per 1000 liters (Requirement 4.2)
- All amounts: Non-negative

**Example:**
```python
from app.schemas import SavingsRecordCreate

record = SavingsRecordCreate(
    field_id=uuid4(),
    period_start=date(2024, 1, 1),
    period_end=date(2024, 1, 31),
    water_saved_liters=5000.0,
    cost_saved_rupees=15.0,  # ₹3 per 1000L
    traditional_usage_liters=15000.0,
    actual_usage_liters=10000.0
)
```

## Validation Features

### Field-Level Validation

Each field has validators that check:
- Type correctness
- Range constraints
- Format requirements
- Business rules

### Model-Level Validation

Some schemas have cross-field validators:
- **SavingsRecord**: Validates savings calculation consistency
- **SavingsRecord**: Validates cost rate is within ₹2-5/1000L range
- **Field**: Validates coordinates are within India

### Error Messages

Validation errors provide clear, actionable messages:
```python
try:
    field = FieldCreate(field_size_acres=0.05, ...)
except ValidationError as e:
    print(e)
    # Output: "Field size must be at least 0.1 acres"
```

## Serialization

### From ORM Models

Use `from_attributes=True` in model_config:
```python
from app.models import Farmer
from app.schemas import FarmerResponse

db_farmer = db.query(Farmer).first()
farmer_response = FarmerResponse.from_orm(db_farmer)
```

### To JSON

```python
field = FieldCreate(...)
json_str = field.model_dump_json()
```

### To Dictionary

```python
field = FieldCreate(...)
field_dict = field.model_dump()
```

## Testing

Comprehensive unit tests are available in `backend/tests/test_schemas.py`:

```bash
pytest tests/test_schemas.py -v
```

Tests cover:
- Valid data creation
- Validation error cases
- Boundary conditions
- Serialization/deserialization
- All supported values (languages, methods, timings)

## Requirements Mapping

The schemas implement validation for these requirements:

- **Requirement 1.5**: Field size validation (0.1-50 acres)
- **Requirement 4.2**: Cost savings rate validation (₹2-5/1000L)
- **Requirement 7.1**: Data persistence with proper types and constraints

## Usage in FastAPI

```python
from fastapi import APIRouter
from app.schemas import FieldCreate, FieldResponse

router = APIRouter()

@router.post("/fields", response_model=FieldResponse)
async def create_field(field: FieldCreate):
    # field is automatically validated
    # Create database record
    return field_response
```

## Best Practices

1. **Always use schemas for API endpoints**: Never expose ORM models directly
2. **Use appropriate schema type**: Create for POST, Update for PATCH/PUT, Response for GET
3. **Leverage validation**: Let Pydantic handle validation, don't duplicate in business logic
4. **Provide examples**: Use `json_schema_extra` for API documentation
5. **Keep schemas focused**: One schema per use case (create, update, response)

## Future Enhancements

Potential improvements:
- Add computed fields for derived values
- Implement custom validators for complex business rules
- Add schema versioning for API evolution
- Create specialized schemas for different user roles
