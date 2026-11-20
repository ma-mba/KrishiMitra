"""Crop recommendation page for KrishiMitra. Load only trusted local joblib files."""
import json
from pathlib import Path
import pandas as pd
import streamlit as st
import joblib

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "crop_recommendation_model.joblib"
META_PATH = ROOT / "models" / "crop_recommendation_metadata.json"

@st.cache_resource(show_spinner="Loading crop recommendation model...")
def load_model():
    # joblib uses pickle; never load a model from an untrusted source.
    bundle = joblib.load(MODEL_PATH)
    if not isinstance(bundle, dict) or not all(k in bundle for k in ("model", "label_encoder", "features")):
        raise ValueError("Unexpected model bundle format")
    return bundle

def main():
    is_mal = st.session_state.get("language") == "മലയാളം"
    st.title("🌾 വിള ശുപാർശ | Crop Recommendation" if is_mal else "🌾 Crop Recommendation")
    st.write("Enter soil test and weather values to predict a suitable crop category." if not is_mal else "മണ്ണ് പരിശോധനയും കാലാവസ്ഥാ വിവരങ്ങളും നൽകി അനുയോജ്യമായ വിള കണ്ടെത്തുക.")
    st.caption("Experimental model: predictions are not a substitute for local agronomic advice or soil laboratory recommendations.")
    if not MODEL_PATH.is_file() or not META_PATH.is_file():
        st.error("Model files missing. Put crop_recommendation_model.joblib and crop_recommendation_metadata.json in the models folder.")
        return
    try:
        metadata = json.loads(META_PATH.read_text(encoding="utf-8"))
        bundle = load_model()
    except Exception as exc:
        st.error(f"Unable to load crop model: {exc}")
        return
    expected = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    if bundle["features"] != expected or metadata.get("features") != expected:
        st.error("Model feature order does not match expected input schema.")
        return
    with st.form("crop_recommendation_form"):
        a,b = st.columns(2)
        with a:
            n=st.number_input("Nitrogen (N) — dataset scale",min_value=0.0,max_value=500.0,value=80.0,step=1.0)
            p=st.number_input("Phosphorus (P) — dataset scale",min_value=0.0,max_value=500.0,value=40.0,step=1.0)
            k=st.number_input("Potassium (K) — dataset scale",min_value=0.0,max_value=500.0,value=40.0,step=1.0)
            ph=st.number_input("Soil pH",min_value=0.0,max_value=14.0,value=6.5,step=0.1)
        with b:
            temp=st.number_input("Temperature (°C)",min_value=-20.0,max_value=60.0,value=26.0,step=0.5)
            hum=st.number_input("Humidity (%)",min_value=0.0,max_value=100.0,value=75.0,step=1.0)
            rain=st.number_input("Rainfall (mm) — dataset reference period",min_value=0.0,max_value=1000.0,value=150.0,step=1.0)
        submit=st.form_submit_button("🌱 Recommend Crop",type="primary",use_container_width=True)
    st.caption("Important: N/P/K measurement units and rainfall aggregation period must match the training dataset. Do not directly substitute values from a lab report or daily weather API without checking compatibility.")
    if not submit:
        return
    row=pd.DataFrame([[n,p,k,temp,hum,ph,rain]],columns=expected)
    try:
        model=bundle["model"]
        encoded=model.predict(row)[0]
        label=str(bundle["label_encoder"].inverse_transform([int(encoded)])[0])
        st.success(f"Recommended crop category: **{label.replace('_',' ').title()}**")
        if hasattr(model,"predict_proba"):
            probs=model.predict_proba(row)[0]
            top=sorted(zip(model.classes_,probs),key=lambda x:x[1],reverse=True)[:3]
            st.write("**Top model predictions**")
            for cls,prob in top:
                name=str(bundle["label_encoder"].inverse_transform([int(cls)])[0]).replace('_',' ').title()
                st.write(f"{name}: {prob:.1%} model score")
        st.info("Check local suitability, crop season, water availability, and KAU recommendations before planting. Model scores are not guaranteed real-world success rates.")
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")
