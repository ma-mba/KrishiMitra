import html

import streamlit as st

from services.auth import load_users
from services.database import get_supabase


DISTRICTS = [
    "Palakkad", "Thrissur", "Ernakulam", "Kozhikode", "Wayanad",
    "Alappuzha", "Kottayam", "Idukki", "Malappuram", "Kannur",
    "Kasaragod", "Kollam", "Pathanamthitta", "Thiruvananthapuram",
]
CROPS = ["Paddy", "Banana", "Coconut", "Pepper", "Rubber", "Cardamom"]


def get_current_user_profile():
    """Return the signed-in user's profile, never a random farmer's profile."""
    return st.session_state.get("user")


def update_current_user_profile(updated_data):
    """Persist editable fields for a real farmer; keep demo changes session-only."""
    current = st.session_state.get("user")
    if not current:
        return False, "Please log in to edit your profile."

    name = str(updated_data.get("name", "")).strip()
    village = str(updated_data.get("village", "")).strip()
    district = updated_data.get("district")
    crop = updated_data.get("crop")

    try:
        acres = float(updated_data.get("acres"))
    except (TypeError, ValueError):
        return False, "Enter a valid land area."

    if not name or len(name) > 120:
        return False, "Enter a name (up to 120 characters)."
    if len(village) > 150:
        return False, "Village must be 150 characters or fewer."
    if district not in DISTRICTS or crop not in CROPS:
        return False, "Select a valid district and crop."
    if not 0.25 <= acres <= 500:
        return False, "Land holding must be between 0.25 and 500 acres."

    editable = {
        "name": name,
        "village": village,
        "district": district,
        "crop": crop,
        "acres": acres,
    }

    if current.get("is_demo"):
        st.session_state["user"] = {**current, **editable}
    else:
        phone = current.get("username")
        farmer_id = current.get("farmer_id")
        if not phone or not farmer_id:
            return False, "Account identity is missing. Please log in again."
        try:
            result = (
                get_supabase()
                .table("farmers")
                .update(editable)
                .eq("phone", phone)
                .eq("farmer_id", farmer_id)
                .execute()
            )
            if not result.data:
                return False, "Profile not found. No changes were saved."
        except Exception:
            return False, "Could not save changes to Supabase. Please try again."
        st.session_state["user"] = {**current, **editable}
    return True, "Profile updated successfully."


