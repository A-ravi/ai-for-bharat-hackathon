"""Unit tests for Pydantic schemas."""
import pytest
from datetime import date, datetime
from uuid import uuid4
from pydantic import ValidationError

from app.schemas import (
    FarmerCreate,
    FarmerUpdate,
    FarmerResponse,
    FieldCreate,
    FieldUpdate,
    FieldResponse,
    RecommendationCreate,
    RecommendationUpdate,
    RecommendationResponse,
    IrrigationActivityCreate,
    IrrigationActivityUpdate,
    IrrigationActivityResponse,
    SavingsRecordCreate,
    SavingsRecordUpdate,
    SavingsRecordResponse,
    SavingsSummary,
)


class TestFarmerSchemas:
    """Test Farmer Pydantic schemas."""

    def test_farmer_create_valid(self):
        """Test creating a valid farmer."""
        farmer = FarmerCreate(
            phone_number="9876543210",
            preferred_language="hi",
            sms_enabled=True
        )
        assert farmer.phone_number == "9876543210"
        assert farmer.preferred_language == "hi"
        assert farmer.sms_enabled is True

    def test_farmer_create_with_country_code(self):
        """Test creating farmer with +91 country code."""
        farmer = FarmerCreate(
            phone_number="+919876543210",
            preferred_language="en"
        )
        assert farmer.phone_number == "+919876543210"

    def test_farmer_create_invalid_phone_short(self):
        """Test farmer creation fails with short phone number."""
        with pytest.raises(ValidationError) as exc_info:
            FarmerCreate(
                phone_number="98765",
                preferred_language="hi"
            )
        assert "Phone number must be exactly 10 digits" in str(exc_info.value)

    def test_farmer_create_invalid_phone_long(self):
        """Test farmer creation fails with long phone number."""
        with pytest.raises(ValidationError) as exc_info:
            FarmerCreate(
                phone_number="98765432101234",
                preferred_language="hi"
            )
        assert "Phone number must be exactly 10 digits" in str(exc_info.value)

    def test_farmer_create_invalid_phone_letters(self):
        """Test farmer creation fails with letters in phone number."""
        with pytest.raises(ValidationError) as exc_info:
            FarmerCreate(
                phone_number="987654abcd",
                preferred_language="hi"
            )
        assert "must contain only digits" in str(exc_info.value)

    def test_farmer_create_invalid_language(self):
        """Test farmer creation fails with unsupported language."""
        with pytest.raises(ValidationError) as exc_info:
            FarmerCreate(
                phone_number="9876543210",
                preferred_language="fr"
            )
        assert "Language must be one of" in str(exc_info.value)

    def test_farmer_create_all_supported_languages(self):
        """Test farmer creation with all supported languages."""
        languages = ["hi", "en", "mr", "gu", "pa", "ta", "te", "kn"]
        for lang in languages:
            farmer = FarmerCreate(
                phone_number="9876543210",
                preferred_language=lang
            )
            assert farmer.preferred_language == lang

    def test_farmer_update_partial(self):
        """Test partial farmer update."""
        update = FarmerUpdate(preferred_language="ta")
        assert update.preferred_language == "ta"
        assert update.phone_number is None
        assert update.sms_enabled is None


