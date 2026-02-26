"""
Agricultural Terminology Dictionaries

Specialized agricultural terms for all supported languages.
These terms are commonly used in farming and irrigation contexts.
"""

from typing import Dict

# Agricultural terminology by language
AGRICULTURAL_TERMS: Dict[str, Dict[str, str]] = {
    "en": {
        # Soil terms
        "soil_moisture": "Soil Moisture",
        "soil_type": "Soil Type",
        "sandy_soil": "Sandy Soil",
        "clay_soil": "Clay Soil",
        "loamy_soil": "Loamy Soil",
        
        # Water terms
        "water_requirement": "Water Requirement",
        "evapotranspiration": "Evapotranspiration",
        "rainfall": "Rainfall",
        "groundwater": "Groundwater",
        
        # Crop stages
        "germination": "Germination",
        "vegetative": "Vegetative Stage",
        "flowering": "Flowering",
        "fruiting": "Fruiting",
        "maturity": "Maturity",
        
        # Irrigation terms
        "irrigation_efficiency": "Irrigation Efficiency",
        "water_application": "Water Application",
        "irrigation_schedule": "Irrigation Schedule",
        
        # Weather terms
        "temperature": "Temperature",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "forecast": "Forecast"
    },
    
    "hi": {
        # Soil terms
        "soil_moisture": "मिट्टी की नमी",
        "soil_type": "मिट्टी का प्रकार",
        "sandy_soil": "रेतीली मिट्टी",
        "clay_soil": "चिकनी मिट्टी",
        "loamy_soil": "दोमट मिट्टी",
        
        # Water terms
        "water_requirement": "पानी की आवश्यकता",
        "evapotranspiration": "वाष्पोत्सर्जन",
        "rainfall": "वर्षा",
        "groundwater": "भूजल",
        
        # Crop stages
        "germination": "अंकुरण",
        "vegetative": "वृद्धि अवस्था",
        "flowering": "फूल आना",
        "fruiting": "फल लगना",
        "maturity": "परिपक्वता",
        
        # Irrigation terms
        "irrigation_efficiency": "सिंचाई दक्षता",
        "water_application": "पानी देना",
        "irrigation_schedule": "सिंचाई कार्यक्रम",
        
        # Weather terms
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "wind_speed": "हवा की गति",
        "forecast": "पूर्वानुमान"
    },
    
    "mr": {
        # Soil terms
        "soil_moisture": "मातीची ओलावा",
        "soil_type": "मातीचा प्रकार",
        "sandy_soil": "वाळूमाती",
        "clay_soil": "चिकणमाती",
        "loamy_soil": "सुपीक माती",
        
        # Water terms
        "water_requirement": "पाण्याची गरज",
        "evapotranspiration": "बाष्पीभवन",
        "rainfall": "पाऊस",
        "groundwater": "भूजल",
        
        # Crop stages
        "germination": "उगवण",
        "vegetative": "वाढीचा टप्पा",
        "flowering": "फुलणे",
        "fruiting": "फळे येणे",
        "maturity": "परिपक्वता",
        
        # Irrigation terms
        "irrigation_efficiency": "सिंचन कार्यक्षमता",
        "water_application": "पाणी देणे",
        "irrigation_schedule": "सिंचन वेळापत्रक",
        
        # Weather terms
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "wind_speed": "वाऱ्याचा वेग",
        "forecast": "अंदाज"
    },
    
    "gu": {
        # Soil terms
        "soil_moisture": "માટીની ભેજ",
        "soil_type": "માટીનો પ્રકાર",
        "sandy_soil": "રેતાળ માટી",
        "clay_soil": "ચીકણી માટી",
        "loamy_soil": "ફળદ્રુપ માટી",
        
        # Water terms
        "water_requirement": "પાણીની જરૂરિયાત",
        "evapotranspiration": "બાષ્પીભવન",
        "rainfall": "વરસાદ",
        "groundwater": "ભૂગર્ભજળ",
        
        # Crop stages
        "germination": "અંકુરણ",
        "vegetative": "વૃદ્ધિ તબક્કો",
        "flowering": "ફૂલ આવવું",
        "fruiting": "ફળ આવવું",
        "maturity": "પરિપક્વતા",
        
        # Irrigation terms
        "irrigation_efficiency": "સિંચાઈ કાર્યક્ષમતા",
        "water_application": "પાણી આપવું",
        "irrigation_schedule": "સિંચાઈ સમયપત્રક",
        
        # Weather terms
        "temperature": "તાપમાન",
        "humidity": "ભેજ",
        "wind_speed": "પવનની ઝડપ",
        "forecast": "આગાહી"
    },
    
    "pa": {
        # Soil terms
        "soil_moisture": "ਮਿੱਟੀ ਦੀ ਨਮੀ",
        "soil_type": "ਮਿੱਟੀ ਦੀ ਕਿਸਮ",
        "sandy_soil": "ਰੇਤਲੀ ਮਿੱਟੀ",
        "clay_soil": "ਚਿਕਨੀ ਮਿੱਟੀ",
        "loamy_soil": "ਉਪਜਾਊ ਮਿੱਟੀ",
        
        # Water terms
        "water_requirement": "ਪਾਣੀ ਦੀ ਲੋੜ",
        "evapotranspiration": "ਵਾਸ਼ਪੀਕਰਨ",
        "rainfall": "ਬਾਰਿਸ਼",
        "groundwater": "ਭੂਮੀਗਤ ਪਾਣੀ",
        
        # Crop stages
        "germination": "ਉਗਣਾ",
        "vegetative": "ਵਾਧਾ ਪੜਾਅ",
        "flowering": "ਫੁੱਲ ਆਉਣਾ",
        "fruiting": "ਫਲ ਲੱਗਣਾ",
        "maturity": "ਪੱਕਣਾ",
        
        # Irrigation terms
        "irrigation_efficiency": "ਸਿੰਚਾਈ ਕੁਸ਼ਲਤਾ",
        "water_application": "ਪਾਣੀ ਦੇਣਾ",
        "irrigation_schedule": "ਸਿੰਚਾਈ ਸਮਾਂ-ਸਾਰਣੀ",
        
        # Weather terms
        "temperature": "ਤਾਪਮਾਨ",
        "humidity": "ਨਮੀ",
        "wind_speed": "ਹਵਾ ਦੀ ਗਤੀ",
        "forecast": "ਪੂਰਵ-ਅਨੁਮਾਨ"
    },
    
    "ta": {
        # Soil terms
        "soil_moisture": "மண் ஈரப்பதம்",
        "soil_type": "மண் வகை",
        "sandy_soil": "மணல் மண்",
        "clay_soil": "களிமண்",
        "loamy_soil": "வளமான மண்",
        
        # Water terms
        "water_requirement": "நீர் தேவை",
        "evapotranspiration": "ஆவியாதல்",
        "rainfall": "மழை",
        "groundwater": "நிலத்தடி நீர்",
        
        # Crop stages
        "germination": "முளைப்பு",
        "vegetative": "வளர்ச்சி நிலை",
        "flowering": "பூக்கும் காலம்",
        "fruiting": "கனி காலம்",
        "maturity": "முதிர்ச்சி",
        
        # Irrigation terms
        "irrigation_efficiency": "நீர்ப்பாசன திறன்",
        "water_application": "நீர் வழங்கல்",
        "irrigation_schedule": "நீர்ப்பாசன அட்டவணை",
        
        # Weather terms
        "temperature": "வெப்பநிலை",
        "humidity": "ஈரப்பதம்",
        "wind_speed": "காற்றின் வேகம்",
        "forecast": "முன்னறிவிப்பு"
    },
    
    "te": {
        # Soil terms
        "soil_moisture": "నేల తేమ",
        "soil_type": "నేల రకం",
        "sandy_soil": "ఇసుక నేల",
        "clay_soil": "బంకమట్టి",
        "loamy_soil": "సారవంతమైన నేల",
        
        # Water terms
        "water_requirement": "నీటి అవసరం",
        "evapotranspiration": "ఆవిరీభవనం",
        "rainfall": "వర్షపాతం",
        "groundwater": "భూగర్భ జలం",
        
        # Crop stages
        "germination": "మొలకెత్తడం",
        "vegetative": "పెరుగుదల దశ",
        "flowering": "పుష్పించడం",
        "fruiting": "ఫలించడం",
        "maturity": "పరిపక్వత",
        
        # Irrigation terms
        "irrigation_efficiency": "నీటిపారుదల సామర్థ్యం",
        "water_application": "నీరు అందించడం",
        "irrigation_schedule": "నీటిపారుదల షెడ్యూల్",
        
        # Weather terms
        "temperature": "ఉష్ణోగ్రత",
        "humidity": "తేమ",
        "wind_speed": "గాలి వేగం",
        "forecast": "అంచనా"
    },
    
    "kn": {
        # Soil terms
        "soil_moisture": "ಮಣ್ಣಿನ ತೇವಾಂಶ",
        "soil_type": "ಮಣ್ಣಿನ ವಿಧ",
        "sandy_soil": "ಮರಳು ಮಣ್ಣು",
        "clay_soil": "ಜೇಡಿಮಣ್ಣು",
        "loamy_soil": "ಫಲವತ್ತಾದ ಮಣ್ಣು",
        
        # Water terms
        "water_requirement": "ನೀರಿನ ಅವಶ್ಯಕತೆ",
        "evapotranspiration": "ಆವಿಯಾಗುವಿಕೆ",
        "rainfall": "ಮಳೆ",
        "groundwater": "ಅಂತರ್ಜಲ",
        
        # Crop stages
        "germination": "ಮೊಳಕೆಯೊಡೆಯುವಿಕೆ",
        "vegetative": "ಬೆಳವಣಿಗೆ ಹಂತ",
        "flowering": "ಹೂಬಿಡುವಿಕೆ",
        "fruiting": "ಫಲಿಸುವಿಕೆ",
        "maturity": "ಪಕ್ವತೆ",
        
        # Irrigation terms
        "irrigation_efficiency": "ನೀರಾವರಿ ದಕ್ಷತೆ",
        "water_application": "ನೀರು ನೀಡುವಿಕೆ",
        "irrigation_schedule": "ನೀರಾವರಿ ವೇಳಾಪಟ್ಟಿ",
        
        # Weather terms
        "temperature": "ತಾಪಮಾನ",
        "humidity": "ತೇವಾಂಶ",
        "wind_speed": "ಗಾಳಿಯ ವೇಗ",
        "forecast": "ಮುನ್ಸೂಚನೆ"
    }
}


def get_agricultural_term(term: str, language: str) -> str:
    """
    Get agricultural term in specified language
    
    Args:
        term: Term key (e.g., "soil_moisture")
        language: Language code
    
    Returns:
        Translated term or original term if not found
    """
    if language in AGRICULTURAL_TERMS and term in AGRICULTURAL_TERMS[language]:
        return AGRICULTURAL_TERMS[language][term]
    
    # Fallback to English
    if term in AGRICULTURAL_TERMS.get("en", {}):
        return AGRICULTURAL_TERMS["en"][term]
    
    return term
