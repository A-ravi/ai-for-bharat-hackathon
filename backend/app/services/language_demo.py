"""
Language Service Demo

Demonstrates the multi-language support capabilities of Jal Sathi.
Run this script to see translations in all 8 supported languages.
"""

from language_service import get_language_service, Language
from agricultural_terms import get_agricultural_term


def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_welcome_messages():
    """Demo welcome messages in all languages"""
    print_section("Welcome Messages in All Languages")
    
    service = get_language_service()
    
    for lang in Language:
        welcome = service.get_text("onboarding.welcome", lang.value)
        lang_name = service.get_text(f"languages.{lang.value}", Language.ENGLISH.value)
        print(f"{lang_name:12} ({lang.value}): {welcome}")


def demo_crop_names():
    """Demo crop names in different languages"""
    print_section("Crop Names in Different Languages")
    
    service = get_language_service()
    crops = ["rice", "wheat", "cotton", "sugarcane"]
    languages = ["en", "hi", "ta", "kn"]
    
    print(f"{'Crop':<12} ", end="")
    for lang in languages:
        lang_name = service.get_text(f"languages.{lang}", "en")
        print(f"{lang_name:<15}", end="")
    print()
    print("-" * 60)
    
    for crop in crops:
        print(f"{crop.capitalize():<12} ", end="")
        for lang in languages:
            crop_name = service.get_crop_name(crop, lang)
            print(f"{crop_name:<15}", end="")
        print()


def demo_recommendation_messages():
    """Demo irrigation recommendation messages"""
    print_section("Irrigation Recommendation Messages")
    
    service = get_language_service()
    
    print("\nScenario: Irrigate 25mm in the evening\n")
    
    for lang in ["en", "hi", "mr", "gu"]:
        lang_name = service.get_text(f"languages.{lang}", "en")
        message = service.format_recommendation_message(
            language=lang,
            irrigate=True,
            amount_mm=25.0,
            timing="evening"
        )
        print(f"{lang_name:12}: {message}")
    
    print("\nScenario: No irrigation needed\n")
    
    for lang in ["en", "hi", "ta", "te"]:
        lang_name = service.get_text(f"languages.{lang}", "en")
        message = service.format_recommendation_message(
            language=lang,
            irrigate=False,
            amount_mm=0,
            timing="morning"
        )
        print(f"{lang_name:12}: {message}")


def demo_sms_messages():
    """Demo SMS message formatting"""
    print_section("SMS Messages (160 Character Limit)")
    
    service = get_language_service()
    
    print("\nIrrigation SMS in different languages:\n")
    
    for lang in Language:
        lang_name = service.get_text(f"languages.{lang.value}", "en")
        sms = service.format_sms_message(
            language=lang.value,
            irrigate=True,
            amount_mm=20.0,
            timing="evening"
        )
        char_count = len(sms)
        print(f"{lang_name:12} ({char_count:3} chars): {sms}")


def demo_savings_messages():
    """Demo savings tracking messages"""
    print_section("Savings Messages")
    
    service = get_language_service()
    
    print("\nYou saved 1000L water and ₹50:\n")
    
    for lang in ["en", "hi", "pa", "kn"]:
        lang_name = service.get_text(f"languages.{lang}", "en")
        message = service.get_savings_message(
            language=lang,
            water_saved_liters=1000.0,
            cost_saved_rupees=50.0
        )
        print(f"{lang_name:12}: {message}")


def demo_milestone_messages():
    """Demo milestone celebration messages"""
    print_section("Milestone Celebration Messages")
    
    service = get_language_service()
    
    print("\nWater milestone (10,000L saved):\n")
    
    for lang in ["en", "hi", "mr", "gu"]:
        lang_name = service.get_text(f"languages.{lang}", "en")
        message = service.get_milestone_message(
            language=lang,
            milestone_type="water",
            value=10000.0
        )
        print(f"{lang_name:12}: {message}")


def demo_agricultural_terms():
    """Demo agricultural terminology"""
    print_section("Agricultural Terminology")
    
    terms = ["soil_moisture", "rainfall", "germination", "temperature"]
    languages = ["en", "hi", "ta", "kn"]
    
    print(f"{'Term':<20} ", end="")
    for lang in languages:
        service = get_language_service()
        lang_name = service.get_text(f"languages.{lang}", "en")
        print(f"{lang_name:<20}", end="")
    print()
    print("-" * 80)
    
    for term in terms:
        print(f"{term:<20} ", end="")
        for lang in languages:
            translated = get_agricultural_term(term, lang)
            print(f"{translated:<20}", end="")
        print()


def demo_irrigation_methods():
    """Demo irrigation method names"""
    print_section("Irrigation Methods")
    
    service = get_language_service()
    methods = ["drip", "sprinkler", "flood"]
    
    print(f"{'Method':<12} ", end="")
    for lang in ["en", "hi", "gu", "pa"]:
        lang_name = service.get_text(f"languages.{lang}", "en")
        print(f"{lang_name:<20}", end="")
    print()
    print("-" * 72)
    
    for method in methods:
        print(f"{method.capitalize():<12} ", end="")
        for lang in ["en", "hi", "gu", "pa"]:
            method_name = service.get_irrigation_method(method, lang)
            print(f"{method_name:<20}", end="")
        print()


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("  JAL SATHI - MULTI-LANGUAGE SUPPORT DEMO")
    print("  Supporting 8 Indian Languages")
    print("=" * 60)
    
    demo_welcome_messages()
    demo_crop_names()
    demo_recommendation_messages()
    demo_sms_messages()
    demo_savings_messages()
    demo_milestone_messages()
    demo_agricultural_terms()
    demo_irrigation_methods()
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
