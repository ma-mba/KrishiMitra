import streamlit as st
import json
import os
from pathlib import Path
from services.auth import load_users, save_users

def get_current_user_profile():
    user = st.session_state.get("user")
    if user:
        return user
    users = load_users()
    return list(users.values())[0]

def update_current_user_profile(updated_data):
    users = load_users()
    username = updated_data.get("username")
    if username in users:
        users[username].update(updated_data)
        save_users(users)
        st.session_state["user"] = users[username]
    else:
        # Save by key
        users[username or "default"] = updated_data
        save_users(users)
        st.session_state["user"] = updated_data

def main():
    lang = st.session_state.get('language', 'English')
    is_mal = (lang == "മലയാളം")

    profile = get_current_user_profile()

    if is_mal:
        st.title("👤 എന്റെ കർഷക പ്രൊഫൈൽ (Farmer Profile)")
        st.write("നിങ്ങളുടെ കൃഷിയിടത്തിന്റെ വിവരങ്ങളും, മുൻഗണനകളും, കർഷക തിരിച്ചറിയൽ കാർഡും.")
    else:
        st.title("👤 My Farmer Profile & Agricultural ID Card")
        st.write("Manage your personal farm details, acreage, soil types, and Krishi Bhavan farmer credentials.")

    # Top Farmer Identity Badge
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(5, 150, 105, 0.35) 100%); border: 1px solid #34d399; border-radius: 16px; padding: 22px 28px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);'>
        <div style='display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 18px;'>
                <div style='font-size: 3.2rem; background: rgba(52, 211, 153, 0.2); border-radius: 50%; width: 72px; height: 72px; display: flex; align-items: center; justify-content: center;'>👨‍🌾</div>
                <div>
                    <div style='font-size: 1.8rem; font-weight: 800; color: #ffffff;'>{profile.get('name', 'Kerala Farmer')}</div>
                    <div style='color: #6ee7b7; font-weight: 600; font-size: 0.95rem;'>Verified Progressive Farmer (പുരോഗമന കർഷകൻ)</div>
                    <div style='color: #cbd5e1; font-size: 0.85rem;'>📍 {profile.get('village', 'Kerala')}, {profile.get('district')} • 🆔 {profile.get('farmer_id')}</div>
                </div>
            </div>
            <div style='text-align: right; margin-top: 10px;'>
                <span style='background: #10b981; color: white; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 0.85rem;'>Certified Organic Member</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Quick Metric Tiles
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🌾 " + ("കൃഷിഭൂമി" if is_mal else "Total Land"), f"{profile.get('acres', 3.5)} " + ("ഏക്കർ" if is_mal else "Acres"))
    with m2:
        st.metric("🌱 " + ("പ്രധാന വിള" if is_mal else "Primary Crop"), str(profile.get('crop', 'Paddy')))
    with m3:
        st.metric("📱 " + ("രജിസ്റ്റർ ചെയ്ത ഫോൺ" if is_mal else "Registered Phone"), str(profile.get('username', '+91 94471 23456')))
    with m4:
        st.metric("💧 " + ("നന രീതി" if is_mal else "Irrigation"), "Drip / Well")

    st.markdown("---")

    # Profile Tabs: View Details & Edit Profile
    tab1, tab2 = st.tabs([
        "📋 " + ("വിശദാംശങ്ങൾ (Farm Details)" if is_mal else "Farm Overview"),
        "✏️ " + ("വിവരങ്ങൾ തിരുത്തുക (Edit Profile)" if is_mal else "Edit Farm Profile")
    ])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            with st.container(border=True):
                st.markdown("#### 🌾 " + ("കൃഷിയിട വിവരങ്ങൾ" if is_mal else "Agronomic Parameters"))
                st.write(f"**{'കർഷകന്റെ പേര്' if is_mal else 'Farmer Name'}:** {profile.get('name')}")
                st.write(f"**{'ഫോൺ / യൂസർനെയിം' if is_mal else 'Mobile Account'}:** `{profile.get('username')}`")
                st.write(f"**{'ജില്ല' if is_mal else 'District'}:** {profile.get('district')}")
                st.write(f"**{'ഗ്രാമം / പഞ്ചായത്ത്' if is_mal else 'Village / Panchayat'}:** {profile.get('village')}")
        
        with col_b:
            with st.container(border=True):
                st.markdown("#### 🚜 " + ("വിളകളും തിരിച്ചറിയൽ കാർഡും" if is_mal else "Crops & Identity Credentials"))
                st.write(f"**{'പ്രധാന വിള' if is_mal else 'Primary Crop'}:** {profile.get('crop')}")
                st.write(f"**{'കൃഷിഭൂമി' if is_mal else 'Farmland Size'}:** {profile.get('acres')} Acres")
                st.write(f"**{'രജിസ്ട്രേഷൻ തീയതി' if is_mal else 'Member Since'}:** {profile.get('joined', 'Nov 2026')}")
                st.write(f"**{'കൃഷിഭവൻ ഐഡി' if is_mal else 'Farmer Reg ID'}:** `{profile.get('farmer_id')}`")

    with tab2:
        st.markdown("#### " + ("നിങ്ങളുടെ കർഷക വിവരങ്ങൾ പുതുക്കുക" if is_mal else "Update Your Farm Information"))
        with st.form("edit_farmer_profile_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("കർഷകന്റെ പേര് (Name)" if is_mal else "Farmer Name", value=profile.get('name', ''))
                new_village = st.text_input("ഗ്രാമം / പഞ്ചായത്ത് (Village)" if is_mal else "Village / Panchayat", value=profile.get('village', ''))
                new_acres = st.number_input("കൃഷിഭൂമി - ഏക്കറിൽ (Acres)" if is_mal else "Land Holding (Acres)", value=float(profile.get('acres', 3.5)), step=0.5)
            with c2:
                all_districts = ["Palakkad", "Thrissur", "Ernakulam", "Kozhikode", "Wayanad", "Alappuzha", "Kottayam", "Idukki", "Malappuram", "Kannur", "Kasaragod", "Kollam", "Pathanamthitta", "Thiruvananthapuram"]
                cur_dist_idx = all_districts.index(profile.get('district', 'Palakkad')) if profile.get('district') in all_districts else 0
                new_district = st.selectbox("ജില്ല (District)" if is_mal else "District", all_districts, index=cur_dist_idx)
                
                all_crops = ["Paddy", "Banana", "Coconut", "Pepper", "Rubber", "Cardamom"]
                cur_crop_idx = all_crops.index(profile.get('crop', 'Paddy')) if profile.get('crop') in all_crops else 0
                new_crop = st.selectbox("പ്രധാന വിള (Primary Crop)" if is_mal else "Primary Crop", all_crops, index=cur_crop_idx)

            save_btn = st.form_submit_button("💾 " + ("വിവരങ്ങൾ സംരക്ഷിക്കുക (Save Changes)" if is_mal else "Save Profile Changes"), type="primary")
            if save_btn:
                profile["name"] = new_name
                profile["village"] = new_village
                profile["acres"] = new_acres
                profile["district"] = new_district
                profile["crop"] = new_crop
                update_current_user_profile(profile)
                
                # Sync with session state
                st.session_state["district"] = new_district
                st.session_state["crop"] = new_crop
                
                st.success("നിങ്ങളുടെ പ്രൊഫൈൽ വിവരങ്ങൾ വിജയകരമായി സംരക്ഷിച്ചു!" if is_mal else "Farmer profile successfully updated!")
                st.rerun()