class TestFieldSchemas:
    """Test Field Pydantic schemas."""

    def test_field_create_valid(self):
        """Test creating a valid field."""
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
        assert field.crop_type == "wheat"
        assert field.field_size_acres == 5.5
        assert field.irrigation_method == "drip"

    def test_field_create_minimum_size(self):
        """Test field creation with minimum size (0.1 acres)."""
        field = FieldCreate(
            farmer_id=uuid4(),
            crop_type="wheat",
            field_size_acres=0.1,
            location_lat=28.6139,
            location_lng=77.2090,
            pincode="110001",
            irrigation_method="drip",
            planting_date=date(2024, 1, 15)
        )
        assert field.field_size_acres == 0.1

    def test_field_create_maximum_size(self):
        """Test field creation with maximum size (50 acres)."""
        field = FieldCreate(
            farmer_id=uuid4(),
            crop_type="wheat",
            field_size_acres=50.0,
            location_lat=28.6139,
            location_lng=77.2090,
            pincode="110001",
            irrigation_method="drip",
            planting_date=date(2024, 1, 15)
        )
        assert field.field_size_acres == 50.0

    def test_field_create_size_too_small(self):
        """Test field creation fails with size below 0.1 acres (Requirement 1.5)."""
        with pytest.raises(ValidationError) as exc_info:
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
        assert "Field size must be at least 0.1 acres" in str(exc_info.value)

    def test_field_create_size_too_large(self):
        """Test field creation fails with size above 50 acres (Requirement 1.5)."""
        with pytest.raises(ValidationError) as exc_info:
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
        assert "Field size must not exceed 50 acres" in str(exc_info.value)

    def test_field_create_invalid_irrigation_method(self):
        """Test field creation fails with invalid irrigation method."""
        with pytest.raises(ValidationError) as exc_info:
            FieldCreate(
                farmer_id=uuid4(),
                crop_type="wheat",
                field_size_acres=5.5,
                location_lat=28.6139,
                location_lng=77.2090,
                pincode="110001",
                irrigation_method="invalid",
                planting_date=date(2024, 1, 15)
            )
        assert "Irrigation method must be one of" in str(exc_info.value)

    def test_field_create_all_irrigation_methods(self):
        """Test field creation with all supported irrigation methods."""
        methods = ["drip", "sprinkler", "flood"]
        for method in methods:
            field = FieldCreate(
                farmer_id=uuid4(),
                crop_type="wheat",
                field_size_acres=5.5,
                location_lat=28.6139,
                location_lng=77.2090,
                pincode="110001",
                irrigation_method=method,
                planting_date=date(2024, 1, 15)
            )
            assert field.irrigation_method == method

    def test_field_create_invalid_pincode(self):
        """Test field creation fails with invalid pincode."""
        with pytest.raises(ValidationError) as exc_info:
            FieldCreate(
                farmer_id=uuid4(),
                crop_type="wheat",
                field_size_acres=5.5,
                location_lat=28.6139,
                location_lng=77.2090,
                pincode="12345",  # Only 5 digits
                irrigation_method="drip",
                planting_date=date(2024, 1, 15)
            )
        assert "pincode must be exactly 6 digits" in str(exc_info.value)

    def test_field_create_latitude_out_of_india(self):
        """Test field creation fails with latitude outside India."""
        with pytest.raises(ValidationError) as exc_info:
            FieldCreate(
                farmer_id=uuid4(),
                crop_type="wheat",
                field_size_acres=5.5,
                location_lat=50.0,  # Too far north
                location_lng=77.2090,
                pincode="110001",
                irrigation_method="drip",
                planting_date=date(2024, 1, 15)
            )
        assert "within India's approximate bounds" in str(exc_info.value)

    def test_field_create_longitude_out_of_india(self):
        """Test field creation fails with longitude outside India."""
        with pytest.raises(ValidationError) as exc_info:
            FieldCreate(
                farmer_id=uuid4(),
                crop_type="wheat",
                field_size_acres=5.5,
                location_lat=28.6139,
                location_lng=120.0,  # Too far east
                pincode="110001",
                irrigation_method="drip",
                planting_date=date(2024, 1, 15)
            )
        assert "within India's approximate bounds" in str(exc_info.value)


class TestRecommendationSchemas:
    """Test Recommendation Pydantic schemas."""

    def test_recommendation_create_valid(self):
        """Test creating a valid recommendation."""
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
        assert rec.irrigate is True
        assert rec.amount_mm == 25.0
        assert rec.timing == "evening"

    def test_recommendation_create_invalid_timing(self):
        """Test recommendation creation fails with invalid timing."""
        with pytest.raises(ValidationError) as exc_info:
            RecommendationCreate(
                field_id=uuid4(),
                date=date(2024, 1, 20),
                irrigate=True,
                amount_mm=25.0,
                timing="midnight",
                confidence=0.85,
                weather_data={},
                reasoning="Low soil moisture",
                localized_message="Test message"
            )
        assert "Timing must be one of" in str(exc_info.value)

    def test_recommendation_create_all_timings(self):
        """Test recommendation creation with all supported timings."""
        timings = ["morning", "afternoon", "evening"]
        for timing in timings:
            rec = RecommendationCreate(
                field_id=uuid4(),
                date=date(2024, 1, 20),
                irrigate=True,
                amount_mm=25.0,
                timing=timing,
                confidence=0.85,
                weather_data={},
                reasoning="Low soil moisture",
                localized_message="Test message"
            )
            assert rec.timing == timing

    def test_recommendation_create_negative_amount(self):
        """Test recommendation creation fails with negative water amount."""
        with pytest.raises(ValidationError) as exc_info:
            RecommendationCreate(
                field_id=uuid4(),
                date=date(2024, 1, 20),
                irrigate=True,
                amount_mm=-5.0,
                timing="evening",
                confidence=0.85,
                weather_data={},
                reasoning="Test",
                localized_message="Test"
            )
        assert "Water amount cannot be negative" in str(exc_info.value)

    def test_recommendation_create_excessive_amount(self):
        """Test recommendation creation fails with excessive water amount."""
        with pytest.raises(ValidationError) as exc_info:
            RecommendationCreate(
                field_id=uuid4(),
                date=date(2024, 1, 20),
                irrigate=True,
                amount_mm=150.0,
                timing="evening",
                confidence=0.85,
                weather_data={},
                reasoning="Test",
                localized_message="Test"
            )
        assert "exceeds reasonable maximum" in str(exc_info.value)

    def test_recommendation_create_invalid_confidence_low(self):
        """Test recommendation creation fails with confidence below 0."""
        with pytest.raises(ValidationError) as exc_info:
            RecommendationCreate(
                field_id=uuid4(),
                date=date(2024, 1, 20),
                irrigate=True,
                amount_mm=25.0,
                timing="evening",
                confidence=-0.1,
                weather_data={},
                reasoning="Test",
                localized_message="Test"
            )
        assert "Confidence must be between 0.0 and 1.0" in str(exc_info.value)

    def test_recommendation_create_invalid_confidence_high(self):
        """Test recommendation creation fails with confidence above 1."""
        with pytest.raises(ValidationError) as exc_info:
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
        assert "Confidence must be between 0.0 and 1.0" in str(exc_info.value)


