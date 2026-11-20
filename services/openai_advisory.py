import os
from pathlib import Path
from openai import OpenAI

def get_api_key():
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("LLM_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return os.getenv("LLM_API_KEY", "")

# Expert KAU & CIBRC treatment database for instant offline/quota fallback
KAU_TREATMENTS = {
    "early blight": {
        "English": {
            "symptoms": "Concentric dark brown rings ('bullseye' target spots) on older foliage, yellowing surrounding leaves, defoliation.",
            "organic": "Spray 1% Bordeaux mixture or *Pseudomonas fluorescens* (20g/L). Apply Neem oil (5ml/L) with soap emulsifier weekly.",
            "chemical": "Foliar spray of Mancozeb (Dithane M-45) @ 2-2.5g/L or Chlorothalonil @ 2g/L at early onset of disease.",
            "prevention": "Ensure wide spacing for air circulation, avoid overhead sprinkler irrigation, practice 3-year solanaceous crop rotation, and mulch around base."
        },
        "Malayalam": {
            "symptoms": "ഇലകളിൽ കേന്ദ്രീകൃതമായ തവിട്ടുനിറത്തിലുള്ള വളയങ്ങൾ (Bullseye പാടുകൾ), ഇലകൾ മഞ്ഞളിച്ച് കൊഴിയുന്നു.",
            "organic": "1% ബോർഡോ മിശ്രിതം അല്ലെങ്കിൽ സ്യൂഡോമോണസ് ഫ്ലൂറസെൻസ് (20 ഗ്രാം/ലിറ്റർ) ഇലകളിൽ തളിക്കുക. വേപ്പെണ്ണ വെളുത്തുള്ളി മിശ്രിതം ഉപയോഗിക്കുക.",
            "chemical": "മാങ്കോസെബ് (Dithane M-45) 2-2.5 ഗ്രാം/ലിറ്റർ വെള്ളത്തിൽ കലക്കി രോഗലക്ഷണം കണ്ട ഉടൻ തളിക്കുക.",
            "prevention": "ചെടികൾ തമ്മിൽ ആവശ്യത്തിന് അകലം പാലിക്കുക, തുള്ളിനന രീതി ഉപയോഗിക്കുക, രോഗബാധയുള്ള ഇലകൾ നശിപ്പിക്കുക."
        }
    },
    "late blight": {
        "English": {
            "symptoms": "Water-soaked lesions on leaf margins turning purplish-black, rapid blighting, white fungal mildew under humid conditions.",
            "organic": "Spray 1% Bordeaux mixture prophylactically before rainy periods. Apply *Trichoderma viride* or *Pseudomonas* to soil and foliage.",
            "chemical": "Spray Metalaxyl + Mancozeb (Ridomil MZ @ 2g/L) or Cymoxanil + Mancozeb @ 2g/L at first appearance.",
            "prevention": "Avoid waterlogging, destroy infected plant debris, ensure proper ridge planting for soil drainage."
        },
        "Malayalam": {
            "symptoms": "ഇലകളുടെ അരികുകളിൽ നനഞ്ഞ പാടുകൾ, പിന്നീട് കറുപ്പ് കലർന്ന തവിട്ടുനിറമായി മാറുന്നു. അടിഭാഗത്ത് വെളുത്ത പൂപ്പൽ വളരുന്നു.",
            "organic": "മഴക്കാലത്തിന് മുൻപായി 1% ബോർഡോ മിശ്രിതം മുൻകരുതലായി തളിക്കുക. ട്രൈക്കോഡെർമ അടങ്ങിയ ജൈവവളങ്ങൾ ചേർക്കുക.",
            "chemical": "റിഡോമിൽ (Metalaxyl + Mancozeb) 2 ഗ്രാം/ലിറ്റർ വെള്ളത്തിൽ തളിക്കുക.",
            "prevention": "തോട്ടത്തിൽ വെള്ളക്കെട്ട് ഒഴിവാക്കുക, വായുസഞ്ചാരം ഉറപ്പാക്കുക, രോഗബാധയേറ്റ ഭാഗങ്ങൾ പൂർണ്ണമായി തീയിട്ട് നശിപ്പിക്കുക."
        }
    },
    "bacterial spot": {
        "English": {
            "symptoms": "Small, water-soaked, dark brown angular spots with yellow halos on leaves, rough scabby lesions on fruits.",
            "organic": "Foliar spray of *Pseudomonas fluorescens* (20g/L). Dip roots/seedlings in Pseudomonas suspension for 30 minutes before planting.",
            "chemical": "Spray Copper Oxychloride (COC @ 2.5g/L) combined with Streptocycline (0.1g/L - 100 ppm).",
            "prevention": "Use certified disease-free seeds, practice hot water seed treatment (50°C for 25 mins), avoid working in wet fields."
        },
        "Malayalam": {
            "symptoms": "ഇലകളിൽ മഞ്ഞ വലയത്തോടുകൂടിയ ചെറിയ തവിട്ടുനിറത്തിലുള്ള പാടുകൾ, കായ്കളിൽ പരുപരുത്ത വ്രണങ്ങൾ.",
            "organic": "സ്യൂഡോമോണസ് ഫ്ലൂറസെൻസ് (20 ഗ്രാം/ലിറ്റർ) ഇലകളിൽ തളിക്കുകയും നടുന്നതിന് മുൻപ് തൈകളുടെ വേരുകൾ മുക്കിവെക്കുകയും ചെയ്യുക.",
            "chemical": "കോപ്പർ ഓക്സിക്ലോറൈഡ് (COC 2.5 ഗ്രാം) + സ്ട്രെപ്റ്റോസൈക്ലിൻ (1 ഗ്രാം / 10 ലിറ്റർ) കലക്കി തളിക്കുക.",
            "prevention": "രോഗമില്ലാത്ത വിത്തുകൾ ഉപയോഗിക്കുക, ചൂടുവെള്ളത്തിൽ വിത്ത് സംസ്കരിക്കുക, ഈർപ്പമുള്ള സമയത്ത് വിളവെടുപ്പ് ഒഴിവാക്കുക."
        }
    },
    "rust": {
        "English": {
            "symptoms": "Reddish-orange or golden powdery pustules primarily on lower leaf surfaces, leaf chlorosis and drying.",
            "organic": "Dust with fine sulfur powder or apply wettable sulfur (2g/L). Neem kernel extract (5%) spray.",
            "chemical": "Spray Propiconazole (Tilt 25 EC @ 1ml/L) or Hexaconazole @ 1ml/L at initiation of pustules.",
            "prevention": "Plant resistant cultivars, balance nitrogen fertilizer (avoid excessive urea), remove alternate host weeds."
        },
        "Malayalam": {
            "symptoms": "ഇലകളുടെ അടിഭാഗത്ത് തുരുമ്പ് പോലുള്ള ചുവപ്പ് കലർന്ന ഓറഞ്ച് പൊടികൾ, ഇലകൾ ഉണങ്ങിപ്പോകുന്നു.",
            "organic": "വെറ്റബിൾ സൾഫർ (2 ഗ്രാം/ലിറ്റർ) തളിക്കുക. 5% വേപ്പിൻകുരു സത്ത് ഉപയോഗിക്കുക.",
            "chemical": "പ്രൊപികൊണാസോൾ (Tilt 1 മില്ലി/ലിറ്റർ) അല്ലെങ്കിൽ ഹെക്സാകൊണാസോൾ തളിക്കുക.",
            "prevention": "നൈട്രജൻ വളങ്ങൾ അധികമാകാതെ ശ്രദ്ധിക്കുക, തുരുമ്പ് രോഗത്തെ പ്രതിരോധിക്കുന്ന ഇനങ്ങൾ കൃഷി ചെയ്യുക."
        }
    },
    "leaf spot": {
        "English": {
            "symptoms": "Circular or irregular brown necrotic spots on leaves with distinct borders, premature leaf drop.",
            "organic": "Foliar spray of 1% Bordeaux mixture or fermented buttermilk-garlic mixture (1:10 dilution).",
            "chemical": "Spray Carbendazim @ 1g/L or Mancozeb @ 2g/L at 14-day intervals.",
            "prevention": "Clean pruning, destroy diseased leaves, promote healthy root aeration."
        },
        "Malayalam": {
            "symptoms": "ഇലകളിൽ വൃത്താകൃതിയിലോ ക്രമരഹിതമായോ ഉള്ള തവിട്ട് പാടുകൾ, ഇലകൾ അകാലത്തിൽ കൊഴിയുന്നു.",
            "organic": "1% ബോർഡോ മിശ്രിതം തളിക്കുക. കാന്താരി-മോര് മിശ്രിതം അല്ലെങ്കിൽ വെളുത്തുള്ളി മിശ്രിതം ഉപയോഗിക്കുക.",
            "chemical": "കാർബെൻഡാസിം (1 ഗ്രാം/ലിറ്റർ) അല്ലെങ്കിൽ മാങ്കോസെബ് (2 ഗ്രാം/ലിറ്റർ) തളിക്കുക.",
            "prevention": "രോഗബാധയുള്ള ഇലകൾ യഥാസമയം നീക്കം ചെയ്യുക, വായുസഞ്ചാരവും വേരുകളിലേക്ക് വായുവും ഉറപ്പാക്കുക."
        }
    },
    "healthy": {
        "English": {
            "symptoms": "Vibrant green foliage, no necrotic lesions, optimal vigor and healthy leaf turgor.",
            "organic": "Apply Panchagavya (3% spray) or Fish Amino Acid (5ml/L) every 15-20 days to promote vegetative growth and immunity.",
            "chemical": "Maintain recommended balanced NPK dosage for the crop. Avoid unnecessary chemical sprays.",
            "prevention": "Continue regular monitoring, maintain soil organic mulch, adhere to scheduled irrigation."
        },
        "Malayalam": {
            "symptoms": "ആരോഗ്യമുള്ള പച്ചനിറത്തിലുള്ള ഇലകൾ, രോഗലക്ഷണങ്ങളോ കേടുകളോ ഇല്ല.",
            "organic": "ചെടിയുടെ പ്രതിരോധശേഷി വർദ്ധിപ്പിക്കാൻ 3% പഞ്ചഗവ്യം അല്ലെങ്കിൽ ഫിഷ് അമിനോ ആസിഡ് (5 മില്ലി/ലിറ്റർ) തളിക്കുക.",
            "chemical": "വിളയ്ക്കനുസരിച്ചുള്ള സന്തുലിത രാസവളപ്രയോഗം മാത്രം നൽകുക. അനാവശ്യ കീടനാശിനികൾ ഒഴിവാക്കുക.",
            "prevention": "കൃത്യമായ നനയും മണ്ണ് പുതയിടലും തുടരുക, തോട്ടം എപ്പോഴും വൃത്തിയായി സൂക്ഷിക്കുക."
        }
    }
}

def get_fallback_advisory(crop_name: str, disease_name: str, confidence: float, language: str = "English") -> str:
    """Return comprehensive KAU-aligned package of practices treatment when API is offline or quota-exceeded."""
    d_lower = disease_name.lower()
    
    # Match best category
    matched_key = "leaf spot"
    if "healthy" in d_lower:
        matched_key = "healthy"
    elif "early blight" in d_lower:
        matched_key = "early blight"
    elif "late blight" in d_lower:
        matched_key = "late blight"
    elif "bacterial" in d_lower or "spot" in d_lower:
        matched_key = "bacterial spot"
    elif "rust" in d_lower:
        matched_key = "rust"
    
    entry = KAU_TREATMENTS[matched_key].get(language, KAU_TREATMENTS[matched_key]["English"])
    
    if language == "Malayalam":
        return f"""### 🌾 KAU കാർഷിക സർവകലാശാല രോഗനിവാരണ മാർഗ്ഗരേഖ

**രോഗ നിർണ്ണയം:** {crop_name} - {disease_name} (വിശ്വാസ്യത: {confidence*100:.1f}%)

---
#### 1. 🔍 രോഗലക്ഷണങ്ങൾ (Symptoms)
{entry['symptoms']}

#### 2. 🌿 ജൈവ പ്രതിവിധികൾ (Organic & Biological Control)
{entry['organic']}

#### 3. 🧪 ശാസ്ത്രീയ രാസനിയന്ത്രണം (Chemical Management - KAU PoP)
{entry['chemical']}

#### 4. 🛡️ പ്രതിരോധ കാർഷിക രീതികൾ (Cultural & Preventive Practices)
{entry['prevention']}

*(കുറിപ്പ്: കേരള കാർഷിക സർവകലാശാല 2016 പാക്കേജ് ഓഫ് പ്രാക്ടീസസ് അടിസ്ഥാനമാക്കിയുള്ളതാണ്).*
"""
    else:
        return f"""### 🌾 Kerala Agricultural University (KAU) Advisory & Treatment Guide

**Diagnosis:** {crop_name} - {disease_name} (Confidence: {confidence*100:.1f}%)

---
#### 1. 🔍 Disease Verification & Symptoms
{entry['symptoms']}

#### 2. 🌿 Biological & Organic Management
{entry['organic']}

#### 3. 🧪 Approved Chemical Control (KAU Package of Practices)
{entry['chemical']}

#### 4. 🛡️ Cultural & Preventive Field Measures
{entry['prevention']}

*(Advisory aligned with Kerala Agricultural University (KAU) Package of Practices).*
"""

def generate_disease_advisory(crop_name: str, disease_name: str, confidence: float, language: str = "English") -> str:
    """Generate agronomic treatment and management recommendations via OpenAI API with KAU fallback."""
    api_key = get_api_key()
    if not api_key:
        return get_fallback_advisory(crop_name, disease_name, confidence, language)

    client = OpenAI(api_key=api_key)
    is_malayalam = (language == "മലയാളം")
    
    if "healthy" in disease_name.lower():
        prompt = (
            f"The plant '{crop_name}' is diagnosed as HEALTHY with {confidence*100:.1f}% confidence. "
            f"Provide best agronomic practices under Kerala Agricultural University (KAU) guidelines: organic growth promoters, "
            f"seasonal preventive care against common pests in Kerala, and soil nutrition maintenance. "
            f"Write the response in {'Malayalam (മലയാളത്തിൽ)' if is_malayalam else 'clear structured English markdown'}."
        )
    else:
        prompt = (
            f"A plant leaf image for '{crop_name}' has been diagnosed with '{disease_name}' with {confidence*100:.1f}% confidence. "
            f"As a Senior Plant Pathologist at Kerala Agricultural University (KAU), provide a comprehensive advisory:\n"
            f"1. **Symptoms & Field Identification**\n"
            f"2. **Immediate Organic & Biological Remedies** (e.g. Pseudomonas fluorescens, Neem oil, Bordeaux mixture, Trichoderma with exact dosages)\n"
            f"3. **Chemical Fungicide Treatment** (Approved KAU dosages per liter of water)\n"
            f"4. **Field Prevention & Cultural Hygiene**\n"
            f"Write the response in {'Malayalam (മലയാളത്തിൽ)' if is_malayalam else 'English markdown'}."
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Kerala Agricultural University (KAU) agronomist and plant pathologist. "
                        "Give highly actionable, scientifically accurate, and farmer-friendly advice for crops in Kerala."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=850
        )
        return response.choices[0].message.content
    except Exception as e:
        # If API hits 429 quota or connection error, seamlessly deliver verified KAU advisory with notice
        fallback = get_fallback_advisory(crop_name, disease_name, confidence, language)
        err_msg = str(e)
        if "429" in err_msg or "credit" in err_msg.lower():
            notice = "> ℹ️ *Note: OpenAI API reported quota limit/no credits remaining on your key. Loaded verified KAU Package of Practices agronomic guidance below:*\n\n"
        else:
            notice = f"> ℹ️ *Notice: OpenAI connection ({err_msg[:80]}...). Using verified KAU guidelines below:*\n\n"
        return notice + fallback
