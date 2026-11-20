"""Bilingual translations (English & Malayalam) for KrishiMitra Kerala.
"""

TRANSLATIONS = {
    # App titles and headers
    "app_title": {
        "English": "🌱 കൃഷിമിത്രം | KrishiMitra Kerala",
        "Malayalam": "🌱 കൃഷിമിത്രം | KrishiMitra Kerala"
    },
    "app_subtitle": {
        "English": "Intelligent Agricultural Advisory for Kerala Farmers",
        "Malayalam": "കേരളത്തിലെ കർഷകർക്കായുള്ള സമഗ്ര കാർഷിക മാർഗ്ഗനിർദ്ദേശം"
    },
    "app_welcome": {
        "English": "Welcome to KrishiMitra Kerala, a unified decision support platform tailored to Kerala's agro-climatic zones, powered by Kerala Agricultural University (KAU) Package of Practices.",
        "Malayalam": "കേരള കാർഷിക സർവകലാശാലയുടെ (KAU) കൃഷിരീതികളെ അടിസ്ഥാനമാക്കി, കേരളത്തിലെ കർഷകർക്കായി തയ്യാറാക്കിയ സമഗ്ര കാർഷിക സഹായിയിലേക്ക് സ്വാഗതം."
    },
    
    # Sidebar
    "sidebar_title": {
        "English": "🌱 KrishiMitra",
        "Malayalam": "🌱 കൃഷിമിത്രം"
    },
    "language_label": {
        "English": "Language / ഭാഷ",
        "Malayalam": "ഭാഷ / Language"
    },
    "district_label": {
        "English": "District / ജില്ല",
        "Malayalam": "ജില്ല / District"
    },
    "crop_label": {
        "English": "Primary Crop / വിള",
        "Malayalam": "പ്രധാന വിള / Primary Crop"
    },
    "navigation_label": {
        "English": "Navigation",
        "Malayalam": "വിഭാഗങ്ങൾ"
    },
    
    # Navigation Page Names
    "nav_home": {
        "English": "Home",
        "Malayalam": "ഹോം"
    },
    "nav_assistant": {
        "English": "AI Assistant",
        "Malayalam": "എഐ സഹായി (AI Assistant)"
    },
    "nav_weather": {
        "English": "Weather",
        "Malayalam": "കാലാവസ്ഥ (Weather)"
    },
    "nav_soil": {
        "English": "Soil Health",
        "Malayalam": "മണ്ണ് പരിശോധന (Soil Health)"
    },
    "nav_crop_health": {
        "English": "Crop Health",
        "Malayalam": "വിള ആരോഗ്യം (Crop Health)"
    },
    "nav_community": {
        "English": "Connect with Farmers",
        "Malayalam": "കർഷക കൂട്ടായ്മ (Community)"
    },
    "nav_about": {
        "English": "About",
        "Malayalam": "വിവരണം (About)"
    },
    
    # Selected badges
    "selected_district": {
        "English": "Selected District",
        "Malayalam": "തിരഞ്ഞെടുത്ത ജില്ല"
    },
    "target_crop": {
        "English": "Target Crop",
        "Malayalam": "തിരഞ്ഞെടുത്ത വിള"
    },
    "active_language": {
        "English": "Active Language",
        "Malayalam": "സജീവ ഭാഷ"
    },
    
    # Home Module cards
    "card_ai_title": {
        "English": "🤖 AI Crop Assistant",
        "Malayalam": "🤖 എഐ കാർഷിക സഹായി"
    },
    "card_ai_desc": {
        "English": "Ask farming questions in English or Malayalam with KAU package of practices citations.",
        "Malayalam": "കാർഷിക സംശയങ്ങൾ ചോദിക്കൂ, KAU മാനദണ്ഡങ്ങൾ അനുസരിച്ചുള്ള മറുപടി നേടൂ."
    },
    "card_weather_title": {
        "English": "☀️ Live Weather",
        "Malayalam": "☀️ തത്സമയ കാലാവസ്ഥ"
    },
    "card_weather_desc": {
        "English": "Real-time district weather, precipitation, and farming advisories.",
        "Malayalam": "ജില്ലാ അടിസ്ഥാനത്തിലുള്ള തത്സമയ മഴ, താപനില മുന്നറിയിപ്പുകൾ."
    },
    "card_soil_title": {
        "English": "🧪 Crop-Specific Soil Health",
        "Malayalam": "🧪 വിളാധിഷ്ഠിത മണ്ണ് പരിശോധന"
    },
    "card_soil_desc": {
        "English": "Customized NPK and pH recommendations specifically tuned to your chosen crop.",
        "Malayalam": "നിങ്ങൾ തിരഞ്ഞെടുത്ത വിളയ്ക്കനുസരിച്ചുള്ള NPK, കുമ്മായം വളപ്രയോഗ ശുപാർശകൾ."
    },
    "card_crop_title": {
        "English": "🌿 AI Leaf Disease Scanner",
        "Malayalam": "🌿 എഐ ഇലരോഗ നിർണ്ണയം"
    },
    "card_crop_desc": {
        "English": "Upload leaf photos for instant 97.15% accurate AI disease diagnosis & OpenAI treatment tips.",
        "Malayalam": "ഇലയുടെ ചിത്രം നൽകി രോഗം കണ്ടെത്തൂ, ഒപ്പം വിദഗ്ധ പ്രതിവിധികളും അറിയൂ."
    },
    "card_comm_title": {
        "English": "👥 Connect with Farmers",
        "Malayalam": "👥 കർഷക കൂട്ടായ്മ"
    },
    "card_comm_desc": {
        "English": "Share insights, ask peer questions, and contact local Krishi Bhavans.",
        "Malayalam": "മറ്റ് കർഷകരുമായി ആശയങ്ങൾ പങ്കുവെക്കാം, കൃഷിഭവൻ നമ്പറുകൾ കണ്ടെത്താം."
    }
}

def t(key: str, lang: str = "English") -> str:
    """Return translation for key and language, falling back to English."""
    val = TRANSLATIONS.get(key, {})
    if isinstance(val, dict):
        return val.get(lang, val.get("English", key))
    return str(val)
