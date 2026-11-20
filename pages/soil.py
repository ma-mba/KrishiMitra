import streamlit as st

CROP_SOIL_STANDARDS = {
    "Paddy": {
        "ideal_ph": (5.5, 6.5),
        "ideal_moisture": (60, 85),
        "ideal_n": (140, 220),  # mg/kg (available)
        "ideal_p": (25, 55),
        "ideal_k": (120, 200),
        "recommendations": {
            "English": {
                "lime": "If pH < 5.5, apply Agricultural Lime (Calcium Carbonate) or Dolomite @ 600 kg/ha (250 kg/acre) 14 days before transplanting.",
                "fertilizer": "For High Yielding Varieties (HYV): Recommended N:P:K is 90:45:45 kg/ha (Urea: Rajphos/DAP: MOP = 200:225:75 kg/ha). Apply 1/3 N + full P + 1/2 K as basal, 1/3 N at maximum tillering, and 1/3 N + 1/2 K at panicle initiation.",
                "organic": "Apply well-decomposed FYM or compost @ 5 tonnes/ha. Incorporate green manure (Daincha or Sunnhemp) 10 days before puddling.",
                "micronutrient": "Apply Zinc Sulphate @ 25 kg/ha if zinc deficiency (Khaira disease / brown rusty leaf blotches) is observed."
            },
            "Malayalam": {
                "lime": "മണ്ണിന്റെ pH 5.5-ൽ കുറവാണെങ്കിൽ, നടീലിന് 14 ദിവസം മുൻപ് ഹെക്ടറിന് 600 കിലോഗ്രാം കുമ്മായം അല്ലെങ്കിൽ ഡോളമൈറ്റ് ചേർക്കുക.",
                "fertilizer": "ഉയർന്ന വിളവ് തരുന്ന ഇനങ്ങൾക്ക് N:P:K അനുപാതം 90:45:45 കി.ഗ്രാം/ഹെക്ടർ. അടിവളമായി മൂന്നിലൊന്ന് നൈട്രജനും മുഴുവൻ ഫോസ്ഫറസും പകുതി പൊട്ടാഷും നൽകുക. ബാക്കി രണ്ട് തവണകളായി (കൂമ്പ് പൊട്ടുമ്പോഴും കതിര് വരുമ്പോഴും) നൽകുക.",
                "organic": "ഹെക്ടറിന് 5 ടൺ കാലിവളം അല്ലെങ്കിൽ കമ്പോസ്റ്റ് ചേർക്കുക. പച്ചിലവളങ്ങളായ ഡെയ്ഞ്ച, ചണ എന്നിവ നടീലിന് മുൻപ് ഉഴുതുചേർക്കുക.",
                "micronutrient": "സിങ്ക് കുറവ് കാണുകയാണെങ്കിൽ ഹെക്ടറിന് 25 കി.ഗ്രാം സിങ്ക് സൾഫേറ്റ് പ്രയോഗിക്കുക."
            }
        }
    },
    "Banana": {
        "ideal_ph": (6.0, 7.5),
        "ideal_moisture": (50, 75),
        "ideal_n": (160, 260),
        "ideal_p": (30, 65),
        "ideal_k": (200, 350),  # Heavy K feeder
        "recommendations": {
            "English": {
                "lime": "Apply 500g slaked lime or dolomite per pit in April-May before planting suckers to neutralize soil acidity.",
                "fertilizer": "For Nendran: 300g N, 115g P2O5, 450g K2O per plant per year (Urea: Rajphos: MOP = 650g : 575g : 750g). Apply in 4 equal splits at 2nd, 3rd, 4th, and 5th month after planting.",
                "organic": "Apply 10-15 kg well-rotted FYM/compost and 1 kg neem cake per pit at planting to prevent nematode and borer attacks.",
                "micronutrient": "Spray micronutrient mixture (Ayur Banana / KAU Banana Micronutrient) @ 5g/L at 3rd and 5th month."
            },
            "Malayalam": {
                "lime": "വാഴ നടുന്നതിന് മുൻപ് കുഴിയിൽ 500 ഗ്രാം കുമ്മായം അല്ലെങ്കിൽ ഡോളമൈറ്റ് ചേർത്ത് മണ്ണുമായി ഇളക്കുക.",
                "fertilizer": "നേന്ത്രവാഴയ്ക്ക് ഒരു ചെടിക്ക് 300 ഗ്രാം നൈട്രജൻ, 115 ഗ്രാം ഫോസ്ഫറസ്, 450 ഗ്രാം പൊട്ടാഷ്. നട്ട് 2, 3, 4, 5 മാസങ്ങളിൽ തുല്യ ഗഡുക്കളായി നൽകുക.",
                "organic": "കുഴിയൊന്നിന് 10-15 കി.ഗ്രാം ചാണകപ്പൊടിയും 1 കി.ഗ്രാം വേപ്പിൻപിണ്ണാക്കും നൽകുന്നത് നിമാവിരകളെയും തണ്ടുതുരപ്പനെയും തടയും.",
                "micronutrient": "3-ാം മാസത്തിലും 5-ാം മാസത്തിലും വാഴയ്ക്കുള്ള മൈക്രോന്യൂട്രിയന്റ് മിശ്രിതം 5 ഗ്രാം/ലിറ്റർ വെള്ളത്തിൽ തളിക്കുക."
            }
        }
    },
    "Coconut": {
        "ideal_ph": (5.5, 7.0),
        "ideal_moisture": (45, 70),
        "ideal_n": (120, 200),
        "ideal_p": (20, 50),
        "ideal_k": (150, 280),
        "recommendations": {
            "English": {
                "lime": "Apply 1 kg Agricultural lime or dolomite per adult palm in the basin (1.8m radius) during April-May.",
                "fertilizer": "For adult palm/year: 500g N, 320g P2O5, 1200g K2O (Urea: Rajphos: Muriate of Potash = 1.1 kg : 1.6 kg : 2.0 kg). Apply 1/3 dose in May-June and 2/3 dose in Sept-Oct.",
                "organic": "Apply 25-50 kg green leaf or compost per palm annually along with coir pith mulch around the basin.",
                "micronutrient": "Apply 500g Magnesium Sulphate (Epsom salt) per palm annually to prevent yellowing and frond chlorosis."
            },
            "Malayalam": {
                "lime": "മഴയ്ക്ക് മുൻപ് (മേയ് മാസത്തിൽ) തെങ്ങിൻ തടത്തിൽ 1 കി.ഗ്രാം കുമ്മായം അല്ലെങ്കിൽ ഡോളമൈറ്റ് വിതറി ഇളക്കുക.",
                "fertilizer": "ഒരു തെങ്ങിന് പ്രതിവർഷം 500 ഗ്രാം N, 320 ഗ്രാം P, 1200 ഗ്രാം K (യൂറിയ 1.1 കി.ഗ്രാം, രാജ്ഫോസ് 1.6 കി.ഗ്രാം, പൊട്ടാഷ് 2 കി.ഗ്രാം). മേയ്-ജൂൺ മാസത്തിലും സെപ്റ്റംബർ-ഒക്ടോബർ മാസത്തിലുമായി 2 തവണകളായി നൽകുക.",
                "organic": "ഒരു തെങ്ങിന് 25-50 കി.ഗ്രാം കമ്പോസ്റ്റോ പച്ചിലവളമോ നൽകി ചകിരിച്ചോറ് കൊണ്ട് തടം പുതയിടുക.",
                "micronutrient": "ഓലകൾ മഞ്ഞളിക്കുന്നത് ഒഴിവാക്കാൻ വർഷത്തിലൊരിക്കൽ 500 ഗ്രാം മഗ്നീഷ്യം സൾഫേറ്റ് (എപ്സം സാൾട്ട്) തടത്തിൽ നൽകുക."
            }
        }
    },
    "Pepper": {
        "ideal_ph": (5.5, 6.5),
        "ideal_moisture": (50, 75),
        "ideal_n": (140, 220),
        "ideal_p": (25, 55),
        "ideal_k": (130, 240),
        "recommendations": {
            "English": {
                "lime": "Apply 500g slaked lime or dolomite per standard (vine base) in April-May every alternate year.",
                "fertilizer": "For mature vine (3+ years): 50g N, 50g P2O5, 150g K2O per year in 2 splits (May-June and August-September).",
                "organic": "Apply 10 kg compost enriched with *Trichoderma harzianum* (50g) to protect against Phytophthora foot rot (Quick wilt).",
                "micronutrient": "Foliar spray of 1% Bordeaux mixture + zinc sulfate (0.25%) before South-West monsoon onset."
            },
            "Malayalam": {
                "lime": "രണ്ട് വർഷത്തിലൊരിക്കൽ ഏപ്രിൽ-മേയ് മാസത്തിൽ കുരുമുളക് കൊടിയുടെ ചുവട്ടിൽ 500 ഗ്രാം കുമ്മായം ചേർക്കുക.",
                "fertilizer": "ഒരു കൊടിക്ക് പ്രതിവർഷം 50 ഗ്രാം N, 50 ഗ്രാം P, 150 ഗ്രാം K. മേയ്-ജൂൺ, ആഗസ്റ്റ്-സെപ്റ്റംബർ മാസങ്ങളിലായി 2 തവണ നൽകുക.",
                "organic": "ദ്രുതവാട്ടത്തിനെതിരെ 10 കി.ഗ്രാം ട്രൈക്കോഡെർമ ചേർത്ത ചാണകപ്പൊടി ചുവട്ടിൽ ഇടുക.",
                "micronutrient": "കാലവർഷത്തിന് മുൻപായി 1% ബോർഡോ മിശ്രിതവും സിങ്ക് സൾഫേറ്റും ഇലകളിൽ തളിക്കുക."
            }
        }
    },
    "Rubber": {
        "ideal_ph": (4.5, 6.0),
        "ideal_moisture": (40, 65),
        "ideal_n": (100, 180),
        "ideal_p": (15, 45),
        "ideal_k": (100, 190),
        "recommendations": {
            "English": {
                "lime": "Rubber tolerates acidic soils. Liming is needed only if pH drops below 4.5 (@ 250 kg/ha).",
                "fertilizer": "Apply 10:10:4:1.5 NPKMg fertilizer mixture @ 400 kg/ha in two splits (March-April and September-October).",
                "organic": "Establish legume cover crops like *Mucuna bracteata* or *Pueraria phaseoloides* to fix atmospheric nitrogen and prevent soil erosion.",
                "micronutrient": "Ensure magnesium supply via Dolomite or Magnesium sulphate if interveinal chlorosis occurs."
            },
            "Malayalam": {
                "lime": "റബ്ബർ അമ്ലതയുള്ള മണ്ണിൽ നന്നായി വളരും. pH 4.5-ൽ താഴെയാണെങ്കിൽ മാത്രം ഹെക്ടറിന് 250 കി.ഗ്രാം കുമ്മായം നൽകുക.",
                "fertilizer": "10:10:4:1.5 NPKMg മിശ്രിതം ഹെക്ടറിന് 400 കി.ഗ്രാം വീതം മാർച്ച്-ഏപ്രിൽ, സെപ്റ്റംബർ-ഒക്ടോബർ മാസങ്ങളിലായി നൽകുക.",
                "organic": "മണ്ണൊലിപ്പ് തടയാനും നൈട്രജൻ വർദ്ധിപ്പിക്കാനും മുകുന, പ്യുറേറിയ തുടങ്ങിയ പയർവർഗ്ഗ ആവരണവിളകൾ വളർത്തുക.",
                "micronutrient": "ഇലകളിൽ മഞ്ഞളിപ്പ് കണ്ടാൽ മഗ്നീഷ്യം സൾഫേറ്റ് അല്ലെങ്കിൽ ഡോളമൈറ്റ് നൽകുക."
            }
        }
    },
    "Cardamom": {
        "ideal_ph": (4.5, 5.8),
        "ideal_moisture": (60, 85),
        "ideal_n": (150, 250),
        "ideal_p": (30, 60),
        "ideal_k": (160, 260),
        "recommendations": {
            "English": {
                "lime": "Apply dolomite @ 250 kg/ha once in 2 years to supply calcium and magnesium without over-raising pH.",
                "fertilizer": "High yielding cardamom under rainfed conditions: 75:75:150 kg/ha N:P2O5:K2O in 2 splits (May-June and Sept-Oct). Under irrigation: 120:120:240 kg/ha in 4 splits.",
                "organic": "Apply 5 tonnes/ha neem cake and well-rotted forest compost. Maintain thick leaf mulch.",
                "micronutrient": "Foliar application of Zinc (0.25%) and Boron (0.1%) promotes better capsule setting and prevents premature fruit drop."
            },
            "Malayalam": {
                "lime": "രണ്ട് വർഷത്തിലൊരിക്കൽ ഹെക്ടറിന് 250 കി.ഗ്രാം ഡോളമൈറ്റ് ചേർക്കുക.",
                "fertilizer": "വിളവിന് ഹെക്ടറിന് 75:75:150 കി.ഗ്രാം N:P:K രണ്ട് തവണകളായി നൽകുക. നനയുള്ള തോട്ടങ്ങളിൽ 120:120:240 കി.ഗ്രാം നാല് തവണയായി നൽകാം.",
                "organic": "ഹെക്ടറിന് 5 ടൺ വേപ്പിൻപിണ്ണാക്കും വനമണ്ണും കമ്പോസ്റ്റും നൽകി പുതയിടൽ നിലനിർത്തുക.",
                "micronutrient": "കായ്പിടുത്തം വർദ്ധിപ്പിക്കാൻ 0.25% സിങ്കും 0.1% ബോറോണും ഇലകളിൽ തളിക്കുക."
            }
        }
    }
}

