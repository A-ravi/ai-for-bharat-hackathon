"""
Language Service for Jal Sathi

Provides multi-language support for 8 Indian languages with template-based
message generation and agricultural terminology dictionaries.

Supported Languages:
- Hindi (hi)
- English (en)
- Marathi (mr)
- Gujarati (gu)
- Punjabi (pa)
- Tamil (ta)
- Telugu (te)
- Kannada (kn)
"""

from typing import Dict, Any, Optional
from enum import Enum
import json
from pathlib import Path


class Language(str, Enum):
    """Supported languages"""
    HINDI = "hi"
    ENGLISH = "en"
    MARATHI = "mr"
    GUJARATI = "gu"
    PUNJABI = "pa"
    TAMIL = "ta"
    TELUGU = "te"
    KANNADA = "kn"


class LanguageService:
    """Service for handling multi-language support"""
    
    def __init__(self):
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.agricultural_terms: Dict[str, Dict[str, str]] = {}
        self._load_translations()
        self._load_agricultural_terms()
    
    def _load_translations(self):
        """Load translation files for all supported languages"""
        translations_dir = Path(__file__).parent / "translations"
        
        for lang in Language:
            translation_file = translations_dir / f"{lang.value}.json"
            if translation_file.exists():
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations[lang.value] = json.load(f)
            else:
                self.translations[lang.value] = {}
    
    def _load_agricultural_terms(self):
        """Load agricultural terminology dictionaries"""
        # Initialize with empty dicts
        for lang in Language:
            self.agricultural_terms[lang.value] = {}
    
    def get_text(self, key: str, language: str, **kwargs) -> str:
        """
        Get translated text for a given key and language
        
        Args:
            key: Translation key (e.g., "onboarding.welcome")
            language: Language code
            **kwargs: Variables for template substitution
        
        Returns:
            Translated text with variables substituted
        """
        if language not in self.translations:
            language = Language.ENGLISH.value
        
        # Navigate nested keys (e.g., "onboarding.welcome")
        keys = key.split(".")
        value = self.translations[language]
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Fallback to English if key not found
                value = self._get_fallback_text(key)
                break
        
        # Perform template substitution
        if isinstance(value, str) and kwargs:
            try:
                value = value.format(**kwargs)
            except KeyError:
                pass  # Return unsubstituted if variables missing
        
        return str(value)
    
    def _get_fallback_text(self, key: str) -> str:
        """Get fallback text in English"""
        keys = key.split(".")
        value = self.translations.get(Language.ENGLISH.value, {})
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return f"[{key}]"  # Return key if not found
        
        return str(value)
    
    def get_crop_name(self, crop_type: str, language: str) -> str:
        """Get localized crop name"""
        crop_key = f"crops.{crop_type}"
        return self.get_text(crop_key, language)
    
    def get_irrigation_method(self, method: str, language: str) -> str:
        """Get localized irrigation method name"""
        method_key = f"irrigation_methods.{method}"
        return self.get_text(method_key, language)
    
    def format_recommendation_message(
        self,
        language: str,
        irrigate: bool,
        amount_mm: float,
        timing: str,
        reasoning: str = ""
    ) -> str:
        """
        Format irrigation recommendation message
        
        Args:
            language: Language code
            irrigate: Whether to irrigate
            amount_mm: Water amount in millimeters
            timing: Timing (morning/afternoon/evening)
            reasoning: Optional reasoning text
        
        Returns:
            Formatted recommendation message
        """
        if irrigate:
            template_key = "recommendation.irrigate"
            message = self.get_text(
                template_key,
                language,
                amount=amount_mm,
                timing=self.get_text(f"timing.{timing}", language)
            )
        else:
            template_key = "recommendation.no_irrigate"
            message = self.get_text(template_key, language)
        
        if reasoning:
            message += " " + reasoning
        
        return message
    
    def format_sms_message(
        self,
        language: str,
        irrigate: bool,
        amount_mm: float,
        timing: str
    ) -> str:
        """
        Format SMS message (optimized for 160 characters)
        
        Args:
            language: Language code
            irrigate: Whether to irrigate
            amount_mm: Water amount in millimeters
            timing: Timing (morning/afternoon/evening)
        
        Returns:
            SMS message within 160 characters
        """
        if irrigate:
            template_key = "sms.irrigate"
            message = self.get_text(
                template_key,
                language,
                amount=amount_mm,
                timing=self.get_text(f"timing.{timing}", language)
            )
        else:
            template_key = "sms.no_irrigate"
            message = self.get_text(template_key, language)
        
        # Ensure message is within 160 characters
        if len(message) > 160:
            message = message[:157] + "..."
        
        return message
    
    def get_savings_message(
        self,
        language: str,
        water_saved_liters: float,
        cost_saved_rupees: float
    ) -> str:
        """
        Format savings message
        
        Args:
            language: Language code
            water_saved_liters: Water saved in liters
            cost_saved_rupees: Cost saved in rupees
        
        Returns:
            Formatted savings message
        """
        return self.get_text(
            "savings.message",
            language,
            water=water_saved_liters,
            cost=cost_saved_rupees
        )
    
    def get_milestone_message(
        self,
        language: str,
        milestone_type: str,
        value: float
    ) -> str:
        """
        Get congratulatory milestone message
        
        Args:
            language: Language code
            milestone_type: Type of milestone (water/cost)
            value: Milestone value
        
        Returns:
            Congratulatory message
        """
        return self.get_text(
            f"milestones.{milestone_type}",
            language,
            value=value
        )
    
    def is_supported_language(self, language: str) -> bool:
        """Check if language is supported"""
        return language in [lang.value for lang in Language]
    
    def get_supported_languages(self) -> list[Dict[str, str]]:
        """Get list of supported languages with names"""
        return [
            {"code": lang.value, "name": self.get_text(f"languages.{lang.value}", Language.ENGLISH.value)}
            for lang in Language
        ]


# Singleton instance
_language_service: Optional[LanguageService] = None


def get_language_service() -> LanguageService:
    """Get or create language service singleton"""
    global _language_service
    if _language_service is None:
        _language_service = LanguageService()
    return _language_service
