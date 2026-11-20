import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pages.profile import get_current_user_profile

st.set_page_config(
    page_title="KrishiMitr | AI for Kerala Farmers",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Vibrant Gradient Green Theme
st.markdown("""
<style>
/* Hide Streamlit default auto-generated multi-page navigation at top of sidebar */
[data-testid="stSidebarNav"] {display: none !important;}
section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] {display: none !important;}

/* Full Website Vibrant Gradient Green Background */
.stApp {
    background: linear-gradient(145deg, #062317 0%, #0d3f2c 25%, #155b40 50%, #0f4430 75%, #072619 100%) !important;
    background-attachment: fixed !important;
    color: #f1f5f9 !important;
}

/* Sidebar Gradient Green */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #051c13 0%, #0b3424 50%, #051a11 100%) !important;
    border-right: 1px solid rgba(52, 211, 153, 0.25) !important;
}

/* Hero Section Banner with Radiant Kerala Green Gradient */
.km-hero-container {
    background: linear-gradient(135deg, #093323 0%, #13573e 35%, #1d7955 70%, #2ea776 100%);
    border-radius: 20px;
    padding: 38px 44px;
    margin-bottom: 24px;
    border: 1px solid rgba(110, 231, 183, 0.45);
    box-shadow: 0 16px 42px rgba(4, 30, 20, 0.6);
    position: relative;
    overflow: hidden;
}

.km-hero-title {
    color: #ffffff;
    font-size: 2.7rem;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 12px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.km-hero-subtitle {
    color: #d1fae5;
    font-size: 1.15rem;
    max-width: 720px;
    line-height: 1.55;
    margin-bottom: 24px;
    font-weight: 400;
}

/* Status Chips on Hero */
.km-chip {
    display: inline-flex;
    align-items: center;
    background: rgba(16, 185, 129, 0.25);
    border: 1px solid rgba(110, 231, 183, 0.6);
    border-radius: 24px;
    padding: 7px 16px;
    color: #ffffff;
    font-size: 0.88rem;
    font-weight: 600;
    margin-right: 10px;
    margin-bottom: 8px;
    backdrop-filter: blur(6px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.km-chip-active {
    background: rgba(52, 211, 153, 0.35);
    border-color: #34d399;
}

/* Streamlit Native Bordered Containers styled with Emerald Glass Gradient */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, rgba(16, 62, 46, 0.75) 0%, rgba(9, 38, 28, 0.85) 100%) !important;
    border: 1px solid rgba(52, 211, 153, 0.3) !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(10px) !important;
}

/* Custom Gradient Buttons */
.stButton > button, .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(110, 231, 183, 0.4) !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 9px 22px !important;
    box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.5) !important;
    border-color: #6ee7b7 !important;
}

/* Input Fields and Selectboxes */
.stTextInput > div > div > input, .stSelectbox > div > div {
    background: rgba(6, 28, 20, 0.75) !important;
    border: 1px solid rgba(52, 211, 153, 0.35) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

/* Metric Widgets Styling */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(16, 62, 46, 0.5) 0%, rgba(9, 38, 28, 0.6) 100%) !important;
    border: 1px solid rgba(52, 211, 153, 0.25) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
}

div[data-testid="stMetricValue"] {
    color: #34d399 !important;
    font-weight: 800 !important;
}

/* Streamlit Tabs with Emerald Accents */
button[data-baseweb="tab"] {
    color: #a7f3d0 !important;
    font-weight: 600 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #34d399 !important;
    border-bottom: 3px solid #34d399 !important;
}
</style>
""", unsafe_allow_html=True)

from services.auth import render_login_portal, load_users

# Auth Session Management
from services.auth import render_login_portal

# Secure session initialization
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

# Language Selection
if "language" not in st.session_state:
    st.session_state["language"] = "English"

lang = st.sidebar.radio(
    "🌐 Language / ഭാഷ",
    ["English", "മലയാളം"],
    horizontal=True,
    key="language"
)

is_mal = (lang == "മലയാളം")

# If not logged in, show the full login/signup portal
if not st.session_state.get("authenticated", False):
    render_login_portal()
    st.stop()

# Load Logged In Farmer Profile
user_profile = st.session_state.get("user") or get_current_user_profile()

# Sidebar Branding & Personal Farmer Mini-Card
st.sidebar.markdown(f"""
<div style='background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(52, 211, 153, 0.35); border-radius: 14px; padding: 14px; margin: 8px 0 12px 0;'>
    <div style='display: flex; align-items: center; justify-content: space-between;'>
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='font-size: 2.2rem;'>👨‍🌾</div>
            <div>
                <div style='font-size: 1.1rem; font-weight: 800; color: #ffffff;'>{user_profile.get('name', 'Kerala Farmer')}</div>
                <div style='font-size: 0.8rem; color: #6ee7b7;'>📍 {user_profile.get('district')} • {user_profile.get('acres')} Acres</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 " + ("ലോഗ് ഔട്ട് (Sign Out)" if is_mal else "Sign Out / Switch User"), key="sign_out_btn", use_container_width=True):
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.rerun()

st.sidebar.markdown("---")

# District Selection
DISTRICTS = [
    "Palakkad", "Thrissur", "Ernakulam", "Kozhikode", "Wayanad",
    "Alappuzha", "Kottayam", "Idukki", "Malappuram", "Kannur",
    "Kasaragod", "Kollam", "Pathanamthitta", "Thiruvananthapuram"
]

DISTRICTS_MAL = {
    "Palakkad": "പാലക്കാട് (Palakkad)",
    "Thrissur": "തൃശ്ശൂർ (Thrissur)",
    "Ernakulam": "എറണാകുളം (Ernakulam)",
    "Kozhikode": "കോഴിക്കോട് (Kozhikode)",
    "Wayanad": "വയനാട് (Wayanad)",
    "Alappuzha": "ആലപ്പുഴ (Alappuzha)",
    "Kottayam": "കോട്ടയം (Kottayam)",
    "Idukki": "ഇടുക്കി (Idukki)",
    "Malappuram": "മലപ്പുറം (Malappuram)",
    "Kannur": "കണ്ണൂർ (Kannur)",
    "Kasaragod": "കാസർഗോഡ് (Kasaragod)",
    "Kollam": "കൊല്ലം (Kollam)",
    "Pathanamthitta": "പത്തനംതിട്ട (Pathanamthitta)",
    "Thiruvananthapuram": "തിരുവനന്തപുരം (Thiruvananthapuram)"
}

district = st.sidebar.selectbox(
    "📍 ജില്ല / District" if is_mal else "📍 District",
    DISTRICTS,
    format_func=lambda d: DISTRICTS_MAL.get(d, d) if is_mal else d,
    index=DISTRICTS.index(user_profile.get('district', 'Palakkad')) if user_profile.get('district') in DISTRICTS else 0,
    key="district"
)

# Crop Selection
CROPS = ["Paddy", "Banana", "Coconut", "Pepper", "Rubber", "Cardamom"]
CROPS_MAL = {
    "Paddy": "നെല്ല് (Paddy)",
    "Banana": "വാഴ (Banana)",
    "Coconut": "തെങ്ങ് (Coconut)",
    "Pepper": "കുരുമുളക് (Pepper)",
    "Rubber": "റബ്ബർ (Rubber)",
    "Cardamom": "ഏലം (Cardamom)"
}

crop = st.sidebar.selectbox(
    "🌾 പ്രധാന വിള / Primary Crop" if is_mal else "🌾 Primary Crop",
    CROPS,
    format_func=lambda c: CROPS_MAL.get(c, c) if is_mal else c,
    index=CROPS.index(user_profile.get('primary_crop', 'Paddy')) if user_profile.get('primary_crop') in CROPS else 0,
    key="crop"
)

st.sidebar.markdown("---")

NAV_OPTIONS_EN = [
    "Home",
    "Farmer Profile",
    "AI Assistant (Hybrid KAU + Web)",
    "Crop Health (Disease Scanner)",
    "Soil Health",
    "Crop Recommendation",
    "Weather (Live Location)",
    "Farmer Connect & Chat",
    "About"
]

NAV_OPTIONS_MAL = [
    "ഹോം (Home)",
    "കർഷക പ്രൊഫൈൽ (Profile)",
    "എഐ സഹായി (AI Assistant)",
    "വിള ആരോഗ്യം (Disease Scanner)",
    "മണ്ണ് പരിശോധന (Soil Health)",
    "വിള ശുപാർശ (Crop Recommendation)",
    "കാലാവസ്ഥ (Weather)",
    "കർഷക കൂട്ടായ്മ & ചാറ്റ് (Connect & Chat)",
    "വിവരണം (About)"
]

page_selection = st.sidebar.radio(
    "🧭 വിഭാഗങ്ങൾ / Navigation" if is_mal else "🧭 Navigation",
    NAV_OPTIONS_MAL if is_mal else NAV_OPTIONS_EN,
    index=0
)

page_idx = (NAV_OPTIONS_MAL if is_mal else NAV_OPTIONS_EN).index(page_selection)
canonical_page = NAV_OPTIONS_EN[page_idx]

# Routing
if canonical_page == "Home":
    hero_title = "AI-Powered Smart Agriculture for Kerala" if not is_mal else "കേരളത്തിനായുള്ള എഐ സ്മാർട്ട് കൃഷി സഹായി"
    hero_sub = (
        "Monitor crop health with deep learning vision, track soil condition, assess pest risks "
        "and get expert recommendations tailored for Kerala's climate and crops." if not is_mal else
        "ഡീപ് ലേണിംഗ് മോഡലിലൂടെ ഇലരോഗങ്ങൾ കണ്ടെത്തൂ, മണ്ണ് പരിശോധനാ ഫലങ്ങൾ വിലയിരുത്തൂ, "
        "കേരളത്തിന്റെ കാലാവസ്ഥയ്ക്കനുയോജ്യമായ KAU വിദഗ്ധ ഉപദേശങ്ങൾ നേടൂ."
    )
    
    st.markdown(f"""
    <div class='km-hero-container'>
        <div class='km-hero-title'>{hero_title}</div>
        <div class='km-hero-subtitle'>{hero_sub}</div>
        <div style='margin-bottom: 8px;'>
            <span class='km-chip km-chip-active'>🌿 Crop Health: 97.15% Accurate</span>
            <span class='km-chip'>🧪 Soil Monitoring: KAU PoP</span>
            <span class='km-chip'>🐛 Pest Risk: Early Warning</span>
            <span class='km-chip'>🌦️ Weather: Live GPS Telemetry</span>
            <span class='km-chip'>💬 Farmer Chat: Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3 Main Dashboard Cards
    st.markdown("### 🌾 " + ("തത്സമയ കൃഷി ഡാഷ്‌ബോർഡ്" if is_mal else "Live Agricultural Dashboard"))
    
    dash_col1, dash_col2, dash_col3 = st.columns(3)
    
    with dash_col1:
        with st.container(border=True):
            st.markdown("#### 🌦️ " + ("തത്സമയ കാലാവസ്ഥ (Kerala)" if is_mal else "Live Weather – Kerala"))
            st.caption(f"📍 Location: **{district} District**")
            
            from pages.weather import fetch_weather, KERALA_DISTRICTS
            coords = KERALA_DISTRICTS.get(district, (10.7867, 76.6548))
            w = fetch_weather(coords[0], coords[1])
            if w and "current" in w:
                cw = w["current"]
                st.markdown(f"<div style='font-size: 2.3rem; font-weight: 800; color: #34d399;'>{cw.get('temperature_2m')} °C</div>", unsafe_allow_html=True)
                st.write(f"💧 **Humidity:** {cw.get('relative_humidity_2m')}% | 🌧️ **Rain:** {cw.get('precipitation')} mm")
                st.write(f"💨 **Wind Speed:** {cw.get('wind_speed_10m')} km/h")
                if cw.get("precipitation", 0) > 0.5:
                    st.warning("⚠️ Rain alert: Avoid foliar spraying today.")
                else:
                    st.success("✅ Favourable spraying and irrigation window.")
            else:
                st.info("Weather telemetry loading...")

    with dash_col2:
        with st.container(border=True):
            st.markdown("#### 🌿 " + ("ഇലരോഗ നിർണ്ണയം" if is_mal else "Crop Health Analysis"))
            st.caption("Upload leaf photo to detect disease & get OpenAI remedies.")
            st.markdown("""
            <div style='border: 2px dashed #34d399; border-radius: 12px; padding: 22px; text-align: center; background: rgba(16, 185, 129, 0.15); margin-bottom: 12px;'>
                <div style='font-size: 1.8rem;'>📸</div>
                <div style='color: #a7f3d0; font-weight: 600;'>Drag & Drop Image or Click Below</div>
                <div style='font-size: 0.8rem; color: #cbd5e1;'>MobileNetV2 Vision Model (97.15%)</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("Supports: JPG, PNG • 38 Disease Classes")

    with dash_col3:
        with st.container(border=True):
            st.markdown("#### 💡 " + ("ദ്രുത ഉപദേശം" if is_mal else "Quick Crop Advisory"))
            st.caption(f"Target Crop: **{CROPS_MAL.get(crop, crop) if is_mal else crop}**")
            
            stage = st.selectbox(
                "വളർച്ചാ ഘട്ടം (Growth Stage)" if is_mal else "Growth Stage",
                ["Seedling / Planting", "Vegetative / Tillering", "Flowering / Panicle", "Harvesting"],
                index=1
            )
            
            if st.button("✨ " + ("ശുപാർശ കാണുക (Get Advisory)" if is_mal else "Get Recommendation"), type="primary", use_container_width=True):
                st.success(f"🌱 **{crop} ({stage}):** Ensure split dose application of Potassium and maintain adequate mulch.")

    st.markdown("---")
    
    # Explore Our Services Grid
    st.subheader("🧭 " + ("മറ്റ് സേവനങ്ങൾ പര്യവേക്ഷണം ചെയ്യുക" if is_mal else "Explore Our Services"))
    
    s1, s2, s3 = st.columns(3)
    with s1:
        with st.container(border=True):
            st.markdown("#### 👤 " + ("എന്റെ പ്രൊഫൈൽ" if is_mal else "My Farmer Profile"))
            st.write("Manage your farm acreage, soil classification, irrigation systems, and Krishi Bhavan registration ID.")
    with s2:
        with st.container(border=True):
            st.markdown("#### 💬 " + ("കർഷക ചാറ്റ്" if is_mal else "Direct Farmer Chat"))
            st.write("Chat directly 1-on-1 with nearby Kerala farmers for real-time field advice, crop pricing, and seed exchange.")
    with s3:
        with st.container(border=True):
            st.markdown("#### 🤖 " + ("ഹൈബ്രിഡ് എഐ സഹായി" if is_mal else "Hybrid AI Crop Assistant"))
            st.write("Ask any farming question in English or Malayalam. Combines official KAU PoP documents with live agronomic web research.")

elif canonical_page == "Farmer Profile":
    import importlib
    from pages import profile as profile_page
    importlib.reload(profile_page)
    profile_page.main()

elif canonical_page == "AI Assistant (Hybrid KAU + Web)":
    import importlib
    from pages import assistant as assistant_page
    importlib.reload(assistant_page)
    assistant_page.main()

elif canonical_page == "Crop Health (Disease Scanner)":
    import importlib
    from pages import crop_health as crop_health_page
    importlib.reload(crop_health_page)
    crop_health_page.main()

elif canonical_page == "Soil Health":
    import importlib
    from pages import soil as soil_page
    importlib.reload(soil_page)
    soil_page.main()

elif canonical_page == "Crop Recommendation":
    from pages import crop_recommendation as crop_recommendation_page
    crop_recommendation_page.main()

elif canonical_page == "Weather (Live Location)":
    import importlib
    from pages import weather as weather_page
    importlib.reload(weather_page)
    weather_page.main()

elif canonical_page == "Farmer Connect & Chat":
    import importlib
    from pages import community as community_page
    importlib.reload(community_page)
    community_page.main()

elif canonical_page == "About":
    st.title("About KrishiMitr | കൃഷിമിത്രം")
    if is_mal:
        st.write(
            "കേരളത്തിലെ കർഷകർക്കും ഗവേഷകർക്കും കൃഷി ഉദ്യോഗസ്ഥർക്കുമായി തയ്യാറാക്കിയ വ്യക്തിഗത സ്മാർട്ട് കാർഷിക സഹായിയാണ് കൃഷിമിത്രം."
        )
        st.markdown("""
        - **വിവരശേഖരം:** കേരള കാർഷിക സർവകലാശാല (KAU) പാക്കേജ് ഓഫ് പ്രാക്ടീസസ് (Crops) 2016.
        - **രോഗനിർണ്ണയ മോഡൽ:** 54,305 ചിത്രങ്ങളിലൂടെ പരിശീലിപ്പിച്ച 97.15% കൃത്യതയുള്ള MobileNetV2 ഡീപ് ലേണിംഗ് മോഡൽ.
        - **കർഷക പ്രൊഫൈൽ:** വ്യക്തിഗത കൃഷിഭൂമി, വിളകൾ, മണ്ണുവിവരങ്ങൾ എന്നിവ രേഖപ്പെടുത്താനുള്ള സൗകര്യം.
        - **കർഷക ചാറ്റ്:** മറ്റ് കർഷകരുമായി നേരിട്ടുള്ള 1-on-1 സന്ദേശവിനിമയം.
        - **സഹായം:** കിസാൻ കോൾ സെന്റർ (ടോൾ ഫ്രീ): 1800-180-1551.
        """)
    else:
        st.write(
            "KrishiMitr is an advanced AI agricultural personal decision support system designed specifically for Kerala farmers."
        )
        st.markdown("""
        - **Knowledge Base:** Kerala Agricultural University (KAU) Package of Practices (Crops) 2016.
        - **Vision Model:** MobileNetV2 CNN trained on 54,305 images for 38 plant disease classes (**97.15% validation accuracy**).
        - **Personal Profile:** Track your exact acreage, soil type, irrigation, and crop history.
        - **Direct Farmer Messaging:** 1-on-1 real-time chat with nearby progressive farmers.
        - **Multilingual Support:** Complete English and Malayalam interfaces for all 14 Kerala districts.
        """)
