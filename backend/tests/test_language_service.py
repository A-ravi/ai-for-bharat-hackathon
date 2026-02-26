"""
Unit tests for Language Service

Tests language detection, switching, translation, and message formatting.
"""

import pytest
from app.services import (
    LanguageService,
    Language,
    get_language_service,
    get_agricultural_term,
    AGRICULTURAL_TERMS
)


class TestLanguageService:
    """Test suite for LanguageService"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.service = LanguageService()
    
    def test_supported_languages(self):
        """Test that all 8 languages are supported"""
        supported = [lang.value for lang in Language]
        assert len(supported) == 8
        assert "hi" in supported  # Hindi
        assert "en" in supported  # English
        assert "mr" in supported  # Marathi
        assert "gu" in supported  # Gujarati
        assert "pa" in supported  # Punjabi
        assert "ta" in supported  # Tamil
        assert "te" in supported  # Telugu
        assert "kn" in supported  # Kannada
    
    def test_is_supported_language(self):
        """Test language support checking"""
        assert self.service.is_supported_language("en")
        assert self.service.is_supported_language("hi")
        assert self.service.is_supported_language("ta")
        assert not self.service.is_supported_language("fr")
        assert not self.service.is_supported_language("invalid")
    
    def test_get_text_english(self):
        """Test getting text in English"""
        text = self.service.get_text("onboarding.welcome", "en")
        assert text == "Welcome to Jal Sathi"
    
    def test_get_text_hindi(self):
        """Test getting text in Hindi"""
        text = self.service.get_text("onboarding.welcome", "hi")
        assert "जल साथी" in text
    
    def test_get_text_all_languages(self):
        """Test getting text in all supported languages"""
        for lang in Language:
            text = self.service.get_text("onboarding.welcome", lang.value)
            assert text is not None
            assert len(text) > 0
            assert text != "[onboarding.welcome]"  # Should not be fallback
    
    def test_get_text_with_template_substitution(self):
        """Test template variable substitution"""
        message = self.service.get_text(
            "recommendation.irrigate",
            "en",
            amount=25,
            timing="evening"
        )
        assert "25" in message
        assert "evening" in message
    
    def test_get_text_fallback_to_english(self):
        """Test fallback to English for unsupported language"""
        text = self.service.get_text("onboarding.welcome", "unsupported_lang")
        assert text == "Welcome to Jal Sathi"
    
    def test_get_text_missing_key(self):
        """Test handling of missing translation key"""
        text = self.service.get_text("nonexistent.key", "en")
        assert "[nonexistent.key]" in text
    
    def test_get_crop_name_english(self):
        """Test getting crop names in English"""
        assert self.service.get_crop_name("rice", "en") == "Rice"
        assert self.service.get_crop_name("wheat", "en") == "Wheat"
        assert self.service.get_crop_name("cotton", "en") == "Cotton"
    
    def test_get_crop_name_hindi(self):
        """Test getting crop names in Hindi"""
        rice = self.service.get_crop_name("rice", "hi")
        assert rice == "धान"
        
        wheat = self.service.get_crop_name("wheat", "hi")
        assert wheat == "गेहूं"
    
    def test_get_crop_name_all_languages(self):
        """Test crop names available in all languages"""
        crops = ["rice", "wheat", "cotton", "sugarcane"]
        for lang in Language:
            for crop in crops:
                name = self.service.get_crop_name(crop, lang.value)
                assert name is not None
                assert len(name) > 0
    
    def test_get_irrigation_method_english(self):
        """Test getting irrigation method names in English"""
        assert self.service.get_irrigation_method("drip", "en") == "Drip Irrigation"
        assert self.service.get_irrigation_method("sprinkler", "en") == "Sprinkler"
        assert self.service.get_irrigation_method("flood", "en") == "Flood Irrigation"
    
    def test_get_irrigation_method_regional(self):
        """Test irrigation methods in regional languages"""
        # Hindi
        drip_hi = self.service.get_irrigation_method("drip", "hi")
        assert "ड्रिप" in drip_hi
        
        # Tamil
        drip_ta = self.service.get_irrigation_method("drip", "ta")
        assert "சொட்டு" in drip_ta
    
    def test_format_recommendation_message_irrigate(self):
        """Test formatting irrigation recommendation (irrigate=True)"""
        message = self.service.format_recommendation_message(
            language="en",
            irrigate=True,
            amount_mm=25.0,
            timing="evening"
        )
        assert "25" in message
        assert "evening" in message
    
    def test_format_recommendation_message_no_irrigate(self):
        """Test formatting irrigation recommendation (irrigate=False)"""
        message = self.service.format_recommendation_message(
            language="en",
            irrigate=False,
            amount_mm=0,
            timing="morning"
        )
        assert "No irrigation needed" in message
    
    def test_format_recommendation_message_with_reasoning(self):
        """Test recommendation message with reasoning"""
        message = self.service.format_recommendation_message(
            language="en",
            irrigate=True,
            amount_mm=20.0,
            timing="morning",
            reasoning="Low soil moisture detected"
        )
        assert "20" in message
        assert "Low soil moisture detected" in message
    
    def test_format_recommendation_all_languages(self):
        """Test recommendation formatting in all languages"""
        for lang in Language:
            message = self.service.format_recommendation_message(
                language=lang.value,
                irrigate=True,
                amount_mm=25.0,
                timing="evening"
            )
            assert message is not None
            assert len(message) > 0
    
    def test_format_sms_message_irrigate(self):
        """Test SMS message formatting for irrigation"""
        sms = self.service.format_sms_message(
            language="en",
            irrigate=True,
            amount_mm=20.0,
            timing="evening"
        )
        assert len(sms) <= 160  # SMS character limit
        assert "20" in sms
        assert "Jal Sathi" in sms
    
    def test_format_sms_message_no_irrigate(self):
        """Test SMS message formatting for no irrigation"""
        sms = self.service.format_sms_message(
            language="en",
            irrigate=False,
            amount_mm=0,
            timing="morning"
        )
        assert len(sms) <= 160
        assert "Jal Sathi" in sms
    
    def test_format_sms_message_character_limit(self):
        """Test that SMS messages respect 160 character limit"""
        for lang in Language:
            sms = self.service.format_sms_message(
                language=lang.value,
                irrigate=True,
                amount_mm=25.0,
                timing="evening"
            )
            assert len(sms) <= 160, f"SMS too long for {lang.value}: {len(sms)} chars"
    
    def test_format_sms_message_hindi(self):
        """Test SMS formatting in Hindi"""
        sms = self.service.format_sms_message(
            language="hi",
            irrigate=True,
            amount_mm=25.0,
            timing="evening"
        )
        assert "25" in sms
        assert "जल साथी" in sms
        assert len(sms) <= 160
    
    def test_get_savings_message(self):
        """Test savings message formatting"""
        message = self.service.get_savings_message(
            language="en",
            water_saved_liters=1000.0,
            cost_saved_rupees=50.0
        )
        assert "1000" in message
        assert "50" in message
    
    def test_get_savings_message_all_languages(self):
        """Test savings messages in all languages"""
        for lang in Language:
            message = self.service.get_savings_message(
                language=lang.value,
                water_saved_liters=500.0,
                cost_saved_rupees=25.0
            )
            assert message is not None
            assert "500" in message or "25" in message
    
    def test_get_milestone_message(self):
        """Test milestone congratulatory messages"""
        message = self.service.get_milestone_message(
            language="en",
            milestone_type="water",
            value=10000.0
        )
        assert "10000" in message
        assert "Congratulations" in message or "congratulations" in message.lower()
    
    def test_get_milestone_message_cost(self):
        """Test cost milestone messages"""
        message = self.service.get_milestone_message(
            language="en",
            milestone_type="cost",
            value=500.0
        )
        assert "500" in message
    
    def test_get_supported_languages_list(self):
        """Test getting list of supported languages"""
        languages = self.service.get_supported_languages()
        assert len(languages) == 8
        assert all("code" in lang and "name" in lang for lang in languages)
    
    def test_singleton_pattern(self):
        """Test that get_language_service returns singleton"""
        service1 = get_language_service()
        service2 = get_language_service()
        assert service1 is service2


class TestAgriculturalTerms:
    """Test suite for agricultural terminology"""
    
    def test_agricultural_terms_all_languages(self):
        """Test that agricultural terms exist for all languages"""
        for lang in Language:
            assert lang.value in AGRICULTURAL_TERMS
            assert len(AGRICULTURAL_TERMS[lang.value]) > 0
    
    def test_get_agricultural_term_english(self):
        """Test getting agricultural terms in English"""
        assert get_agricultural_term("soil_moisture", "en") == "Soil Moisture"
        assert get_agricultural_term("rainfall", "en") == "Rainfall"
        assert get_agricultural_term("germination", "en") == "Germination"
    
    def test_get_agricultural_term_hindi(self):
        """Test getting agricultural terms in Hindi"""
        term = get_agricultural_term("soil_moisture", "hi")
        assert "मिट्टी" in term
        
        term = get_agricultural_term("rainfall", "hi")
        assert "वर्षा" in term
    
    def test_get_agricultural_term_all_languages(self):
        """Test agricultural terms in all languages"""
        terms = ["soil_moisture", "rainfall", "temperature", "germination"]
        for lang in Language:
            for term in terms:
                result = get_agricultural_term(term, lang.value)
                assert result is not None
                assert len(result) > 0
    
    def test_get_agricultural_term_fallback(self):
        """Test fallback to English for missing term"""
        result = get_agricultural_term("nonexistent_term", "hi")
        assert result == "nonexistent_term"
    
    def test_agricultural_terms_consistency(self):
        """Test that all languages have the same set of terms"""
        english_terms = set(AGRICULTURAL_TERMS["en"].keys())
        for lang in Language:
            if lang.value != "en":
                lang_terms = set(AGRICULTURAL_TERMS[lang.value].keys())
                assert english_terms == lang_terms, f"Terms mismatch for {lang.value}"


class TestLanguageEdgeCases:
    """Test edge cases and error handling"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.service = LanguageService()
    
    def test_empty_language_code(self):
        """Test handling of empty language code"""
        text = self.service.get_text("onboarding.welcome", "")
        assert text == "Welcome to Jal Sathi"  # Should fallback to English
    
    def test_none_language_code(self):
        """Test handling of None language code"""
        # This should raise an error or handle gracefully
        try:
            text = self.service.get_text("onboarding.welcome", None)
            # If it doesn't raise, it should fallback
            assert text is not None
        except (TypeError, KeyError):
            pass  # Expected behavior
    
    def test_special_characters_in_messages(self):
        """Test that special characters are preserved"""
        for lang in Language:
            text = self.service.get_text("savings.message", lang.value, water=100, cost=5)
            assert "₹" in text  # Rupee symbol should be present
    
    def test_numeric_formatting_in_templates(self):
        """Test numeric value formatting in templates"""
        message = self.service.format_recommendation_message(
            language="en",
            irrigate=True,
            amount_mm=25.5,
            timing="morning"
        )
        assert "25.5" in message
    
    def test_unicode_handling(self):
        """Test proper Unicode handling for all languages"""
        for lang in Language:
            text = self.service.get_text("onboarding.welcome", lang.value)
            # Should not raise encoding errors
            assert isinstance(text, str)
            encoded = text.encode('utf-8')
            decoded = encoded.decode('utf-8')
            assert decoded == text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