class TestIrrigationActivitySchemas:
    """Test IrrigationActivity Pydantic schemas."""

    def test_irrigation_activity_create_valid(self):
        """Test creating a valid irrigation activity."""
        activity = IrrigationActivityCreate(
            field_id=uuid4(),
            date=date(2024, 1, 20),
            amount_mm=25.0,
            method="drip",
            farmer_reported=True,
            cost_rupees=150.0
        )
        assert activity.amount_mm == 25.0
        assert activity.method == "drip"
        assert activity.farmer_reported is True

    def test_irrigation_activity_create_negative_cost(self):
        """Test irrigation activity creation fails with negative cost."""
        with pytest.raises(ValidationError) as exc_info:
            IrrigationActivityCreate(
                field_id=uuid4(),
                date=date(2024, 1, 20),
                amount_mm=25.0,
                method="drip",
                farmer_reported=True,
                cost_rupees=-10.0
            )
        assert "Cost cannot be negative" in str(exc_info.value)

    def test_irrigation_activity_create_invalid_method(self):
        """Test irrigation activity creation fails with invalid method."""
        with pytest.raises(ValidationError) as exc_info:
            IrrigationActivityCreate(
                field_id=uuid4(),
                date=date(2024, 1, 20),
                amount_mm=25.0,
                method="invalid",
                farmer_reported=True,
                cost_rupees=150.0
            )
        assert "Irrigation method must be one of" in str(exc_info.value)


