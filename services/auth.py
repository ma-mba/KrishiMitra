import json
import hashlib
import streamlit as st
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parents[1] / "data" / "users.json"

DEFAULT_USERS = {
    "9447123456": {
        "username": "9447123456",
        "name": "Kishore Kumar",
        "password_hash": hashlib.sha256("farmer123".encode()).hexdigest(),
        "district": "Palakkad",
        "village": "Alathur, Chittur Taluk",
        "crop": "Paddy",
        "acres": 3.5,
        "farmer_id": "KL-AGRI-2026-8941",
        "joined": "November 2026"
    },
    "9847054321": {
        "username": "9847054321",
        "name": "Mary Varghese",
        "password_hash": hashlib.sha256("farmer123".encode()).hexdigest(),
        "district": "Thrissur",
        "village": "Ollur, Thrissur",
        "crop": "Banana",
        "acres": 2.0,
        "farmer_id": "KL-AGRI-2026-5520",
        "joined": "November 2026"
    }
}

def load_users():
    if not USERS_FILE.exists():
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        save_users(DEFAULT_USERS)
        return DEFAULT_USERS
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_USERS

def save_users(users):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username_or_phone: str, password: str):
    users = load_users()
    clean_user = username_or_phone.strip()
    
    # Check by username/phone
    if clean_user in users:
        u = users[clean_user]
        if u.get("password_hash") == hash_pw(password):
            return u
            
    # Check by name
    for u in users.values():
        if u.get("name", "").lower() == clean_user.lower():
            if u.get("password_hash") == hash_pw(password):
                return u
    return None

def register_user(name: str, phone: str, password: str, district: str, crop: str, acres: float = 2.0):
    users = load_users()
    clean_phone = phone.strip()
    
    if clean_phone in users:
        return False, "An account with this phone number already exists."
        
    farmer_num = 1000 + len(users) + 1
    new_user = {
        "username": clean_phone,
        "name": name.strip(),
        "password_hash": hash_pw(password),
        "district": district,
        "village": f"{district} Rural",
        "crop": crop,
        "acres": acres,
        "farmer_id": f"KL-AGRI-2026-{farmer_num}",
        "joined": "November 2026"
    }
    users[clean_phone] = new_user
    save_users(users)
    return True, new_user

