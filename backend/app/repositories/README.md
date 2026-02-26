# Repository Layer

This directory contains the repository pattern implementation for Jal Sathi's database operations. The repository layer provides a clean abstraction over database access with CRUD operations, transaction management, and comprehensive error handling.

## Architecture

The repository layer follows these design principles:

1. **Repository Pattern**: Each model has a dedicated repository class
2. **Base Repository**: Common CRUD operations in a generic base class
3. **Transaction Management**: Automatic commit/rollback handling
4. **Error Handling**: Custom exceptions and comprehensive logging
5. **Type Safety**: Generic types for compile-time type checking

## Components

### Base Repository (`base.py`)

The `BaseRepository` class provides generic CRUD operations for all models:

- `create(obj)` - Create a new entity
- `get_by_id(id)` - Retrieve entity by UUID
- `get_all(skip, limit)` - List entities with pagination
- `update(id, data)` - Update entity fields
- `delete(id)` - Delete entity by UUID
- `exists(id)` - Check if entity exists
- `count()` - Count total entities

**Error Handling:**
- `RepositoryError` - Base exception for all repository errors
- `NotFoundError` - Entity not found
- `DuplicateError` - Unique constraint violation

### Farmer Repository (`farmer.py`)

Specialized operations for Farmer entities:

- `get_by_phone_number(phone)` - Find farmer by phone number
- `get_by_language(language)` - Filter farmers by preferred language
- `get_sms_enabled_farmers()` - Get farmers with SMS enabled
- `update_last_active(farmer_id)` - Update last activity timestamp
- `get_with_fields(farmer_id)` - Eager load farmer with all fields

### Field Repository (`field.py`)

Specialized operations for Field entities:

- `get_by_farmer_id(farmer_id)` - Get all fields for a farmer
- `get_by_crop_type(crop_type)` - Filter fields by crop type
- `get_by_pincode(pincode)` - Filter fields by postal code
- `get_by_location_range(min_lat, max_lat, min_lng, max_lng)` - Geographic search
- `get_with_recommendations(field_id)` - Eager load field with recommendations
- `count_by_farmer(farmer_id)` - Count fields per farmer

### Recommendation Repository (`recommendation.py`)

Specialized operations for Recommendation entities:

- `get_by_field_id(field_id)` - Get all recommendations for a field
- `get_by_field_and_date(field_id, date)` - Get specific date recommendation
- `get_by_date_range(field_id, start, end)` - Get recommendations in date range
- `get_latest_by_field(field_id)` - Get most recent recommendation
- `get_irrigation_recommendations(field_id, start, end)` - Filter by irrigate=True
- `count_by_field(field_id)` - Count recommendations per field

### Irrigation Activity Repository (`irrigation_activity.py`)

Specialized operations for IrrigationActivity entities:

- `get_by_field_id(field_id)` - Get all activities for a field
- `get_by_field_and_date(field_id, date)` - Get specific date activity
- `get_by_date_range(field_id, start, end)` - Get activities in date range
- `get_farmer_reported(field_id)` - Filter farmer-reported activities
- `calculate_total_water_usage(field_id, start, end)` - Sum water usage
- `calculate_total_cost(field_id, start, end)` - Sum irrigation costs
- `count_by_field(field_id)` - Count activities per field

### Savings Record Repository (`savings_record.py`)

Specialized operations for SavingsRecord entities:

- `get_by_field_id(field_id)` - Get all savings records for a field
- `get_by_period(field_id, start, end)` - Get specific period record
- `get_overlapping_periods(field_id, start, end)` - Find overlapping records
- `get_latest_by_field(field_id)` - Get most recent savings record
- `calculate_total_water_saved(field_id, start, end)` - Sum water savings
- `calculate_total_cost_saved(field_id, start, end)` - Sum cost savings
- `get_savings_summary(field_id)` - Comprehensive savings statistics
- `count_by_field(field_id)` - Count records per field

## Usage Examples

### Basic CRUD Operations

```python
from app.core.database import get_db
from app.repositories import FarmerRepository
from app.models import Farmer
from datetime import datetime
import uuid

# Get database session
db = next(get_db())

# Create repository
farmer_repo = FarmerRepository(db)

# Create a new farmer
farmer = Farmer(
    id=uuid.uuid4(),
    phone_number="+919876543210",
    preferred_language="hi",
    created_at=datetime.utcnow(),
    last_active=datetime.utcnow(),
    sms_enabled=True
)
created_farmer = farmer_repo.create(farmer)

# Get farmer by ID
farmer = farmer_repo.get_by_id(created_farmer.id)

# Update farmer
updated_farmer = farmer_repo.update(
    farmer.id,
    {"preferred_language": "en", "sms_enabled": False}
)

# Delete farmer
success = farmer_repo.delete(farmer.id)
```

