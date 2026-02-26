"""Manual test script to verify Pydantic schemas work correctly."""
from datetime import date, datetime
from uuid import uuid4
from pydantic import ValidationError

from app.schemas import (
    FarmerCreate,
    FieldCreate,
    RecommendationCreate,
    IrrigationActivityCreate,
    SavingsRecordCreate,
)


def test_farmer_schema():
    """Test Farmer schema."""
    print("Testing Farmer schema...")
    
    # Valid farmer
    farmer = FarmerCreate(
        phone_number="9876543210",
        preferred_language="hi",
        sms_enabled=True
    )
    print(f"✓ Valid farmer created: {farmer.phone_number}")
    
    # Test validation - invalid phone
    try:
        FarmerCreate(phone_number="123", preferred_language="hi")
        print("✗ Should have failed with invalid phone")
    except ValidationError as e:
        print(f"✓ Correctly rejected invalid phone: {e.error_count()} errors")
    
    # Test validation - invalid language
    try:
        FarmerCreate(phone_number="9876543210", preferred_language="fr")
        print("✗ Should have failed with invalid language")
    except ValidationError as e:
        print(f"✓ Correctly rejected invalid language: {e.error_count()} errors")
    
    print()


def test_field_schema():
    """Test Field schema."""
    print("Testing Field schema...")
    
    # Valid field
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
    print(f"✓ Valid field created: {field.crop_type}, {field.field_size_acres} acres")
    
    # Test field size validation - too small (Requirement 1.5)
    try:
        FieldCreate(
            farmer_id=uuid4(),
            crop_type="wheat",
            field_size_acres=0.05,
            location_lat=28.6139,
            location_lng=77.2090,
            pincode="110001",
            irrigation_method="drip",
            planting_date=date(2024, 1, 15)
        )
        print("✗ Should have failed with field size too small")
    except ValidationError as e:
        print(f"✓ Correctly rejected field size < 0.1 acres: {e.error_count()} errors")
    
    # Test field size validation - too large (Requirement 1.5)
    try:
        FieldCreate(
            farmer_id=uuid4(),
            crop_type="wheat",
            field_size_acres=51.0,
            location_lat=28.6139,
            location_lng=77.2090,
            pincode="110001",
            irrigation_method="drip",
            planting_date=date(2024, 1, 15)
        )
        print("✗ Should have failed with field size too large")
    except ValidationError as e:
        print(f"✓ Correctly rejected field size > 50 acres: {e.error_count()} errors")
    
    # Test minimum valid size
    field_min = FieldCreate(
        farmer_id=uuid4(),
        crop_type="wheat",
        field_size_acres=0.1,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 15)
    )
    print(f"✓ Minimum field size accepted: {field_min.field_size_acres} acres")
    
    # Test maximum valid size
    field_max = FieldCreate(
        farmer_id=uuid4(),
        crop_type="wheat",
        field_size_acres=50.0,
        location_lat=28.6139,
        location_lng=77.2090,
        pincode="110001",
        irrigation_method="drip",
        planting_date=date(2024, 1, 15)
    )
    print(f"✓ Maximum field size accepted: {field_max.field_size_acres} acres")
    
    print()


def test_recommendation_schema():
    """Test Recommendation schema."""
    print("Testing Recommendation schema...")
    
    # Valid recommendation
    rec = RecommendationCreate(
        field_id=uuid4(),
        date=date(2024, 1, 20),
        irrigate=True,
        amount_mm=25.0,
        timing="evening",
        confidence=0.85,
        weather_data={"temperature": 28.5, "humidity": 65},
        reasoning="Low soil moisture, no rain expected for 3 days",
        localized_message="Kal shaam 25mm paani dein"
    )
    print(f"✓ Valid recommendation created: {rec.amount_mm}mm, {rec.timing}")
    
    # Test timing validation
    try:
        RecommendationCreate(
            field_id=uuid4(),
            date=date(2024, 1, 20),
            irrigate=True,
            amount_mm=25.0,
            timing="midnight",
            confidence=0.85,
            weather_data={},
            reasoning="Test",
            localized_message="Test"
        )
        print("✗ Should have failed with invalid timing")
    except ValidationError as e:
        print(f"✓ Correctly rejected invalid timing: {e.error_count()} errors")
    
    # Test confidence validation
    try:
        RecommendationCreate(
            field_id=uuid4(),
            date=date(2024, 1, 20),
            irrigate=True,
            amount_mm=25.0,
            timing="evening",
            confidence=1.5,
            weather_data={},
            reasoning="Test",
            localized_message="Test"
        )
        print("✗ Should have failed with invalid confidence")
    except ValidationError as e:
        print(f"✓ Correctly rejected confidence > 1.0: {e.error_count()} errors")
    
    print()


