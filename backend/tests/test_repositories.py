"""
Unit tests for repository layer

Tests CRUD operations, specialized queries, error handling, and transaction management
for all repository classes.
"""

import pytest
from datetime import datetime, date, timedelta
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models import Farmer, Field, Recommendation, IrrigationActivity, SavingsRecord
from app.repositories import (
    FarmerRepository,
    FieldRepository,
    RecommendationRepository,
    IrrigationActivityRepository,
    SavingsRecordRepository
)
from app.repositories.base import RepositoryError, DuplicateError


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()


@pytest.fixture
def sample_farmer():
    """Create a sample farmer for testing"""
    return Farmer(
        id=uuid4(),
        phone_number="+919876543210",
        preferred_language="hi",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        sms_enabled=True
    )


@pytest.fixture
def sample_field(sample_farmer):
    """Create a sample field for testing"""
    return Field(
        id=uuid4(),
        farmer_id=sample_farmer.id,
        crop_type="wheat",
        field_size_acres=5.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )


# ============================================================================
# Farmer Repository Tests
# ============================================================================

def test_farmer_repository_create(db_session, sample_farmer):
    """Test creating a farmer through repository"""
    repo = FarmerRepository(db_session)
    created = repo.create(sample_farmer)
    
    assert created.id == sample_farmer.id
    assert created.phone_number == sample_farmer.phone_number
    assert created.preferred_language == "hi"


def test_farmer_repository_get_by_id(db_session, sample_farmer):
    """Test retrieving farmer by ID"""
    repo = FarmerRepository(db_session)
    created = repo.create(sample_farmer)
    
    retrieved = repo.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.phone_number == created.phone_number


def test_farmer_repository_get_by_phone_number(db_session, sample_farmer):
    """Test retrieving farmer by phone number"""
    repo = FarmerRepository(db_session)
    repo.create(sample_farmer)
    
    retrieved = repo.get_by_phone_number(sample_farmer.phone_number)
    assert retrieved is not None
    assert retrieved.phone_number == sample_farmer.phone_number


def test_farmer_repository_update(db_session, sample_farmer):
    """Test updating farmer"""
    repo = FarmerRepository(db_session)
    created = repo.create(sample_farmer)
    
    updated = repo.update(created.id, {
        "preferred_language": "en",
        "sms_enabled": False
    })
    
    assert updated is not None
    assert updated.preferred_language == "en"
    assert updated.sms_enabled is False


def test_farmer_repository_delete(db_session, sample_farmer):
    """Test deleting farmer"""
    repo = FarmerRepository(db_session)
    created = repo.create(sample_farmer)
    
    success = repo.delete(created.id)
    assert success is True
    
    retrieved = repo.get_by_id(created.id)
    assert retrieved is None


def test_farmer_repository_get_by_language(db_session):
    """Test filtering farmers by language"""
    repo = FarmerRepository(db_session)
    
    # Create farmers with different languages
    farmer1 = Farmer(
        id=uuid4(), phone_number="+919876543210", preferred_language="hi",
        created_at=datetime.utcnow(), last_active=datetime.utcnow(), sms_enabled=True
    )
    farmer2 = Farmer(
        id=uuid4(), phone_number="+919876543211", preferred_language="en",
        created_at=datetime.utcnow(), last_active=datetime.utcnow(), sms_enabled=True
    )
    farmer3 = Farmer(
        id=uuid4(), phone_number="+919876543212", preferred_language="hi",
        created_at=datetime.utcnow(), last_active=datetime.utcnow(), sms_enabled=True
    )
    
    repo.create(farmer1)
    repo.create(farmer2)
    repo.create(farmer3)
    
    hindi_farmers = repo.get_by_language("hi")
    assert len(hindi_farmers) == 2


def test_farmer_repository_update_last_active(db_session, sample_farmer):
    """Test updating last active timestamp"""
    repo = FarmerRepository(db_session)
    created = repo.create(sample_farmer)
    
    original_time = created.last_active
    
    # Wait a moment and update
    import time
    time.sleep(0.1)
    
    updated = repo.update_last_active(created.id)
    assert updated is not None
    assert updated.last_active > original_time


# ============================================================================
# Field Repository Tests
# ============================================================================