def analyze_nutrient(val, low, high, is_mal):
    if val < low:
        return ("⚠️ കുറവ് (Low)" if is_mal else "⚠️ Deficit / Low", "#ff4d4f")
    elif val > high:
        return ("⚠️ അധികം (Excess)" if is_mal else "⚠️ Excess / High", "#faad14")
    else:
        return ("✅ അനുയോജ്യം (Optimal)" if is_mal else "✅ Optimal / Balanced", "#52c41a")

def main():
    lang = st.session_state.get('language', 'English')
    is_mal = (lang == "മലയാളം")

    if is_mal:
        st.title("🧪 വിളാധിഷ്ഠിത മണ്ണ് പരിശോധന & വളനിർണ്ണയം")
        st.write("നിങ്ങളുടെ മണ്ണിന്റെ പരിശോധനാ ഫലങ്ങളും തിരഞ്ഞെടുത്ത വിളയും നൽകി കേരള കാർഷിക സർവകലാശാല (KAU) മാനദണ്ഡപ്രകാരമുള്ള ശാസ്ത്രീയ വളപ്രയോഗം അറിയുക.")
        crop_label = "പരിശോധിക്കേണ്ട വിള:"
    else:
        st.title("🧪 Crop-Specific Soil Health Assessment")
        st.write("Enter your soil test parameters to receive customized fertilizer and soil conditioning recommendations tuned specifically to your target crop under KAU Package of Practices.")
        crop_label = "Target Crop:"

    selected_crop = st.selectbox(
        crop_label,
        list(CROP_SOIL_STANDARDS.keys()),
        index=list(CROP_SOIL_STANDARDS.keys()).index(st.session_state.get('crop', 'Paddy')) if st.session_state.get('crop', 'Paddy') in CROP_SOIL_STANDARDS else 0,
        key="soil_target_crop"
    )

    crop_data = CROP_SOIL_STANDARDS[selected_crop]
    ideal_ph = crop_data["ideal_ph"]
    ideal_moisture = crop_data["ideal_moisture"]
    ideal_n = crop_data["ideal_n"]
    ideal_p = crop_data["ideal_p"]
    ideal_k = crop_data["ideal_k"]

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📋 " + ("മണ്ണ് പരിശോധനാ വിവരങ്ങൾ നൽകുക" if is_mal else "Enter Soil Test Values"))
        ph = st.number_input("മണ്ണിന്റെ അമ്ലത (pH)" if is_mal else "Soil pH (0 - 14)", min_value=0.0, max_value=14.0, value=5.6, step=0.1)
        moisture = st.slider("മണ്ണിലെ ഈർപ്പം (Moisture %)" if is_mal else "Soil Moisture (%)", 0, 100, 55)
        nitrogen = st.slider("നൈട്രജൻ - N (mg/kg)" if is_mal else "Available Nitrogen - N (mg/kg)", 0, 500, 120)
        phosphorus = st.slider("ഫോസ്ഫറസ് - P (mg/kg)" if is_mal else "Available Phosphorus - P (mg/kg)", 0, 500, 20)
        potassium = st.slider("പൊട്ടാസ്യം - K (mg/kg)" if is_mal else "Available Potassium - K (mg/kg)", 0, 600, 110)

    with col2:
        st.subheader(" " + (f"{selected_crop} വിളയ്ക്കുള്ള അനുയോജ്യ മാനദണ്ഡങ്ങൾ" if is_mal else f"Ideal Benchmarks for {selected_crop}"))
        
        ph_status, ph_color = analyze_nutrient(ph, ideal_ph[0], ideal_ph[1], is_mal)
        m_status, m_color = analyze_nutrient(moisture, ideal_moisture[0], ideal_moisture[1], is_mal)
        n_status, n_color = analyze_nutrient(nitrogen, ideal_n[0], ideal_n[1], is_mal)
        p_status, p_color = analyze_nutrient(phosphorus, ideal_p[0], ideal_p[1], is_mal)
        k_status, k_color = analyze_nutrient(potassium, ideal_k[0], ideal_k[1], is_mal)

        table_md = f"""
| {"ഘടകം (Parameter)" if is_mal else "Parameter"} | {"നിങ്ങളുടെ അളവ് (Your Value)" if is_mal else "Your Value"} | {"അനുയോജ്യ അളവ് (Ideal for " + selected_crop + ")" if is_mal else "Ideal for " + selected_crop} | {"സ്ഥിതി (Status)" if is_mal else "Status"} |
| :--- | :---: | :---: | :---: |
| **pH** | `{ph:.1f}` | `{ideal_ph[0]} - {ideal_ph[1]}` | <span style="color:{ph_color};font-weight:bold;">{ph_status}</span> |
| **Moisture** | `{moisture}%` | `{ideal_moisture[0]}% - {ideal_moisture[1]}%` | <span style="color:{m_color};font-weight:bold;">{m_status}</span> |
| **Nitrogen (N)** | `{nitrogen} mg/kg` | `{ideal_n[0]} - {ideal_n[1]} mg/kg` | <span style="color:{n_color};font-weight:bold;">{n_status}</span> |
| **Phosphorus (P)**| `{phosphorus} mg/kg` | `{ideal_p[0]} - {ideal_p[1]} mg/kg` | <span style="color:{p_color};font-weight:bold;">{p_status}</span> |
| **Potassium (K)** | `{potassium} mg/kg` | `{ideal_k[0]} - {ideal_k[1]} mg/kg` | <span style="color:{k_color};font-weight:bold;">{k_status}</span> |
"""
        st.markdown(table_md, unsafe_allow_html=True)

    # Detailed Recommendations Section
    st.markdown("---")
    st.subheader("🌾 " + (f"{selected_crop} കൃഷിക്കുള്ള ശാസ്ത്രീയ വളപ്രയോഗ ശുപാർശകൾ (KAU PoP)" if is_mal else f"KAU Package of Practices Recommendations for {selected_crop}"))
    
    recs = crop_data["recommendations"]["Malayalam" if is_mal else "English"]
    
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown("#### ⚪ " + ("കുമ്മായം / അമ്ലതാ നിയന്ത്രണം (Liming & pH Correction)" if is_mal else "Liming & pH Correction"))
        if ph < ideal_ph[0]:
            st.error(recs["lime"])
        elif ph > ideal_ph[1]:
            st.warning("മണ്ണിന്റെ pH ഉയർന്നതാണ്. കുമ്മായ പ്രയോഗം ഒഴിവാക്കുക. ജൈവാംശം വർദ്ധിപ്പിക്കാൻ കൂടുതൽ കമ്പോസ്റ്റ് നൽകുക." if is_mal else "Soil pH is slightly high. Avoid liming. Increase organic compost and green manuring.")
        else:
            st.success("മണ്ണിന്റെ അമ്ലത ഈ വിളയ്ക്ക് തികച്ചും അനുയോജ്യമാണ്. അധിക കുമ്മായ പ്രയോഗം ആവശ്യമില്ല." if is_mal else "Soil pH is ideal for this crop. No corrective liming required.")

        st.markdown("#### 🧪 " + ("രാസവളപ്രയോഗ ശുപാർശ (Chemical Fertilizers NPK)" if is_mal else "Chemical Fertilizer Recommendations (NPK)"))
        st.info(recs["fertilizer"])

    with r_col2:
        st.markdown("#### 🌿 " + ("ജൈവവളങ്ങളും പുതയിടലും (Organic Manuring & Soil Health)" if is_mal else "Organic Manuring & Soil Conditioning"))
        st.success(recs["organic"])

        st.markdown("#### 🔬 " + ("സൂക്ഷ്മ മൂലകങ്ങൾ (Micronutrient Management)" if is_mal else "Micronutrient Management"))
        st.warning(recs["micronutrient"])

    st.caption("ശ്രദ്ധിക്കുക: കേരള കാർഷിക സർവകലാശാല (KAU) 2016 പാക്കേജ് ഓഫ് പ്രാക്ടീസസ് അടിസ്ഥാനമാക്കി തയ്യാറാക്കിയത്." if is_mal else "Guidelines derived from Kerala Agricultural University (KAU) Package of Practices.")
