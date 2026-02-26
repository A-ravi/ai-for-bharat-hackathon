"""
Unit tests for database models

Tests basic model creation, relationships, and constraints.
"""

import pytest
from datetime import datetime, date
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models import Farmer, Field, Recommendation, IrrigationActivity, SavingsRecord


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


def test_farmer_creation(db_session):
    """Test creating a farmer record"""
    farmer = Farmer(
        id=uuid4(),
        phone_number="+919876543210",
        preferred_language="hi",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        sms_enabled=True
    )
    
    db_session.add(farmer)
    db_session.commit()
    
    assert farmer.id is not None
    assert farmer.phone_number == "+919876543210"
    assert farmer.preferred_language == "hi"
    assert farmer.sms_enabled is True


def test_field_creation(db_session):
    """Test creating a field record with farmer relationship"""
    farmer = Farmer(
        id=uuid4(),
        phone_number="+919876543210",
        preferred_language="hi",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        sms_enabled=True
    )
    db_session.add(farmer)
    db_session.commit()
    
    field = Field(
        id=uuid4(),
        farmer_id=farmer.id,
        crop_type="wheat",
        field_size_acres=5.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    
    db_session.add(field)
    db_session.commit()
    
    assert field.id is not None
    assert field.farmer_id == farmer.id
    assert field.crop_type == "wheat"
    assert field.field_size_acres == 5.0
    assert field.irrigation_method == "drip"


def test_recommendation_creation(db_session):
    """Test creating a recommendation record"""
    farmer = Farmer(
        id=uuid4(),
        phone_number="+919876543210",
        preferred_language="hi",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        sms_enabled=True
    )
    db_session.add(farmer)
    
    field = Field(
        id=uuid4(),
        farmer_id=farmer.id,
        crop_type="wheat",
        field_size_acres=5.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    db_session.add(field)
    db_session.commit()
    
    recommendation = Recommendation(
        id=uuid4(),
        field_id=field.id,
        date=date.today(),
        irrigate=True,
        amount_mm=25.0,
        timing="evening",
        confidence=0.85,
        weather_data={"temp": 30, "humidity": 60},
        reasoning="Low soil moisture, no rain expected",
        localized_message="आज शाम 25mm पानी दें",
        created_at=datetime.utcnow()
    )
    
    db_session.add(recommendation)
    db_session.commit()
    
    assert recommendation.id is not None
    assert recommendation.field_id == field.id
    assert recommendation.irrigate is True
    assert recommendation.amount_mm == 25.0
    assert recommendation.timing == "evening"


def test_irrigation_activity_creation(db_session):
    """Test creating an irrigation activity record"""
    farmer = Farmer(
        id=uuid4(),
        phone_number="+919876543210",
        preferred_language="hi",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        sms_enabled=True
    )
    db_session.add(farmer)
    
    field = Field(
        id=uuid4(),
        farmer_id=farmer.id,
        crop_type="wheat",
        field_size_acres=5.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    db_session.add(field)
    db_session.commit()
    
    activity = IrrigationActivity(
        id=uuid4(),
        field_id=field.id,
        date=date.today(),
        amount_mm=25.0,
        method="drip",
        farmer_reported=True,
        cost_rupees=50.0,
        created_at=datetime.utcnow()
    )
    
    db_session.add(activity)
    db_session.commit()
    
    assert activity.id is not None
    assert activity.field_id == field.id
    assert activity.amount_mm == 25.0
    assert activity.farmer_reported is True
    assert activity.cost_rupees == 50.0


def test_savings_record_creation(db_session):
    """Test creating a savings record"""
    farmer = Farmer(
        id=uuid4(),
        phone_number="+919876543210",
        preferred_language="hi",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        sms_enabled=True
    )
    db_session.add(farmer)
    
    field = Field(
        id=uuid4(),
        farmer_id=farmer.id,
        crop_type="wheat",
        field_size_acres=5.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    db_session.add(field)
    db_session.commit()
    
    savings = SavingsRecord(
        id=uuid4(),
        field_id=field.id,
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        water_saved_liters=5000.0,
        cost_saved_rupees=150.0,
        traditional_usage_liters=15000.0,
        actual_usage_liters=10000.0,
        calculated_at=datetime.utcnow()
    )
    
    db_session.add(savings)
    db_session.commit()
    
    assert savings.id is not None
    assert savings.field_id == field.id
    assert savings.water_saved_liters == 5000.0
    assert savings.cost_saved_rupees == 150.0


def test_farmer_field_relationship(db_session):
    """Test the relationship between farmer and fields"""
    farmer = Farmer(
        id=uuid4(),
        phone_number="+919876543210",
        preferred_language="hi",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        sms_enabled=True
    )
    db_session.add(farmer)
    db_session.commit()
    
    field1 = Field(
        id=uuid4(),
        farmer_id=farmer.id,
        crop_type="wheat",
        field_size_acres=5.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    
    field2 = Field(
        id=uuid4(),
        farmer_id=farmer.id,
        crop_type="rice",
        field_size_acres=3.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="flood",
        planting_date=date(2024, 1, 15),
        created_at=datetime.utcnow()
    )
    
    db_session.add_all([field1, field2])
    db_session.commit()
    
    # Refresh to load relationships
    db_session.refresh(farmer)
    
    assert len(farmer.fields) == 2
    assert farmer.fields[0].crop_type in ["wheat", "rice"]
    assert farmer.fields[1].crop_type in ["wheat", "rice"]


def test_field_cascade_delete(db_session):
    """Test that deleting a farmer cascades to fields"""
    farmer = Farmer(
        id=uuid4(),
        phone_number="+919876543210",
        preferred_language="hi",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        sms_enabled=True
    )
    db_session.add(farmer)
    db_session.commit()
    
    field = Field(
        id=uuid4(),
        farmer_id=farmer.id,
        crop_type="wheat",
        field_size_acres=5.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 1),
        created_at=datetime.utcnow()
    )
    db_session.add(field)
    db_session.commit()
    
    field_id = field.id
    
    # Delete farmer
    db_session.delete(farmer)
    db_session.commit()
    
    # Field should be deleted due to cascade
    deleted_field = db_session.query(Field).filter(Field.id == field_id).first()
    assert deleted_field is None
