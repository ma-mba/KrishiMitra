"""KrishiMitra farmer authentication with Supabase and separate demo access."""

from datetime import datetime, timezone
from uuid import uuid4
import time
from collections import deque
from threading import Lock
import streamlit as st
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from services.database import get_supabase

PASSWORD_HASHER = PasswordHasher()

DEFAULT_USERS = {
    "9447123456": {
        "username": "9447123456",
        "name": "Kishore Kumar",
        "district": "Palakkad",
        "village": "Alathur, Chittur Taluk",
        "crop": "Paddy",
        "acres": 3.5,
        "farmer_id": "KL-AGRI-2026-8941",
        "joined": "November 2026",
        "is_demo": True,
    },
    "9847054321": {
        "username": "9847054321",
        "name": "Mary Varghese",
        "district": "Thrissur",
        "village": "Ollur, Thrissur",
        "crop": "Banana",
        "acres": 2.0,
        "farmer_id": "KL-AGRI-2026-5520",
        "joined": "November 2026",
        "is_demo": True,
    },
}


def load_users():
    """Retained for compatibility with the demo-login UI."""
    return {phone: profile.copy() for phone, profile in DEFAULT_USERS.items()}
def save_users(users):
    raise RuntimeError(
        "Local JSON storage is disabled. "
        "Farmer profile changes must be saved to Supabase."
    )


def _session_user(record):
    """Return a safe user profile without password hashes."""
    registered = record.get("registered_at") or datetime.now(timezone.utc).isoformat()
    district = record.get("district") or "Palakkad"
    return {
        "username": record["phone"],
        "name": record["name"],
        "district": district,
        "village": record.get("village") or f"{district} Rural",
        "crop": record.get("crop") or "Paddy",
        "acres": float(record.get("acres") or 0),
        "farmer_id": record["farmer_id"],
        "joined": registered[:10],
        "is_demo": False,
    }


def register_user(name: str, phone: str, password: str,
                  district: str, crop: str, acres: float = 2.0):
    """Register a real farmer in Supabase; never store plaintext passwords."""
    name = name.strip()
    phone = phone.strip()

    if not name:
        return False, "Please enter your name."
    if not (phone.isascii() and phone.isdigit() and len(phone) == 10):
        return False, "Please enter a valid 10-digit mobile number."
    if len(password) < 8:
        return False, "Password must contain at least 8 characters."
    if not 0.25 <= acres <= 500.0:
        return False, "Land holding must be between 0.25 and 500 acres."

    # Prevent a real account from using the same phone as a demo profile.
    if phone in DEFAULT_USERS:
        return False, "This phone number is reserved for a demo profile."

    farmer_id = (
        f"KL-AGRI-{datetime.now(timezone.utc).year}-"
        f"{uuid4().hex[:16].upper()}"
    )
    record = {
        "name": name,
        "phone": phone,
        "password_hash": PASSWORD_HASHER.hash(password),
        "district": district,
        "crop": crop,
        "acres": float(acres),
        "farmer_id": farmer_id,
    }

    try:
        result = get_supabase().table("farmers").insert(record).execute()
        if not result.data:
            return False, "Registration could not be completed. Please try again."
        return True, _session_user(result.data[0])
    except Exception as exc:
        if str(getattr(exc, "code", "")) == "23505":
            return False, "An account with this phone number already exists."
        return False, "Registration is temporarily unavailable. Please try again later."

# Basic server-side login rate limiting.
# Maximum 5 attempts per identifier within 5 minutes.
LOGIN_ATTEMPTS = {}
LOGIN_LOCK = Lock()
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300


def login_allowed(identifier):
    now = time.monotonic()
    key = identifier.strip().casefold()

    with LOGIN_LOCK:
        attempts = LOGIN_ATTEMPTS.setdefault(key, deque())

        while attempts and now - attempts[0] > LOGIN_WINDOW_SECONDS:
            attempts.popleft()

        if len(attempts) >= MAX_LOGIN_ATTEMPTS:
            return False

        # Count every attempt, successful or unsuccessful.
        attempts.append(now)
        return True



def authenticate_user(username_or_phone: str, password: str):
    """Authenticate a registered farmer using Supabase."""
    identifier = username_or_phone.strip()

    if not identifier or not password:
        return None

    if not login_allowed(identifier):
        return None

    try:
        db = get_supabase()
        query = db.table("farmers").select("*")

        if identifier.isascii() and identifier.isdigit():
            result = (
                query.eq("phone", identifier)
                .limit(1)
                .execute()
            )
        else:
            result = (
                query.ilike("name", identifier)
                .limit(100)
                .execute()
            )

        for record in result.data or []:
            try:
                PASSWORD_HASHER.verify(
                    record["password_hash"],
                    password
                )
            except (
                VerifyMismatchError,
                VerificationError,
                InvalidHashError
            ):
                continue

            # Record successful login atomically in Supabase.
            try:
                db.rpc(
                    "record_farmer_login",
                    {"p_farmer_id": record["id"]}
                ).execute()
            except Exception:
                pass

            return _session_user(record)

    except Exception:
        return None

    return None


def _sign_in(user):
    st.session_state["authenticated"] = True
    st.session_state["user"] = user
    st.session_state["district"] = user.get("district", "Palakkad")
    st.session_state["crop"] = user.get("crop", "Paddy")
    st.rerun()