def main():
    lang = st.session_state.get("language", "English")
    is_mal = lang == "മലയാളം"
    profile = get_current_user_profile()

    if not profile:
        st.warning("Please log in to view your farmer profile.")
        return

    if is_mal:
        st.title("👤 എന്റെ കർഷക പ്രൊഫൈൽ (Farmer Profile)")
        st.write("നിങ്ങളുടെ കൃഷിയിടത്തിന്റെ വിവരങ്ങളും കർഷക തിരിച്ചറിയൽ കാർഡും.")
    else:
        st.title("👤 My Farmer Profile & Agricultural ID Card")
        st.write("Manage your personal farm details and land holding information.")

    name_safe = html.escape(str(profile.get("name") or "Kerala Farmer"))
    village_safe = html.escape(str(profile.get("village") or "Kerala"))
    district_safe = html.escape(str(profile.get("district") or ""))
    farmer_id_safe = html.escape(str(profile.get("farmer_id") or ""))
    account_label = "Demo Farmer Profile" if profile.get("is_demo") else "KrishiMitra Farmer Profile"

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.35) 100%); border: 1px solid #34d399; border-radius: 16px; padding: 22px 28px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);'>
        <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 18px;'>
                <div style='font-size: 3.2rem; background: rgba(52, 211, 153, 0.2); border-radius: 50%; width: 72px; height: 72px; display: flex; align-items: center; justify-content: center;'>👨‍🌾</div>
                <div>
                    <div style='font-size: 1.8rem; font-weight: 800; color: #ffffff;'>{name_safe}</div>
                    <div style='color: #6ee7b7; font-weight: 600; font-size: 0.95rem;'>{account_label}</div>
                    <div style='color: #cbd5e1; font-size: 0.85rem;'>📍 {village_safe}, {district_safe} • 🆔 {farmer_id_safe}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🌾 " + ("കൃഷിഭൂമി" if is_mal else "Total Land"), f"{profile.get('acres', 0)} " + ("ഏക്കർ" if is_mal else "Acres"))
    with m2:
        st.metric("🌱 " + ("പ്രധാന വിള" if is_mal else "Primary Crop"), str(profile.get("crop") or "—"))
    with m3:
        st.metric("📱 " + ("രജിസ്റ്റർ ചെയ്ത ഫോൺ" if is_mal else "Registered Phone"), str(profile.get("username") or "—"))
    with m4:
        st.metric("💧 " + ("നന രീതി" if is_mal else "Irrigation"), "Not specified")

    st.markdown("---")
    tab1, tab2 = st.tabs([
        "📋 " + ("വിശദാംശങ്ങൾ (Farm Details)" if is_mal else "Farm Overview"),
        "✏️ " + ("വിവരങ്ങൾ തിരുത്തുക (Edit Profile)" if is_mal else "Edit Farm Profile"),
    ])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            with st.container(border=True):
                st.markdown("#### 🌾 " + ("കൃഷിയിട വിവരങ്ങൾ" if is_mal else "Agronomic Parameters"))
                st.write(f"**{'കർഷകന്റെ പേര്' if is_mal else 'Farmer Name'}:** {profile.get('name')}")
                st.write(f"**{'ഫോൺ / യൂസർനെയിം' if is_mal else 'Mobile Account'}:** `{profile.get('username')}`")
                st.write(f"**{'ജില്ല' if is_mal else 'District'}:** {profile.get('district')}")
                st.write(f"**{'ഗ്രാമം / പഞ്ചായത്ത്' if is_mal else 'Village / Panchayat'}:** {profile.get('village') or 'Not specified'}")
        with col_b:
            with st.container(border=True):
                st.markdown("#### 🚜 " + ("വിളകളും തിരിച്ചറിയൽ കാർഡും" if is_mal else "Crops & Identity Credentials"))
                st.write(f"**{'പ്രധാന വിള' if is_mal else 'Primary Crop'}:** {profile.get('crop')}")
                st.write(f"**{'കൃഷിഭൂമി' if is_mal else 'Farmland Size'}:** {profile.get('acres')} Acres")
                st.write(f"**{'രജിസ്ട്രേഷൻ തീയതി' if is_mal else 'Member Since'}:** {profile.get('joined') or '—'}")
                st.write(f"**{'കൃഷിഭവൻ ഐഡി' if is_mal else 'Farmer Reg ID'}:** `{profile.get('farmer_id')}`")

    with tab2:
        st.markdown("#### " + ("നിങ്ങളുടെ കർഷക വിവരങ്ങൾ പുതുക്കുക" if is_mal else "Update Your Farm Information"))
        if profile.get("is_demo"):
            st.info("Demo profile changes last only for this session and are not stored in Supabase.")
        with st.form("edit_farmer_profile_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("കർഷകന്റെ പേര് (Name)" if is_mal else "Farmer Name", value=profile.get("name") or "")
                new_village = st.text_input("ഗ്രാമം / പഞ്ചായത്ത് (Village)" if is_mal else "Village / Panchayat", value=profile.get("village") or "")
                new_acres = st.number_input(
                    "കൃഷിഭൂമി - ഏക്കറിൽ (Acres)" if is_mal else "Land Holding (Acres)",
                    min_value=0.25, max_value=500.0,
                    value=max(0.25, min(500.0, float(profile.get("acres") or 2.0))), step=0.5,
                )
            with c2:
                current_district = profile.get("district")
                new_district = st.selectbox(
                    "ജില്ല (District)" if is_mal else "District", DISTRICTS,
                    index=DISTRICTS.index(current_district) if current_district in DISTRICTS else 0,
                )
                current_crop = profile.get("crop")
                new_crop = st.selectbox(
                    "പ്രധാന വിള (Primary Crop)" if is_mal else "Primary Crop", CROPS,
                    index=CROPS.index(current_crop) if current_crop in CROPS else 0,
                )
            save_btn = st.form_submit_button(
                "💾 " + ("വിവരങ്ങൾ സംരക്ഷിക്കുക (Save Changes)" if is_mal else "Save Profile Changes"),
                type="primary",
            )
            if save_btn:
                success, message = update_current_user_profile({
                    "name": new_name,
                    "village": new_village,
                    "acres": new_acres,
                    "district": new_district,
                    "crop": new_crop,
                })
                if success:
                    st.success("നിങ്ങളുടെ പ്രൊഫൈൽ വിവരങ്ങൾ വിജയകരമായി സംരക്ഷിച്ചു!" if is_mal else message)
                    st.rerun()
                else:
                    st.error(message)