def render_login_portal():
    """Render a modern, lush green farmer login & signup screen for deployed production."""
    lang = st.session_state.get('language', 'English')
    is_mal = (lang == "മലയാളം")

    st.markdown("""
    <div style='text-align: center; margin-top: 10px; margin-bottom: 24px;'>
        <div style='font-size: 3.5rem;'>🌱</div>
        <div style='font-size: 2.2rem; font-weight: 800; color: #34d399;'>KrishiMitr | കൃഷിമിത്രം</div>
        <div style='color: #a7f3d0; font-size: 1.05rem;'>AI-Powered Personal Smart Agriculture for Kerala Farmers</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            tab_login, tab_register, tab_quick = st.tabs([
                 ("ലോഗിൻ (Login)" if is_mal else "Farmer Login"),
                ("പുതിയ കർഷകൻ (Register)" if is_mal else "Create Account"),
                ("ഡെമോ ലോഗിൻ (Quick Demo)" if is_mal else "Demo Access")
            ])

            # 1. LOGIN TAB
            with tab_login:
                st.markdown("#### " + ("നിങ്ങളുടെ അക്കൗണ്ടിലേക്ക് പ്രവേശിക്കുക" if is_mal else "Sign in to your farm portal"))
                with st.form("farmer_login_form"):
                    user_input = st.text_input(
                        "ഫോൺ നമ്പർ അല്ലെങ്കിൽ പേര് (Mobile or Name):" if is_mal else "Mobile Number or Username:",
                        placeholder="e.g. 9447123456 or Kishore Kumar"
                    )
                    pass_input = st.text_input(
                        "പാസ്‌വേഡ് (Password):" if is_mal else "Password:",
                        type="password",
                        placeholder="••••••••"
                    )
                    login_btn = st.form_submit_button("" + ("ലോഗിൻ ചെയ്യുക (Login)" if is_mal else "Login"), type="primary", use_container_width=True)

                    if login_btn:
                        if user_input and pass_input:
                            user = authenticate_user(user_input, pass_input)
                            if user:
                                st.session_state["authenticated"] = True
                                st.session_state["user"] = user
                                st.session_state["district"] = user.get("district", "Palakkad")
                                st.session_state["crop"] = user.get("crop", "Paddy")
                                st.success("വിജയകരമായി ലോഗിൻ ചെയ്തു!" if is_mal else "Successfully logged in!")
                                st.rerun()
                            else:
                                st.error("തെറ്റായ ഫോൺ നമ്പറോ പാസ്‌വേഡോ ആണ്." if is_mal else "Invalid mobile number or password.")
                        else:
                            st.warning("ദയവായി ഫോൺ നമ്പറും പാസ്‌വേഡും നൽകുക." if is_mal else "Please enter both mobile number and password.")

            # 2. REGISTER TAB
            with tab_register:
                st.markdown("#### " + ("പുതിയ കർഷക രജിസ്ട്രേഷൻ" if is_mal else "New Farmer Registration"))
                with st.form("farmer_register_form"):
                    reg_name = st.text_input("കർഷകന്റെ പേര് (Full Name):" if is_mal else "Full Name:", placeholder="e.g. Ramesh Menon")
                    reg_phone = st.text_input("ഫോൺ നമ്പർ (Mobile Number):" if is_mal else "Mobile Number:", placeholder="e.g. 9847123456")
                    reg_pass = st.text_input("പാസ്‌വേഡ് (Password):" if is_mal else "Create Password:", type="password", placeholder="••••••••")
                    
                    districts = ["Palakkad", "Thrissur", "Ernakulam", "Kozhikode", "Wayanad", "Alappuzha", "Kottayam", "Idukki", "Malappuram", "Kannur", "Kasaragod", "Kollam", "Pathanamthitta", "Thiruvananthapuram"]
                    reg_dist = st.selectbox("ജില്ല (District):" if is_mal else "District:", districts, index=0)
                    
                    crops = ["Paddy", "Banana", "Coconut", "Pepper", "Rubber", "Cardamom"]
                    reg_crop = st.selectbox("പ്രധാന വിള (Primary Crop):" if is_mal else "Primary Crop:", crops, index=0)
                    
                    reg_acres = st.number_input("കൃഷിഭൂമി (Land in Acres):" if is_mal else "Land Holding (Acres):", min_value=0.25, max_value=500.0, value=2.0, step=0.5)

                    reg_btn = st.form_submit_button("🌱 " + ("അക്കൗണ്ട് നിർമ്മിക്കുക (Register)" if is_mal else "Register My Farm"), type="primary", use_container_width=True)

                    if reg_btn:
                        if reg_name and reg_phone and reg_pass:
                            ok, res = register_user(reg_name, reg_phone, reg_pass, reg_dist, reg_crop, reg_acres)
                            if ok:
                                st.session_state["authenticated"] = True
                                st.session_state["user"] = res
                                st.session_state["district"] = reg_dist
                                st.session_state["crop"] = reg_crop
                                st.success("അക്കൗണ്ട് വിജയകരമായി നിർമ്മിച്ചു!" if is_mal else "Farmer account successfully registered!")
                                st.rerun()
                            else:
                                st.error(res)
                        else:
                            st.warning("എല്ലാ കോളങ്ങളും പൂരിപ്പിക്കുക." if is_mal else "Please fill out all required fields.")

            # 3. QUICK DEMO TAB
            with tab_quick:
                st.markdown("#### " + ("ഒറ്റ ക്ലിക്കിൽ ഡെമോ ലോഗിൻ ചെയ്യുക" if is_mal else "One-Click Demo Access"))
                st.write("For testing after deployment, select an existing profile:")
                
                c_d1, c_d2 = st.columns(2)
                with c_d1:
                    if st.button("👨‍🌾 Kishore Kumar\n(Palakkad • Paddy)", use_container_width=True):
                        users = load_users()
                        u = users.get("9447123456", list(users.values())[0])
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = u
                        st.session_state["district"] = u.get("district", "Palakkad")
                        st.session_state["crop"] = u.get("crop", "Paddy")
                        st.rerun()
                with c_d2:
                    if st.button("👩‍🌾 Mary Varghese\n(Thrissur • Banana)", use_container_width=True):
                        users = load_users()
                        u = users.get("9847054321", list(users.values())[1])
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = u
                        st.session_state["district"] = u.get("district", "Thrissur")
                        st.session_state["crop"] = u.get("crop", "Banana")
                        st.rerun()
