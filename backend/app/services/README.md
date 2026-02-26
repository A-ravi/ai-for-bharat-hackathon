# Language Service

Multi-language support system for Jal Sathi, providing translations and localized content for 8 Indian languages.

## Supported Languages

- **Hindi (hi)** - हिंदी
- **English (en)** - English
- **Marathi (mr)** - मराठी
- **Gujarati (gu)** - ગુજરાતી
- **Punjabi (pa)** - ਪੰਜਾਬੀ
- **Tamil (ta)** - தமிழ்
- **Telugu (te)** - తెలుగు
- **Kannada (kn)** - ಕನ್ನಡ

## Features

### 1. Language Detection and Switching
- Automatic language detection based on user preference
- Seamless switching between languages
- Fallback to English for unsupported languages

### 2. Translation Files
- JSON-based translation files for each language
- Organized by feature area (onboarding, recommendations, savings, etc.)
- Template-based message generation with variable substitution

### 3. Agricultural Terminology
- Specialized dictionaries for agricultural terms
- Consistent terminology across all languages
- Terms for soil, water, crops, irrigation, and weather

### 4. Message Formatting
- Recommendation messages with irrigation advice
- SMS messages optimized for 160-character limit
- Savings tracking messages
- Milestone celebration messages

## Usage

### Basic Translation

```python
from app.services import get_language_service

service = get_language_service()

# Get translated text
welcome = service.get_text("onboarding.welcome", "hi")
# Output: "जल साथी में आपका स्वागत है"

# With template variables
message = service.get_text(
    "recommendation.irrigate",
    "en",
    amount=25,
    timing="evening"
)
# Output: "Water your field 25mm this evening."
```

### Crop Names

```python
# Get localized crop names
rice_hindi = service.get_crop_name("rice", "hi")
# Output: "धान"

wheat_tamil = service.get_crop_name("wheat", "ta")
# Output: "கோதுமை"
```

### Irrigation Methods

```python
# Get localized irrigation method names
drip_gujarati = service.get_irrigation_method("drip", "gu")
# Output: "ટીપું સિંચાઈ"
```

### Recommendation Messages

```python
# Format irrigation recommendation
message = service.format_recommendation_message(
    language="hi",
    irrigate=True,
    amount_mm=25.0,
    timing="evening",
    reasoning="Low soil moisture"
)
# Output: "आज शाम 25मिमी पानी दें। कारण: Low soil moisture"
```

### SMS Messages

```python
# Format SMS (optimized for 160 characters)
sms = service.format_sms_message(
    language="pa",
    irrigate=True,
    amount_mm=20.0,
    timing="morning"
)
# Output: "ਅੱਜ ਸਵੇਰੇ 20ਮਿਮੀ ਪਾਣੀ ਦਿਓ। -ਜਲ ਸਾਥੀ"
```

### Savings Messages

```python
# Format savings message
savings = service.get_savings_message(
    language="mr",
    water_saved_liters=1000.0,
    cost_saved_rupees=50.0
)
# Output: "तुम्ही 1000ली पाणी आणि ₹50 वाचवले!"
```

### Milestone Messages

```python
# Get milestone celebration message
milestone = service.get_milestone_message(
    language="te",
    milestone_type="water",
    value=10000.0
)
# Output: "అభినందనలు! మీరు 10000లీ నీరు ఆదా చేశారు!"
```

### Agricultural Terms

```python
from app.services import get_agricultural_term

# Get agricultural terminology
soil_moisture_kn = get_agricultural_term("soil_moisture", "kn")
# Output: "ಮಣ್ಣಿನ ತೇವಾಂಶ"

rainfall_gu = get_agricultural_term("rainfall", "gu")
# Output: "વરસાદ"
```

## Translation File Structure

Translation files are located in `backend/app/services/translations/` and follow this structure:

```json
{
  "languages": {
    "hi": "हिंदी",
    "en": "English",
    ...
  },
  "onboarding": {
    "welcome": "Welcome to Jal Sathi",
    "crop_type": "What crop are you growing?",
    ...
  },
  "crops": {
    "rice": "Rice",
    "wheat": "Wheat",
    ...
  },
  "recommendation": {
    "irrigate": "Water your field {amount}mm this {timing}.",
    "no_irrigate": "No irrigation needed today."
  },
  "sms": {
    "irrigate": "Water {amount}mm {timing}. -Jal Sathi",
    "no_irrigate": "No water needed today. -Jal Sathi"
  },
  ...
}
```

## Adding New Translations

To add a new translation:

1. Add the key-value pair to `en.json` first
2. Add corresponding translations to all other language files
3. Use template variables with `{variable_name}` for dynamic content
4. Test with the language service

Example:
```json
{
  "new_feature": {
    "message": "Hello {name}, your field is {size} acres."
  }
}
```

## SMS Character Limits

SMS messages are automatically truncated to 160 characters to ensure single-SMS delivery:

- Messages longer than 160 characters are truncated with "..."
- All language translations are optimized to fit within this limit
- Unicode characters (Devanagari, Tamil, etc.) are properly handled

## Testing

Run the test suite:

```bash
cd backend
pytest tests/test_language_service.py -v
```

Test coverage includes:
- All 8 supported languages
- Translation retrieval and fallback
- Template variable substitution
- SMS character limits
- Agricultural terminology
- Unicode handling
- Edge cases and error handling

## Requirements Validation

This implementation validates:
- **Requirement 1.1**: Regional language onboarding flow
- **Requirement 1.2**: Support for 8 Indian languages
- **Requirement 2.3**: Recommendations in farmer's selected language
- **Requirement 8.4**: Web app text in regional languages

## Architecture

The language service uses:
- **Singleton pattern** for efficient resource usage
- **JSON files** for easy translation management
- **Template-based generation** for dynamic content
- **Fallback mechanism** for missing translations
- **UTF-8 encoding** for proper Unicode support

## Performance

- Translations are loaded once at startup
- In-memory dictionary lookups (O(1) complexity)
- No database queries required
- Minimal overhead for message generation