def test_field_repository_create(db_session, sample_farmer, sample_field):
    """Test creating a field through repository"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    created = field_repo.create(sample_field)
    
    assert created.id == sample_field.id
    assert created.farmer_id == sample_farmer.id
    assert created.crop_type == "wheat"


def test_field_repository_get_by_farmer_id(db_session, sample_farmer):
    """Test retrieving fields by farmer ID"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    
    # Create multiple fields
    field1 = Field(
        id=uuid4(), farmer_id=sample_farmer.id, crop_type="wheat",
        field_size_acres=5.0, location_lat=28.6139, location_lng=77.2090,
        pincode="110001", irrigation_method="drip", planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    field2 = Field(
        id=uuid4(), farmer_id=sample_farmer.id, crop_type="rice",
        field_size_acres=3.0, location_lat=28.6139, location_lng=77.2090,
        pincode="110001", irrigation_method="flood", planting_date=date(2024, 1, 15),
        created_at=datetime.utcnow()
    )
    
    field_repo.create(field1)
    field_repo.create(field2)
    
    fields = field_repo.get_by_farmer_id(sample_farmer.id)
    assert len(fields) == 2


def test_field_repository_get_by_crop_type(db_session, sample_farmer):
    """Test filtering fields by crop type"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    
    field1 = Field(
        id=uuid4(), farmer_id=sample_farmer.id, crop_type="wheat",
        field_size_acres=5.0, location_lat=28.6139, location_lng=77.2090,
        pincode="110001", irrigation_method="drip", planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    field2 = Field(
        id=uuid4(), farmer_id=sample_farmer.id, crop_type="rice",
        field_size_acres=3.0, location_lat=28.6139, location_lng=77.2090,
        pincode="110001", irrigation_method="flood", planting_date=date(2024, 1, 15),
        created_at=datetime.utcnow()
    )
    
    field_repo.create(field1)
    field_repo.create(field2)
    
    wheat_fields = field_repo.get_by_crop_type("wheat")
    assert len(wheat_fields) == 1
    assert wheat_fields[0].crop_type == "wheat"


def test_field_repository_get_by_location_range(db_session, sample_farmer):
    """Test geographic search for fields"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    
    field1 = Field(
        id=uuid4(), farmer_id=sample_farmer.id, crop_type="wheat",
        field_size_acres=5.0, location_lat=28.6139, location_lng=77.2090,
        pincode="110001", irrigation_method="drip", planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    field2 = Field(
        id=uuid4(), farmer_id=sample_farmer.id, crop_type="rice",
        field_size_acres=3.0, location_lat=19.0760, location_lng=72.8777,
        pincode="400001", irrigation_method="flood", planting_date=date(2024, 1, 15),
        created_at=datetime.utcnow()
    )
    
    field_repo.create(field1)
    field_repo.create(field2)
    
    # Search for fields in Delhi area
    delhi_fields = field_repo.get_by_location_range(
        min_lat=28.0, max_lat=29.0,
        min_lng=77.0, max_lng=78.0
    )
    assert len(delhi_fields) == 1
    assert delhi_fields[0].location_lat == 28.6139


def test_field_repository_count_by_farmer(db_session, sample_farmer):
    """Test counting fields per farmer"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    
    field1 = Field(
        id=uuid4(), farmer_id=sample_farmer.id, crop_type="wheat",
        field_size_acres=5.0, location_lat=28.6139, location_lng=77.2090,
        pincode="110001", irrigation_method="drip", planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    field2 = Field(
        id=uuid4(), farmer_id=sample_farmer.id, crop_type="rice",
        field_size_acres=3.0, location_lat=28.6139, location_lng=77.2090,
        pincode="110001", irrigation_method="flood", planting_date=date(2024, 1, 15),
        created_at=datetime.utcnow()
    )
    
    field_repo.create(field1)
    field_repo.create(field2)
    
    count = field_repo.count_by_farmer(sample_farmer.id)
    assert count == 2


# ============================================================================
# Recommendation Repository Tests
# ============================================================================

def test_recommendation_repository_create(db_session, sample_farmer, sample_field):
    """Test creating a recommendation through repository"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    rec_repo = RecommendationRepository(db_session)
    
    recommendation = Recommendation(
        id=uuid4(),
        field_id=sample_field.id,
        date=date.today(),
        irrigate=True,
        amount_mm=25.0,
        timing="evening",
        confidence=0.85,
        weather_data={"temp": 30, "humidity": 60},
        reasoning="Low soil moisture",
        localized_message="आज शाम 25mm पानी दें",
        created_at=datetime.utcnow()
    )
    
    created = rec_repo.create(recommendation)
    assert created.id == recommendation.id
    assert created.irrigate is True


def test_recommendation_repository_get_by_field_and_date(db_session, sample_farmer, sample_field):
    """Test retrieving recommendation by field and date"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    rec_repo = RecommendationRepository(db_session)
    
    today = date.today()
    recommendation = Recommendation(
        id=uuid4(), field_id=sample_field.id, date=today, irrigate=True,
        amount_mm=25.0, timing="evening", confidence=0.85,
        weather_data={}, reasoning="Test", localized_message="Test",
        created_at=datetime.utcnow()
    )
    
    rec_repo.create(recommendation)
    
    retrieved = rec_repo.get_by_field_and_date(sample_field.id, today)
    assert retrieved is not None
    assert retrieved.date == today


def test_recommendation_repository_get_by_date_range(db_session, sample_farmer, sample_field):
    """Test retrieving recommendations in date range"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    rec_repo = RecommendationRepository(db_session)
    
    # Create recommendations for 7 days
    today = date.today()
    for i in range(7):
        rec_date = today + timedelta(days=i)
        recommendation = Recommendation(
            id=uuid4(), field_id=sample_field.id, date=rec_date, irrigate=True,
            amount_mm=25.0, timing="evening", confidence=0.85,
            weather_data={}, reasoning="Test", localized_message="Test",
            created_at=datetime.utcnow()
        )
        rec_repo.create(recommendation)
    
    # Get 7-day schedule
    week_later = today + timedelta(days=6)
    schedule = rec_repo.get_by_date_range(sample_field.id, today, week_later)
    assert len(schedule) == 7


def test_recommendation_repository_get_latest(db_session, sample_farmer, sample_field):
    """Test retrieving latest recommendation"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    rec_repo = RecommendationRepository(db_session)
    
    # Create recommendations
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    rec1 = Recommendation(
        id=uuid4(), field_id=sample_field.id, date=yesterday, irrigate=True,
        amount_mm=20.0, timing="morning", confidence=0.80,
        weather_data={}, reasoning="Test", localized_message="Test",
        created_at=datetime.utcnow()
    )
    rec2 = Recommendation(
        id=uuid4(), field_id=sample_field.id, date=today, irrigate=True,
        amount_mm=25.0, timing="evening", confidence=0.85,
        weather_data={}, reasoning="Test", localized_message="Test",
        created_at=datetime.utcnow()
    )
    
    rec_repo.create(rec1)
    rec_repo.create(rec2)
    
    latest = rec_repo.get_latest_by_field(sample_field.id)
    assert latest is not None
    assert latest.date == today


# ============================================================================
# Irrigation Activity Repository Tests
# ============================================================================

def test_irrigation_activity_repository_create(db_session, sample_farmer, sample_field):
    """Test creating an irrigation activity through repository"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    activity_repo = IrrigationActivityRepository(db_session)
    
    activity = IrrigationActivity(
        id=uuid4(),
        field_id=sample_field.id,
        date=date.today(),
        amount_mm=25.0,
        method="drip",
        farmer_reported=True,
        cost_rupees=50.0,
        created_at=datetime.utcnow()
    )
    
    created = activity_repo.create(activity)
    assert created.id == activity.id
    assert created.amount_mm == 25.0


def test_irrigation_activity_calculate_total_water_usage(db_session, sample_farmer, sample_field):
    """Test calculating total water usage"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    activity_repo = IrrigationActivityRepository(db_session)
    
    # Create activities
    start_date = date(2024, 1, 1)
    for i in range(5):
        activity = IrrigationActivity(
            id=uuid4(), field_id=sample_field.id,
            date=start_date + timedelta(days=i),
            amount_mm=20.0, method="drip", farmer_reported=True,
            cost_rupees=40.0, created_at=datetime.utcnow()
        )
        activity_repo.create(activity)
    
    end_date = date(2024, 1, 5)
    total = activity_repo.calculate_total_water_usage(sample_field.id, start_date, end_date)
    assert total == 100.0  # 5 activities * 20mm


def test_irrigation_activity_calculate_total_cost(db_session, sample_farmer, sample_field):
    """Test calculating total irrigation cost"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    activity_repo = IrrigationActivityRepository(db_session)
    
    # Create activities
    start_date = date(2024, 1, 1)
    for i in range(5):
        activity = IrrigationActivity(
            id=uuid4(), field_id=sample_field.id,
            date=start_date + timedelta(days=i),
            amount_mm=20.0, method="drip", farmer_reported=True,
            cost_rupees=40.0, created_at=datetime.utcnow()
        )
        activity_repo.create(activity)
    
    end_date = date(2024, 1, 5)
    total = activity_repo.calculate_total_cost(sample_field.id, start_date, end_date)
    assert total == 200.0  # 5 activities * ₹40


# ============================================================================
# Savings Record Repository Tests
# ============================================================================

def test_savings_record_repository_create(db_session, sample_farmer, sample_field):
    """Test creating a savings record through repository"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    savings_repo = SavingsRecordRepository(db_session)
    
    savings = SavingsRecord(
        id=uuid4(),
        field_id=sample_field.id,
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        water_saved_liters=5000.0,
        cost_saved_rupees=150.0,
        traditional_usage_liters=15000.0,
        actual_usage_liters=10000.0,
        calculated_at=datetime.utcnow()
    )
    
    created = savings_repo.create(savings)
    assert created.id == savings.id
    assert created.water_saved_liters == 5000.0


def test_savings_record_get_savings_summary(db_session, sample_farmer, sample_field):
    """Test getting comprehensive savings summary"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    savings_repo = SavingsRecordRepository(db_session)
    
    # Create multiple savings records
    savings1 = SavingsRecord(
        id=uuid4(), field_id=sample_field.id,
        period_start=date(2024, 1, 1), period_end=date(2024, 1, 31),
        water_saved_liters=5000.0, cost_saved_rupees=150.0,
        traditional_usage_liters=15000.0, actual_usage_liters=10000.0,
        calculated_at=datetime.utcnow()
    )
    savings2 = SavingsRecord(
        id=uuid4(), field_id=sample_field.id,
        period_start=date(2024, 2, 1), period_end=date(2024, 2, 29),
        water_saved_liters=4500.0, cost_saved_rupees=135.0,
        traditional_usage_liters=14000.0, actual_usage_liters=9500.0,
        calculated_at=datetime.utcnow()
    )
    
    savings_repo.create(savings1)
    savings_repo.create(savings2)
    
    summary = savings_repo.get_savings_summary(sample_field.id)
    assert summary['total_water_saved_liters'] == 9500.0
    assert summary['total_cost_saved_rupees'] == 285.0
    assert summary['record_count'] == 2


def test_savings_record_calculate_total_water_saved(db_session, sample_farmer, sample_field):
    """Test calculating total water saved"""
    farmer_repo = FarmerRepository(db_session)
    farmer_repo.create(sample_farmer)
    
    field_repo = FieldRepository(db_session)
    field_repo.create(sample_field)
    
    savings_repo = SavingsRecordRepository(db_session)
    
    # Create savings records
    savings1 = SavingsRecord(
        id=uuid4(), field_id=sample_field.id,
        period_start=date(2024, 1, 1), period_end=date(2024, 1, 31),
        water_saved_liters=5000.0, cost_saved_rupees=150.0,
        traditional_usage_liters=15000.0, actual_usage_liters=10000.0,
        calculated_at=datetime.utcnow()
    )
    savings2 = SavingsRecord(
        id=uuid4(), field_id=sample_field.id,
        period_start=date(2024, 2, 1), period_end=date(2024, 2, 29),
        water_saved_liters=4500.0, cost_saved_rupees=135.0,
        traditional_usage_liters=14000.0, actual_usage_liters=9500.0,
        calculated_at=datetime.utcnow()
    )
    
    savings_repo.create(savings1)
    savings_repo.create(savings2)
    
    total = savings_repo.calculate_total_water_saved(sample_field.id)
    assert total == 9500.0


# ============================================================================
# Error Handling Tests
# ============================================================================

def test_repository_get_nonexistent_id(db_session):
    """Test retrieving non-existent entity returns None"""
    repo = FarmerRepository(db_session)
    result = repo.get_by_id(uuid4())
    assert result is None


def test_repository_update_nonexistent_id(db_session):
    """Test updating non-existent entity returns None"""
    repo = FarmerRepository(db_session)
    result = repo.update(uuid4(), {"preferred_language": "en"})
    assert result is None


def test_repository_delete_nonexistent_id(db_session):
    """Test deleting non-existent entity returns False"""
    repo = FarmerRepository(db_session)
    result = repo.delete(uuid4())
    assert result is False


def test_repository_exists(db_session, sample_farmer):
    """Test checking if entity exists"""
    repo = FarmerRepository(db_session)
    
    # Non-existent
    assert repo.exists(uuid4()) is False
    
    # Existent
    created = repo.create(sample_farmer)
    assert repo.exists(created.id) is True


def test_repository_count(db_session):
    """Test counting entities"""
    repo = FarmerRepository(db_session)
    
    assert repo.count() == 0
    
    farmer1 = Farmer(
        id=uuid4(), phone_number="+919876543210", preferred_language="hi",
        created_at=datetime.utcnow(), last_active=datetime.utcnow(), sms_enabled=True
    )
    farmer2 = Farmer(
        id=uuid4(), phone_number="+919876543211", preferred_language="en",
        created_at=datetime.utcnow(), last_active=datetime.utcnow(), sms_enabled=True
    )
    
    repo.create(farmer1)
    repo.create(farmer2)
    
    assert repo.count() == 2