class TestSavingsRecordSchemas:
    """Test SavingsRecord Pydantic schemas."""

    def test_savings_record_create_valid(self):
        """Test creating a valid savings record."""
        record = SavingsRecordCreate(
            field_id=uuid4(),
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            water_saved_liters=5000.0,
            cost_saved_rupees=15.0,  # ₹3 per 1000L
            traditional_usage_liters=15000.0,
            actual_usage_liters=10000.0
        )
        assert record.water_saved_liters == 5000.0
        assert record.cost_saved_rupees == 15.0

    def test_savings_record_create_invalid_period(self):
        """Test savings record creation fails when end is before start."""
        with pytest.raises(ValidationError) as exc_info:
            SavingsRecordCreate(
                field_id=uuid4(),
                period_start=date(2024, 1, 31),
                period_end=date(2024, 1, 1),
                water_saved_liters=5000.0,
                cost_saved_rupees=15.0,
                traditional_usage_liters=15000.0,
                actual_usage_liters=10000.0
            )
        assert "period_end must be after period_start" in str(exc_info.value)

    def test_savings_record_create_inconsistent_savings(self):
        """Test savings record creation fails with inconsistent savings calculation."""
        with pytest.raises(ValidationError) as exc_info:
            SavingsRecordCreate(
                field_id=uuid4(),
                period_start=date(2024, 1, 1),
                period_end=date(2024, 1, 31),
                water_saved_liters=6000.0,  # Incorrect
                cost_saved_rupees=15.0,
                traditional_usage_liters=15000.0,
                actual_usage_liters=10000.0  # Should be 5000L saved
            )
        assert "water_saved_liters" in str(exc_info.value)

    def test_savings_record_create_cost_too_low(self):
        """Test savings record creation fails with cost rate below ₹2/1000L."""
        with pytest.raises(ValidationError) as exc_info:
            SavingsRecordCreate(
                field_id=uuid4(),
                period_start=date(2024, 1, 1),
                period_end=date(2024, 1, 31),
                water_saved_liters=5000.0,
                cost_saved_rupees=5.0,  # ₹1 per 1000L - too low
                traditional_usage_liters=15000.0,
                actual_usage_liters=10000.0
            )
        assert "between ₹2 and ₹5 per 1000 liters" in str(exc_info.value)

    def test_savings_record_create_cost_too_high(self):
        """Test savings record creation fails with cost rate above ₹5/1000L."""
        with pytest.raises(ValidationError) as exc_info:
            SavingsRecordCreate(
                field_id=uuid4(),
                period_start=date(2024, 1, 1),
                period_end=date(2024, 1, 31),
                water_saved_liters=5000.0,
                cost_saved_rupees=30.0,  # ₹6 per 1000L - too high
                traditional_usage_liters=15000.0,
                actual_usage_liters=10000.0
            )
        assert "between ₹2 and ₹5 per 1000 liters" in str(exc_info.value)

    def test_savings_record_create_valid_cost_range(self):
        """Test savings record creation with valid cost rates (₹2-5/1000L)."""
        # Test ₹2 per 1000L
        record1 = SavingsRecordCreate(
            field_id=uuid4(),
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            water_saved_liters=5000.0,
            cost_saved_rupees=10.0,
            traditional_usage_liters=15000.0,
            actual_usage_liters=10000.0
        )
        assert record1.cost_saved_rupees == 10.0

        # Test ₹5 per 1000L
        record2 = SavingsRecordCreate(
            field_id=uuid4(),
            period_start=date(2024, 1, 1),
            period_end=date(2024, 1, 31),
            water_saved_liters=5000.0,
            cost_saved_rupees=25.0,
            traditional_usage_liters=15000.0,
            actual_usage_liters=10000.0
        )
        assert record2.cost_saved_rupees == 25.0

    def test_savings_summary_valid(self):
        """Test creating a valid savings summary."""
        summary = SavingsSummary(
            total_water_saved_liters=15000.0,
            total_cost_saved_rupees=45.0,
            average_savings_percentage=33.3,
            number_of_periods=3
        )
        assert summary.total_water_saved_liters == 15000.0
        assert summary.number_of_periods == 3


class TestSerialization:
    """Test model serialization and deserialization."""

    def test_farmer_response_from_orm(self):
        """Test FarmerResponse can be created from ORM model."""
        # Simulate ORM model data
        farmer_data = {
            "id": uuid4(),
            "phone_number": "9876543210",
            "preferred_language": "hi",
            "sms_enabled": True,
            "created_at": datetime.utcnow(),
            "last_active": datetime.utcnow()
        }
        
        # This would normally be done with from_attributes=True
        farmer = FarmerResponse(**farmer_data)
        assert farmer.phone_number == "9876543210"

    def test_field_response_json_serialization(self):
        """Test FieldResponse JSON serialization."""
        field = FieldResponse(
            id=uuid4(),
            farmer_id=uuid4(),
            crop_type="wheat",
            field_size_acres=5.5,
            location_lat=28.6139,
            location_lng=77.2090,
            pincode="110001",
            irrigation_method="drip",
            planting_date=date(2024, 1, 15),
            created_at=datetime.utcnow()
        )
        
        # Test JSON serialization
        json_data = field.model_dump_json()
        assert "wheat" in json_data
        assert "5.5" in json_data

    def test_recommendation_response_with_complex_weather_data(self):
        """Test RecommendationResponse with complex weather data."""
        weather_data = {
            "temperature": 28.5,
            "humidity": 65,
            "rainfall_probability": 10,
            "wind_speed": 5.2,
            "forecast": ["sunny", "partly_cloudy"]
        }
        
        rec = RecommendationResponse(
            id=uuid4(),
            field_id=uuid4(),
            date=date(2024, 1, 20),
            irrigate=True,
            amount_mm=25.0,
            timing="evening",
            confidence=0.85,
            weather_data=weather_data,
            reasoning="Low soil moisture",
            localized_message="Test message",
            created_at=datetime.utcnow()
        )
        
        assert rec.weather_data["temperature"] == 28.5
        assert rec.weather_data["forecast"] == ["sunny", "partly_cloudy"]
