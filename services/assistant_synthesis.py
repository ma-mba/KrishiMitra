from services.openai_advisory import get_api_key
from openai import OpenAI

def build_dynamic_synthesis(query: str, kau_results: list, web_results: list, crop: str, language: str = "English") -> str:
    """Build a comprehensive, question-specific agronomic answer when OpenAI API is offline or quota-limited."""
    q_lower = query.lower()
    is_mal = (language == "മലയാളം")
    crop_name = crop.capitalize()
    
    # 1. FERTILIZATION INTENT
    if any(w in q_lower for w in ["fertiliz", "fertilise", "npk", "manure", "വളം", "വളപ്രയോഗം", "nutrition", "feed"]):
        if crop == "apple":
            if is_mal:
                return f"""### 🍎 ആപ്പിൾ കൃഷിയിലെ ശാസ്ത്രീയ വളപ്രയോഗ മാർഗ്ഗരേഖ (Apple Fertilization Guide)

**ചോദ്യം:** *"{query}"*  
**തിരഞ്ഞെടുത്ത വിള:** **ആപ്പിൾ (Apple)** *(കേരളത്തിൽ ഇടുക്കിയിലെ കാന്തല്ലൂർ, വട്ടവട മേഖലകളിൽ പ്രധാനമായും കൃഷിചെയ്യുന്നു)*

---
#### 1. 🌿 അടിവളവും ജൈവവള പ്രയോഗവും (Organic Manuring)
- **വിശ്രമാവസ്ഥയിൽ (ഡിസംബർ - ജനുവരി):** തൈയൊന്നിന് 20-30 കി.ഗ്രാം ഉണങ്ങിപ്പൊടിഞ്ഞ കാലിവളം അല്ലെങ്കിൽ കമ്പോസ്റ്റ് തടത്തിൽ ഇളക്കി ചേർക്കുക.
- **വേപ്പിൻപിണ്ണാക്ക്:** മണ്ണിലെ നിമാവിരകളെ തടയാൻ 1-2 കി.ഗ്രാം വേപ്പിൻപിണ്ണാക്ക് ചേർക്കുക.

#### 2. 🧪 രാസവള ശുപാർശ (NPK Dosage per Mature Tree)
- **ഒരു കായ്ഫലമുള്ള മരത്തിന് പ്രതിവർഷം:**
  - **നൈട്രജൻ (N):** 500 - 700 ഗ്രാം (യൂറിയ ~ 1.2 കി.ഗ്രാം)
  - **ഫോസ്ഫറസ് (P):** 250 - 350 ഗ്രാം (റോക്ക് ഫോസ്ഫേറ്റ്/DAP ~ 1.5 കി.ഗ്രാം)
  - **പൊട്ടാസ്യം (K):** 700 - 1000 ഗ്രാം (MOP ~ 1.5 കി.ഗ്രാം)
- **നൽകേണ്ട രീതി:** ഫോസ്ഫറസും പകുതി പൊട്ടാഷും മുഴുവൻ ജൈവവളങ്ങളും മഞ്ഞുകാലത്ത് (ഡിസംബറിൽ) നൽകുക. പകുതി നൈട്രജൻ തളിരിടുന്നതിന് (ഫെബ്രുവരി-മാർച്ച്) മുൻപും, ബാക്കി നൈട്രജനും പൊട്ടാഷും കായ്പിടുത്തത്തിന് ശേഷം (മേയ് മാസത്തിൽ) നൽകുക.

#### 3. 🔬 സൂക്ഷ്മ മൂലകങ്ങൾ (Micronutrients & Foliar Spray)
- പൂവിടുന്നതിന് മുൻപും (Pink bud stage) കായ്പിടുത്തത്തിന് ശേഷവും **ബോറോൺ (0.1% Borax)**, **സിങ്ക് (0.2% Zinc Sulphate)** എന്നിവ ഇലകളിൽ തളിക്കുന്നത് കായ് കൊഴിച്ചിൽ തടയും.
- കാൽസ്യം കുറവ് പരിഹരിക്കാൻ 0.5% കാൽസ്യം ക്ലോറൈഡ് തളിക്കുക.

#### 4. 🛡️ പ്രധാന നിർദ്ദേശങ്ങൾ
- മണ്ണിന്റെ അനുയോജ്യ pH: **6.0 - 6.8**.
- വളം തടിയുടെ ചുവട്ടിൽ നേരിട്ട് ഇടാതെ, മരത്തിന്റെ ശിഖര വ്യാപ്തിയിലുള്ള (Drip line) തടങ്ങളിൽ വിതറി മണ്ണിട്ട് മൂടുക.
"""
            else:
                return f"""### 🍎 Complete Apple Tree Nutrition & Fertilization Guide

**Query:** *"{query}"*  
**Identified Crop:** **Apple (*Malus domestica*)** *(Cultivated in Kerala's cool high ranges: Kanthalloor & Vattavada, Idukki)*

---
#### 1. 🌿 Basal & Organic Manuring (Dormant Season - Dec to Jan)
- **Well-Rotted FYM / Compost:** Apply **20 - 30 kg per mature bearing tree** during the winter dormant stage before bud break.
- **Neem Cake:** 1 - 2 kg per tree basin to control root grubs and improve soil microbial flora.

#### 2. 🧪 NPK Fertilizer Schedule (Per Mature Tree/Year)
- **Recommended Pure Nutrients:**
  - **Nitrogen (N):** 500 – 700 g (Urea: ~1.2 kg)
  - **Phosphorus (P₂O₅):** 250 – 350 g (SSP / Rock Phosphate: ~1.5 kg)
  - **Potassium (K₂O):** 700 – 1000 g (MOP: ~1.5 kg)
- **Split Timing:**
  - **First Split (Winter Dormancy, Dec-Jan):** Full Organic Manure + Full Phosphorus + 50% Potassium.
  - **Second Split (Bud Burst / Pre-Bloom, Feb-Mar):** 50% Nitrogen.
  - **Third Split (Fruit Set / Pea Stage, May):** Remaining 50% Nitrogen + 50% Potassium to boost fruit sizing and sweetness.

#### 3. 🔬 Essential Foliar Micronutrients
- **Boron:** Spray **Solubor or Borax @ 0.1% (1g/L)** at the pink bud stage to enhance pollen germination and uniform fruit set.
- **Zinc:** Spray Zinc Sulphate (0.2%) in early spring to prevent 'little leaf' rosette symptoms.
- **Calcium:** Apply Calcium Chloride (0.5%) spray during fruit sizing to avoid 'Bitter Pit' disorder.

#### 4. 🛡️ Agronomic Best Practices
- **Optimal Soil pH:** **6.0 to 6.8**. Apply lime or dolomite in winter if soil is acidic.
- **Application Technique:** Apply fertilizers in a circular trench under the tree drip canopy (perimeter), not against the trunk bark. Water thoroughly post-application.
"""
        else:
            # Generic/KAU fertilization
            if is_mal:
                return f"""### 🌾 {crop_name} വിളയ്ക്കുള്ള സമഗ്ര വളപ്രയോഗ ശുപാർശ (KAU PoP)

**ചോദ്യം:** *"{query}"*  
**വിള:** **{crop_name}**

---
#### 1. 🌿 ജൈവവള പ്രയോഗം
- നടീലിന് മുൻപായി ഏക്കറിന് 2-3 ടൺ ഉണങ്ങിപ്പൊടിഞ്ഞ കാലിവളമോ കമ്പോസ്റ്റോ അടിത്തട്ടിൽ ചേർക്കുക.
- പച്ചിലവളങ്ങൾ അല്ലെങ്കിൽ വേപ്പിൻപിണ്ണാക്ക് മണ്ണുമായി യോജിപ്പിക്കുക.

#### 2. 🧪 രാസവള ക്രമം (NPK Split Schedule)
- അടിവളമായി മുഴുവൻ ഫോസ്ഫറസും (രാജ്ഫോസ്), പകുതി പൊട്ടാഷും (MOP), മൂന്നിലൊന്ന് നൈട്രജനും (യൂറിയ) നൽകുക.
- ബാക്കി നൈട്രജനും പൊട്ടാഷും വളർച്ചാ ഘട്ടങ്ങളിൽ തുല്യ ഗഡുക്കളായി മേൽവളമായി നൽകുക.

#### 3. ⚪ കുമ്മായ പ്രയോഗം
- കേരളത്തിലെ മണ്ണിലെ അമ്ലത ക്രമീകരിക്കാൻ pH പരിശോധന നടത്തി ആവശ്യമായ കുമ്മായം (Dolomite) അടിവളത്തിന് രണ്ടാഴ്ച മുൻപ് ചേർക്കുക.
"""
            else:
                return f"""### 🌾 Scientific Fertilizer Management for {crop_name} (KAU PoP)

**Query:** *"{query}"*  
**Target Crop:** **{crop_name}**

---
#### 1. 🌿 Basal Organic Nutrition
- Incorporate **5 tonnes/ha of well-rotted FYM or vermicompost** during preliminary land preparation.
- Apply neem cake (250 kg/ha) to enhance nitrogen uptake efficiency and suppress soil pests.

#### 2. 🧪 Balanced NPK Split Applications
- **Basal:** Apply 100% of Phosphorus (Rock Phosphate), 50% of Potassium (MOP), and 33% of Nitrogen (Urea).
- **Top-Dressing:** Split remaining Nitrogen and Potassium during vegetative growth and fruit/grain development.

#### 3. ⚪ Soil Neutralization & Liming
- Maintain soil pH around 5.5 - 6.5. Broadcast Agricultural Lime or Dolomite 14 days before planting to ensure nutrient bioavailability.
"""

    # 2. PEST & DISEASE / YELLOW LEAF INTENT
    elif any(w in q_lower for w in ["yellow", "disease", "rot", "blight", "spot", "pest", "bug", "worm", "രോഗം", "മഞ്ഞ", "കീട"]):
        if is_mal:
            return f"""### 🌾 {crop_name} കീട-രോഗ പ്രതിരോധ കർമ്മപദ്ധതി (Diagnosis & Treatment)

**ചോദ്യം:** *"{query}"*  
**പരിശോധിച്ച വിള:** **{crop_name}**

---
#### 1. 🔍 പ്രധാന കാരണം (Probable Cause)
ലക്ഷണങ്ങൾ പ്രധാനമായും **പോഷകക്കുറവ് (പൊട്ടാസ്യം/മഗ്നീഷ്യം)**, **കുമിൾബാധ (Leaf Spot / Blight)**, അല്ലെങ്കിൽ വേരുകളിൽ വെള്ളക്കെട്ട് നിന്നുള്ള **വേരുചീയൽ** എന്നിവ മൂലമാകാം.

#### 2. ⚡ അടിയന്തര നടപടികൾ (Next 24-48 Hours)
- രോഗബാധയേറ്റ ഇലകൾ മുറിച്ചുമാറ്റി തോട്ടത്തിന് പുറത്തു കളയുക.
- തടത്തിൽ വെള്ളക്കെട്ടുണ്ടെങ്കിൽ അടിയന്തരമായി നീർവാർച്ചാ ചാലുകൾ കീറുക.

#### 3. 🌿 ജൈവ പ്രതിവിധികൾ (Organic Controls)
- **സ്യൂഡോമോണസ് ഫ്ലൂറസെൻസ് (Pseudomonas fluorescens):** 20 ഗ്രാം/ലിറ്റർ വെള്ളത്തിൽ കലക്കി തളിക്കുക.
- **1% ബോർഡോ മിശ്രിതം:** കുമിൾരോഗം തടയാൻ പ്രയോഗിക്കുക.

#### 4. 🧪 രാസനിയന്ത്രണം (Chemical Fungicide)
- കുമിൾബാധ രൂക്ഷമാണെങ്കിൽ: **മാങ്കോസെബ്** 2 ഗ്രാം/ലിറ്റർ അല്ലെങ്കിൽ **കാർബെൻഡാസിം** 1 ഗ്രാം/ലിറ്റർ തളിക്കുക.
"""
        else:
            return f"""### 🌾 {crop_name} Health Diagnosis & Farmer Action Plan

**Query:** *"{query}"*  
**Crop Analyzed:** **{crop_name}**

---
#### 1. 🔍 Diagnosis & Primary Cause
Symptoms suggest either **nutrient chlorosis (Potassium / Magnesium deficiency)**, **fungal foliar infection (Leaf Spot / Blight)**, or **root asphyxiation due to poor drainage**.

#### 2. ⚡ Immediate Action (24-48 Hours)
- Prune heavily damaged leaves and safely dispose of them outside the plot.
- Inspect drainage ditches; clear any water stagnation around the root collar.

#### 3. 🌿 Biological & Organic Solutions
- **Foliar Bio-spray:** Apply *Pseudomonas fluorescens* (20g/L) across all leaf surfaces.
- **Protective Spray:** Apply 1% freshly prepared Bordeaux mixture.

#### 4. 🧪 Targeted Chemical Intervention
- For spreading fungal lesions: Spray **Mancozeb (Dithane M-45 @ 2g/L)** or **Propiconazole (1ml/L)** with a wetting agent.
"""

    # 3. GENERAL AGRONOMIC QUERY
    else:
        # Fallback to combined web + KAU points
        web_points = [f"- {w.get('title')}: {w.get('snippet')[:180]}…" for w in web_results[:3]]
        web_text = "\n".join(web_points) if web_points else "Consult local agricultural extension for specialized advice."
        
        if is_mal:
            return f"""### 🌾 {crop_name} കാർഷിക മാർഗ്ഗനിർദ്ദേശം (Agronomic Advisory)

**ചോദ്യം:** *"{query}"*  
**വിള:** **{crop_name}**

---
#### 🔍 കണ്ടെത്തലുകളും നിർദ്ദേശങ്ങളും:
{web_text}

#### 📋 കർഷകർക്കുള്ള പൊതുവായ ശുപാർശകൾ:
- മണ്ണുപരിശോധന നടത്തി സമീകൃത വളപ്രയോഗം നടത്തുക.
- ശാസ്ത്രീയമായ നീർവാർച്ചയും രോഗനിയന്ത്രണവും ഉറപ്പുവരുത്തുക.
- കൂടുതൽ വിവരങ്ങൾക്ക് അടുത്തുള്ള കൃഷിഭവനുമായോ KAU വിദഗ്ധരുമായോ ബന്ധപ്പെടുക.
"""
        else:
            return f"""### 🌾 Agronomic Advisory for {crop_name}

**Query:** *"{query}"*  
**Crop Identified:** **{crop_name}**

---
#### 🔍 Key Findings & Guidelines:
{web_text}

#### 📋 Actionable Farmer Recommendations:
- Follow recommended spacing, seasonal planting windows, and balanced NPK nutrition.
- Practice integrated pest management (IPM) combining biological control with judicious chemical usage.
- Contact your local Krishi Bhavan or KAU Extension Centre for field-specific guidance.
"""

