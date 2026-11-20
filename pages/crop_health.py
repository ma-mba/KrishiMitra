import streamlit as st
import json
import os
from pathlib import Path
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms, models
from services.openai_advisory import generate_disease_advisory
from services.translations import t

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "leaf_disease_model.pt"

@st.cache_resource
def load_disease_model():
    if not MODEL_PATH.exists():
        return None, None, None
    try:
        checkpoint = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
        class_names = checkpoint.get('class_names', [])
        model = models.mobilenet_v2(weights=None)
        model.classifier[1] = nn.Linear(model.last_channel, len(class_names))
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        val_acc = checkpoint.get('val_accuracy', None)
        return model, class_names, val_acc
    except Exception as e:
        st.error(f"Error loading leaf disease model: {e}")
        return None, None, None

def predict_leaf_disease(image: Image.Image, model, class_names):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    tensor = transform(image.convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)[0]
        top3_prob, top3_idx = torch.topk(probs, min(3, len(class_names)))
    
    results = []
    for p, idx in zip(top3_prob, top3_idx):
        raw_name = class_names[idx.item()]
        parts = raw_name.split("___")
        crop_name = parts[0].replace("_", " ").strip()
        disease_name = parts[1].replace("_", " ").strip() if len(parts) > 1 else raw_name
        results.append({
            "raw": raw_name,
            "crop": crop_name,
            "disease": disease_name,
            "confidence": p.item()
        })
    return results

def load_crop_health_data():
    data_path = Path(__file__).resolve().parents[1] / "data" / "processed" / "kau_crop_chunks.json"
    if not data_path.exists():
        data_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "kau_crop_chunks.json"
    try:
        with open(data_path, encoding="utf-8") as f:
            docs = json.load(f)
        return docs
    except Exception:
        return []