### Specialized Queries

```python
from app.repositories import FieldRepository, RecommendationRepository
from datetime import date, timedelta

# Field repository
field_repo = FieldRepository(db)

# Get all fields for a farmer
fields = field_repo.get_by_farmer_id(farmer_id)

# Get fields by location
fields_in_area = field_repo.get_by_location_range(
    min_lat=28.0, max_lat=29.0,
    min_lng=77.0, max_lng=78.0
)

# Recommendation repository
rec_repo = RecommendationRepository(db)

# Get 7-day schedule
today = date.today()
week_later = today + timedelta(days=7)
schedule = rec_repo.get_by_date_range(field_id, today, week_later)

# Get latest recommendation
latest = rec_repo.get_latest_by_field(field_id)
```

### Aggregation Queries

```python
from app.repositories import IrrigationActivityRepository, SavingsRecordRepository
from datetime import date

# Irrigation activity repository
activity_repo = IrrigationActivityRepository(db)

# Calculate water usage for a month
start_date = date(2024, 1, 1)
end_date = date(2024, 1, 31)
total_water = activity_repo.calculate_total_water_usage(
    field_id, start_date, end_date
)
total_cost = activity_repo.calculate_total_cost(
    field_id, start_date, end_date
)

# Savings repository
savings_repo = SavingsRecordRepository(db)

# Get comprehensive savings summary
summary = savings_repo.get_savings_summary(field_id)
print(f"Total water saved: {summary['total_water_saved_liters']}L")
print(f"Total cost saved: ₹{summary['total_cost_saved_rupees']}")
```

### Error Handling

```python
from app.repositories import FarmerRepository
from app.repositories.base import RepositoryError, DuplicateError, NotFoundError

farmer_repo = FarmerRepository(db)

try:
    # Attempt to create farmer
    farmer = farmer_repo.create(new_farmer)
except DuplicateError as e:
    print(f"Farmer already exists: {e}")
except RepositoryError as e:
    print(f"Database error: {e}")

try:
    # Attempt to get farmer
    farmer = farmer_repo.get_by_id(farmer_id)
    if not farmer:
        raise NotFoundError(f"Farmer {farmer_id} not found")
except RepositoryError as e:
    print(f"Query failed: {e}")
```

### Transaction Management

```python
from app.core.database import SessionLocal
from app.repositories import FarmerRepository, FieldRepository

# Manual transaction management
db = SessionLocal()
try:
    farmer_repo = FarmerRepository(db)
    field_repo = FieldRepository(db)
    
    # Create farmer
    farmer = farmer_repo.create(new_farmer)
    
    # Create field for farmer
    field = field_repo.create(new_field)
    
    # Both operations committed automatically by repositories
    
except RepositoryError as e:
    # Rollback handled automatically by repositories
    print(f"Transaction failed: {e}")
finally:
    db.close()
```

## Best Practices

1. **Always use repositories** - Never access models directly from API endpoints
2. **Handle exceptions** - Catch `RepositoryError` and its subclasses
3. **Use pagination** - Always specify `skip` and `limit` for list operations
4. **Close sessions** - Use context managers or try/finally blocks
5. **Log errors** - Repository layer logs all errors automatically
6. **Validate input** - Use Pydantic schemas before repository calls
7. **Use eager loading** - Use `get_with_*` methods to avoid N+1 queries

## Testing

Each repository should be tested with:

1. **Unit tests** - Test individual methods with mock database
2. **Integration tests** - Test with real database (test instance)
3. **Error scenarios** - Test constraint violations and failures
4. **Transaction tests** - Verify rollback behavior

Example test structure:

```python
import pytest
from app.repositories import FarmerRepository
from app.repositories.base import DuplicateError

def test_create_farmer(db_session):
    repo = FarmerRepository(db_session)
    farmer = repo.create(test_farmer)
    assert farmer.id is not None

def test_duplicate_phone_number(db_session):
    repo = FarmerRepository(db_session)
    repo.create(test_farmer)
    with pytest.raises(DuplicateError):
        repo.create(test_farmer)  # Same phone number
```

## Requirements Validation

This repository layer implements:

- **Requirement 7.1**: Persistent storage of all farmer profiles, field data, and irrigation history
- **Requirement 7.2**: Immediate data saving with timestamps for all irrigation activities

The repository pattern ensures:
- Data persistence through SQLAlchemy ORM
- Transaction safety with automatic rollback
- Timestamp tracking on all create operations
- Comprehensive error handling and logging