def render_login_portal():
    """Render the bilingual farmer login, registration, and demo portal."""
    lang = st.session_state.get("language", "English")
    is_mal = lang == "മലയാളം"

    st.markdown(
        """
        <div style='text-align: center; margin-top: 10px; margin-bottom: 24px;'>
            <div style='font-size: 3.5rem;'>🌱</div>
            <div style='font-size: 2.2rem; font-weight: 800; color: #34d399;'>
                KrishiMitr | കൃഷിമിത്രം
            </div>
            <div style='color: #a7f3d0; font-size: 1.05rem;'>
                AI-Powered Personal Smart Agriculture for Kerala Farmers
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            tab_login, tab_register, tab_quick = st.tabs([
                "ലോഗിൻ (Login)" if is_mal else "Farmer Login",
                "പുതിയ കർഷകൻ (Register)" if is_mal else "Create Account",
                "ഡെമോ ലോഗിൻ (Quick Demo)" if is_mal else "Demo Access",
            ])

            with tab_login:
                st.markdown("#### " + (
                    "നിങ്ങളുടെ അക്കൗണ്ടിലേക്ക് പ്രവേശിക്കുക"
                    if is_mal else "Sign in to your farm portal"
                ))
                with st.form("farmer_login_form"):
                    user_input = st.text_input(
                        "ഫോൺ നമ്പർ അല്ലെങ്കിൽ പേര് (Mobile or Name):"
                        if is_mal else "Mobile Number or Username:",
                        placeholder="e.g. 9447123456 or Kishore Kumar",
                    )
                    pass_input = st.text_input(
                        "പാസ്‌വേഡ് (Password):" if is_mal else "Password:",
                        type="password",
                        placeholder="••••••••",
                    )
                    login_btn = st.form_submit_button(
                        "ലോഗിൻ ചെയ്യുക (Login)" if is_mal else "Login",
                        type="primary", use_container_width=True,
                    )

                if login_btn:
                    if user_input and pass_input:
                        user = authenticate_user(user_input, pass_input)
                        if user:
                            _sign_in(user)
                        else:
                            st.error(
                                "തെറ്റായ ഫോൺ നമ്പറോ പാസ്‌വേഡോ ആണ്."
                                if is_mal else "Invalid mobile number or password."
                            )
                    else:
                        st.warning(
                            "ദയവായി ഫോൺ നമ്പറും പാസ്‌വേഡും നൽകുക."
                            if is_mal else "Please enter both mobile number and password."
                        )

            with tab_register:
                st.markdown("#### " + (
                    "പുതിയ കർഷക രജിസ്ട്രേഷൻ"
                    if is_mal else "New Farmer Registration"
                ))
                with st.form("farmer_register_form"):
                    reg_name = st.text_input(
                        "കർഷകന്റെ പേര് (Full Name):" if is_mal else "Full Name:",
                        placeholder="e.g. Ramesh Menon",
                    )
                    reg_phone = st.text_input(
                        "ഫോൺ നമ്പർ (Mobile Number):" if is_mal else "Mobile Number:",
                        placeholder="e.g. 9847123456",
                    )
                    reg_pass = st.text_input(
                        "പാസ്‌വേഡ് (Password):" if is_mal else "Create Password:",
                        type="password", placeholder="••••••••",
                    )
                    districts = [
                        "Palakkad", "Thrissur", "Ernakulam", "Kozhikode",
                        "Wayanad", "Alappuzha", "Kottayam", "Idukki",
                        "Malappuram", "Kannur", "Kasaragod", "Kollam",
                        "Pathanamthitta", "Thiruvananthapuram",
                    ]
                    reg_dist = st.selectbox(
                        "ജില്ല (District):" if is_mal else "District:",
                        districts, index=0,
                    )
                    crops = [
                        "Paddy", "Banana", "Coconut", "Pepper", "Rubber", "Cardamom"
                    ]
                    reg_crop = st.selectbox(
                        "പ്രധാന വിള (Primary Crop):" if is_mal else "Primary Crop:",
                        crops, index=0,
                    )
                    reg_acres = st.number_input(
                        "കൃഷിഭൂമി (Land in Acres):" if is_mal else "Land Holding (Acres):",
                        min_value=0.25, max_value=500.0, value=2.0, step=0.5,
                    )
                    st.caption(
                        "Your details are stored securely to manage your farmer account. "
                        "Passwords are stored as hashes, not readable text."
                    )
                    reg_btn = st.form_submit_button(
                        "🌱 " + (
                            "അക്കൗണ്ട് നിർമ്മിക്കുക (Register)"
                            if is_mal else "Register My Farm"
                        ),
                        type="primary", use_container_width=True,
                    )

                if reg_btn:
                    if reg_name and reg_phone and reg_pass:
                        ok, res = register_user(
                            reg_name, reg_phone, reg_pass,
                            reg_dist, reg_crop, reg_acres,
                        )
                        if ok:
                            _sign_in(res)
                        else:
                            st.error(res)
                    else:
                        st.warning(
                            "എല്ലാ കോളങ്ങളും പൂരിപ്പിക്കുക."
                            if is_mal else "Please fill out all required fields."
                        )

            with tab_quick:
                st.markdown("#### " + (
                    "ഒറ്റ ക്ലിക്കിൽ ഡെമോ ലോഗിൻ ചെയ്യുക"
                    if is_mal else "One-Click Demo Access"
                ))
                st.write("For testing after deployment, select an existing profile:")
                c_d1, c_d2 = st.columns(2)
                with c_d1:
                    if st.button(
                        "👨‍🌾 Kishore Kumar\n(Palakkad • Paddy)",
                        use_container_width=True,
                    ):
                        _sign_in(load_users()["9447123456"])
                with c_d2:
                    if st.button(
                        "👩‍🌾 Mary Varghese\n(Thrissur • Banana)",
                        use_container_width=True,
                    ):
                        _sign_in(load_users()["9847054321"])