def test_irrigation_activity_schema():
    """Test IrrigationActivity schema."""
    print("Testing IrrigationActivity schema...")
    
    # Valid activity
    activity = IrrigationActivityCreate(
        field_id=uuid4(),
        date=date(2024, 1, 20),
        amount_mm=25.0,
        method="drip",
        farmer_reported=True,
        cost_rupees=150.0
    )
    print(f"✓ Valid irrigation activity created: {activity.amount_mm}mm, ₹{activity.cost_rupees}")
    
    # Test negative cost
    try:
        IrrigationActivityCreate(
            field_id=uuid4(),
            date=date(2024, 1, 20),
            amount_mm=25.0,
            method="drip",
            farmer_reported=True,
            cost_rupees=-10.0
        )
        print("✗ Should have failed with negative cost")
    except ValidationError as e:
        print(f"✓ Correctly rejected negative cost: {e.error_count()} errors")
    
    print()


def test_savings_record_schema():
    """Test SavingsRecord schema."""
    print("Testing SavingsRecord schema...")
    
    # Valid savings record
    record = SavingsRecordCreate(
        field_id=uuid4(),
        period_start=date(2024, 1, 1),
        period_end=date(2024, 1, 31),
        water_saved_liters=5000.0,
        cost_saved_rupees=15.0,  # ₹3 per 1000L
        traditional_usage_liters=15000.0,
        actual_usage_liters=10000.0
    )
    print(f"✓ Valid savings record created: {record.water_saved_liters}L saved, ₹{record.cost_saved_rupees}")
    
    # Test period validation
    try:
        SavingsRecordCreate(
            field_id=uuid4(),
            period_start=date(2024, 1, 31),
            period_end=date(2024, 1, 1),
            water_saved_liters=5000.0,
            cost_saved_rupees=15.0,
            traditional_usage_liters=15000.0,
            actual_usage_liters=10000.0
        )
        print("✗ Should have failed with invalid period")
    except ValidationError as e:
        print(f"✓ Correctly rejected invalid period: {e.error_count()} errors")
    
    # Test savings calculation validation
    try:
        SavingsRecordCreate(
            field_id=uuid4(),
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            water_saved_liters=6000.0,  # Incorrect
            cost_saved_rupees=15.0,
            traditional_usage_liters=15000.0,
            actual_usage_liters=10000.0
        )
        print("✗ Should have failed with inconsistent savings")
    except ValidationError as e:
        print(f"✓ Correctly rejected inconsistent savings calculation: {e.error_count()} errors")
    
    # Test cost rate validation - too low (Requirement 4.2)
    try:
        SavingsRecordCreate(
            field_id=uuid4(),
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            water_saved_liters=5000.0,
            cost_saved_rupees=5.0,  # ₹1 per 1000L - too low
            traditional_usage_liters=15000.0,
            actual_usage_liters=10000.0
        )
        print("✗ Should have failed with cost rate too low")
    except ValidationError as e:
        print(f"✓ Correctly rejected cost rate < ₹2/1000L: {e.error_count()} errors")
    
    # Test cost rate validation - too high (Requirement 4.2)
    try:
        SavingsRecordCreate(
            field_id=uuid4(),
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            water_saved_liters=5000.0,
            cost_saved_rupees=30.0,  # ₹6 per 1000L - too high
            traditional_usage_liters=15000.0,
            actual_usage_liters=10000.0
        )
        print("✗ Should have failed with cost rate too high")
    except ValidationError as e:
        print(f"✓ Correctly rejected cost rate > ₹5/1000L: {e.error_count()} errors")
    
    # Test valid cost rates
    for rate in [2.0, 3.0, 5.0]:
        cost = (5000.0 / 1000.0) * rate
        record = SavingsRecordCreate(
            field_id=uuid4(),
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            water_saved_liters=5000.0,
            cost_saved_rupees=cost,
            traditional_usage_liters=15000.0,
            actual_usage_liters=10000.0
        )
        print(f"✓ Valid cost rate ₹{rate}/1000L accepted: ₹{cost}")
    
    print()


def test_serialization():
    """Test model serialization."""
    print("Testing serialization...")
    
    # Create a field and serialize to JSON
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
    
    json_data = field.model_dump_json()
    print(f"✓ Field serialized to JSON: {len(json_data)} characters")
    
    # Test dict conversion
    dict_data = field.model_dump()
    print(f"✓ Field converted to dict: {len(dict_data)} fields")
    
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Pydantic Schema Validation Tests")
    print("=" * 60)
    print()
    
    test_farmer_schema()
    test_field_schema()
    test_recommendation_schema()
    test_irrigation_activity_schema()
    test_savings_record_schema()
    test_serialization()
    
    print("=" * 60)
    print("All manual tests completed!")
    print("=" * 60)