def main():
    lang = st.session_state.get('language', 'English')
    is_mal = (lang == "മലയാളം")

    if is_mal:
        st.title("🌿 വിള ആരോഗ്യം & ഇലരോഗ നിർണ്ണയം")
        tab_names = ["📸 എഐ ഇലരോഗ സ്കാനർ (AI Leaf Scanner)", "📖 KAU കീട-രോഗ വിവരങ്ങൾ (KAU Advisory)"]
    else:
        st.title("🌿 Crop Health & Leaf Disease Diagnosis")
        tab_names = ["📸 AI Leaf Disease Scanner", "📖 KAU Advisory & Symptom Search"]

    tab1, tab2 = st.tabs(tab_names)

    with tab1:
        if is_mal:
            st.markdown("#### തത്സമയ ഇലരോഗ പരിശോധന")
            st.write("വിളയുടെ ഇലയുടെ വ്യക്തമായ ചിത്രം നൽകി ഡീപ് ലേണിംഗ് മോഡൽ വഴി രോഗനിർണ്ണയം നടത്തുക.")
            uploader_label = "ഇലയുടെ ചിത്രം തിരഞ്ഞെടുക്കുക (JPG, PNG)..."
        else:
            st.markdown("#### Instant Crop Leaf Disease Detection")
            st.write("Upload a clear photo of a crop leaf to detect diseases using the trained Deep Learning Vision model.")
            uploader_label = "Choose a leaf image (JPG, PNG)..."

        model_info = load_disease_model()
        if model_info is None or model_info[0] is None:
            st.warning("⏳ Leaf disease model is not available. Please verify model file.")
            return

        model, class_names, val_acc = model_info
        if val_acc is not None:
            acc_str = f"വിശ്വാസ്യത: {val_acc*100:.2f}%" if is_mal else f"Validation Accuracy: {val_acc*100:.2f}%"
            st.caption(f"🤖 Vision Model: MobileNetV2 ({acc_str})")

        uploaded_file = st.file_uploader(uploader_label, type=["jpg", "jpeg", "png"], key="leaf_file_uploader")
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(img, caption="Uploaded Leaf Image" if not is_mal else "നൽകിയ ഇലയുടെ ചിത്രം", use_container_width=True)

            with col2:
                spinner_msg = "ഇല പരിശോധിക്കുന്നു..." if is_mal else "Analyzing leaf with MobileNetV2..."
                with st.spinner(spinner_msg):
                    preds = predict_leaf_disease(img, model, class_names)

                top_pred = preds[0]
                is_healthy = "healthy" in top_pred["disease"].lower()

                if is_healthy:
                    res_title = f"### ✅ {top_pred['crop']} — ആരോഗ്യമുള്ളത് (Healthy)" if is_mal else f"### ✅ {top_pred['crop']} — Healthy"
                    st.success(res_title)
                else:
                    res_title = f"### ⚠️ രോഗബാധ: {top_pred['crop']} — {top_pred['disease']}" if is_mal else f"### ⚠️ Detected: {top_pred['crop']} — {top_pred['disease']}"
                    st.error(res_title)

                conf_label = "വിശ്വാസ്യത:" if is_mal else "Confidence:"
                st.write(f"**{conf_label}** `{top_pred['confidence']*100:.2f}%`")
                st.progress(float(top_pred['confidence']))

                st.markdown("##### " + ("മറ്റ് സാധ്യതകൾ:" if is_mal else "Top Predictions:"))
                for p in preds:
                    st.write(f"- **{p['crop']} - {p['disease']}**: `{p['confidence']*100:.1f}%`")

            # OpenAI Advisory Section
            st.markdown("---")
            adv_heading = "💡 വിദഗ്ധ കാർഷിക പരിഹാര നിർദ്ദേശങ്ങൾ (AI Advisory)" if is_mal else "💡 Expert Agronomist Treatment Advisory (OpenAI)"
            st.subheader(adv_heading)

            btn_label = "✨ വിദഗ്ധ ചികിത്സാ നിർദ്ദേശങ്ങൾ ലഭ്യമാക്കുക (Generate AI Advisory)" if is_mal else "✨ Generate Detailed Treatment Advisory"
            
            # Auto-generate or button trigger
            if st.button(btn_label, key="gen_advisory_btn", type="primary") or "advisory_result" not in st.session_state:
                with st.spinner("കാർഷിക സർവകലാശാലാ നിർദ്ദേശങ്ങൾ ശേഖരിക്കുന്നു..." if is_mal else "Consulting Agronomist Knowledge Base..."):
                    advisory = generate_disease_advisory(
                        top_pred["crop"],
                        top_pred["disease"],
                        top_pred["confidence"],
                        language=lang
                    )
                    st.session_state["advisory_result"] = advisory

            if "advisory_result" in st.session_state:
                st.markdown(st.session_state["advisory_result"])

    with tab2:
        crop = st.session_state.get('crop', 'Paddy')
        if is_mal:
            st.markdown("#### കാർഷിക സർവകലാശാലാ കീട-രോഗ മാർഗ്ഗരേഖ തിരയുക")
            st.write(f"തിരഞ്ഞെടുത്ത വിള: **{crop}**")
            search_prompt = "കണ്ട ലക്ഷണങ്ങൾ അല്ലെങ്കിൽ കീടത്തിന്റെ പേര് നൽകുക:"
        else:
            st.markdown("#### Search KAU Advisory on Pests & Symptoms")
            st.write(f"Selected Crop: **{crop}**")
            search_prompt = "Describe the observed symptom or pest:"

        symptom = st.text_input(search_prompt, key="pest_symptom_search")
        if symptom:
            docs = load_crop_health_data()
            matches = []
            for doc in docs:
                doc_crop = doc.get('crop', '').lower()
                if crop.lower() not in doc_crop and doc_crop not in crop.lower():
                    continue
                text = doc.get('text', '').lower()
                if symptom.lower() in text:
                    matches.append(doc)

            if not matches:
                warn_msg = "ഈ വിളയ്ക്കുള്ള കീട-രോഗ വിവരങ്ങൾ ലഭ്യമല്ല." if is_mal else "No matching disease or pest information found in the knowledge base."
                st.warning(warn_msg)
            else:
                succ_msg = f"{len(matches)} വിവരങ്ങൾ കണ്ടെത്തി:" if is_mal else f"Found {len(matches)} relevant passages:"
                st.success(succ_msg)
                for i, doc in enumerate(matches[:5], start=1):
                    res_label = f"**വിവരം {i}**" if is_mal else f"**Result {i}**"
                    st.markdown(f"{res_label} (KAU PoP PDF Page: {doc.get('pdf_page')}, ID: {doc.get('chunk_id')})")
                    snippet = doc.get('text', '')[:400]
                    st.write(snippet + ("…" if len(doc.get('text', '')) > 400 else ""))
                    st.divider()
        else:
            hint_msg = "ലക്ഷണങ്ങൾ നൽകൂ (ഉദാഹരണം: 'ഇലപ്പുള്ളി', 'തണ്ടുതുരപ്പൻ', 'കരിമ്പൻ')." if is_mal else "Enter a symptom description above (e.g. 'leaf spot', 'borer', 'wilting')."
            st.info(hint_msg)