def generate_combined_answer(query: str, kau_results: list, web_results: list, crop: str, language: str = "English") -> str:
    """Generate combined answer using OpenAI if credits available, or specialized dynamic synthesis."""
    api_key = get_api_key()
    
    kau_context = "\n\n".join([f"[KAU Official PoP Page {c.get('pdf_page')} - {c.get('chunk_id')}]: {c.get('text')}" for c in kau_results[:3]])
    web_context = "\n\n".join([f"[Web Source: {w.get('title')}]: {w.get('snippet')} (URL: {w.get('url')})" for w in web_results[:3]])
    
    is_mal = (language == "മലയാളം")
    
    if api_key:
        client = OpenAI(api_key=api_key)
        prompt = (
            f"You are a Senior Agronomist at Kerala Agricultural University (KAU).\n"
            f"Farmer Question: '{query}'\n"
            f"Crop: '{crop}'\n\n"
            f"KAU PACKAGE OF PRACTICES CONTEXT:\n{kau_context}\n\n"
            f"LIVE AGRONOMIC WEB FINDINGS:\n{web_context}\n\n"
            f"Answer the farmer's question directly and thoroughly for the crop '{crop}'.\n"
            f"If the question is about fertilizing, provide complete NPK and organic schedules.\n"
            f"If the question is about disease/yellowing, provide cause, immediate action, organic remedies, and chemical control.\n"
            f"Write in {'clear Malayalam (മലയാളത്തിൽ)' if is_mal else 'clear English markdown'}."
        )
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful Kerala Krishi Bhavan agronomist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=900
            )
            return resp.choices[0].message.content
        except Exception:
            pass

    return build_dynamic_synthesis(query, kau_results, web_results, crop, language)
