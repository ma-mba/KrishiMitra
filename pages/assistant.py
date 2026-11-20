import streamlit as st
from services.retrieval import search
from services.web_search import search_agricultural_web
from services.assistant_synthesis import generate_combined_answer

def main():
    lang = st.session_state.get('language', 'English')
    is_mal = (lang == "മലയാളം")

    if is_mal:
        st.title("🤖 എഐ കാർഷിക സഹായി (KAU Knowledge + Live Web)")
        st.write("കേരള കാർഷിക സർവകലാശാലാ (KAU) മാനദണ്ഡങ്ങളും തത്സമയ വെബ് വിവരങ്ങളും സമന്വയിപ്പിച്ച് കർഷകർക്കുള്ള സമഗ്ര ഉപദേശം.")
        query_label = "നിങ്ങളുടെ കാർഷിക സംശയം ചോദിക്കുക:"
        placeholder_text = "ഉദാഹരണം: how to fertilize apples / വാഴയില മഞ്ഞളിക്കുന്നത് എന്തുകൊണ്ട്? / നെല്ലിലെ വളപ്രയോഗം"
        spinner_msg = "കാർഷിക സർവകലാശാലാ രേഖകളിലും തത്സമയ വെബിലും തിരയുന്നു..."
    else:
        st.title("🤖Crop-Specific AI Assistant (KAU + Live Web Search)")
        st.write("Combines verified Kerala Agricultural University (KAU) Package of Practices with live agronomic web intelligence to deliver actionable conclusions to farmers.")
        query_label = "Enter your agricultural question:"
        placeholder_text = "e.g. how to fertilize apples / why my banana leaf is yellow / how to manage blast in paddy"
        spinner_msg = "Consulting KAU Knowledge Base & Live Agronomic Web Sources..."

    sidebar_crop = st.session_state.get('crop', 'Paddy')
    
    query = st.text_input(query_label, key="assistant_query", placeholder=placeholder_text)

    if query:
        with st.spinner(spinner_msg):
            # 1. KAU Multilingual ONNX Retrieval (with smart crop entity extraction)
            kau_results, detected_crop = search(query, crop=sidebar_crop, top_k=4)
            
            # 2. Live Agronomic Web Search (targeted directly to the user's detected crop!)
            web_results = search_agricultural_web(query, crop=detected_crop, max_results=3)
            
            # 3. Dynamic Agronomic Synthesis
            combined_advisory = generate_combined_answer(
                query=query,
                kau_results=kau_results,
                web_results=web_results,
                crop=detected_crop,
                language=lang
            )

        # Colorful Badge for detected crop
        badge_crop = detected_crop.upper()
        is_external = kau_results and kau_results[0].get("is_external_crop", False)
        
        if is_mal:
            tag_note = "തത്സമയ കാർഷിക ഗവേഷണ വിവരങ്ങൾ" if is_external else "KAU ഔദ്യോഗിക രേഖകൾ + തത്സമയ വെബ്"
            st.success(f"🌾 **തിരിച്ചറിഞ്ഞ വിള:** `{badge_crop}` | **ഉറവിടം:** {tag_note}")
        else:
            tag_note = "Specialized Agronomic Web & Extension Knowledge" if is_external else "Official KAU PoP + Live Agronomic Web"
            st.success(f"🌾 **Detected Crop Intent:** `{badge_crop}` | **Multi-Source Engine:** {tag_note}")

        # Tabs for user exploration
        if is_mal:
            tab1_title = "💡 എഐ സമഗ്ര നിഗമനം (Farmer Action Plan)"
            tab2_title = "📚 KAU കാർഷിക രേഖകൾ (KAU PoP)"
            tab3_title = "🌐 തത്സമയ വെബ് വിവരങ്ങൾ (Live Web)"
        else:
            tab1_title = "💡 AI Conclusion & Farmer Action Plan"
            tab2_title = "📚 KAU Knowledge Base (Official PoP)"
            tab3_title = "🌐 Live Agronomic Web Sources"

        tab1, tab2, tab3 = st.tabs([tab1_title, tab2_title, tab3_title])

        with tab1:
            st.markdown(combined_advisory)

        with tab2:
            st.markdown("#### " + ("കേരള കാർഷിക സർവകലാശാലാ (KAU) മാനദണ്ഡങ്ങൾ" if is_mal else "Official KAU Package of Practices Excerpts"))
            if is_external:
                st.info(
                    f"ശ്രദ്ധിക്കുക: '{badge_crop}' കേരളത്തിലെ പരമ്പരാഗത സമതല വിളയല്ലാത്തതിനാൽ (ഉദാഹരണത്തിന് ഇടുക്കി ഹൈറേഞ്ചുകളിൽ മാത്രം വളരുന്നവ), സർവകലാശാലാ പൊതു മാനദണ്ഡങ്ങളും അനുബന്ധ കാർഷിക ഗവേഷണങ്ങളുമാണ് താഴെ നൽകിയിരിക്കുന്നത്." if is_mal else
                    f"Note: '{badge_crop}' is a specialized or temperate crop (e.g. grown in Idukki high ranges). Below are related agronomic & soil management excerpts from KAU."
                )
            for res in kau_results:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.markdown(f"**{'വിവരം' if is_mal else 'Result'} #{res['rank']} — {res.get('crop','').upper()}**")
                    with col2:
                        sim_pct = f"{res['similarity']*100:.1f}%"
                        st.caption(f"🎯 {'സാദൃശ്യം' if is_mal else 'Similarity'}: `{sim_pct}` | 📄 KAU PDF Page: `{res.get('pdf_page')}` | Chunk: `{res.get('chunk_id')}`")
                    st.write(res['text'][:650] + ("…" if len(res['text']) > 650 else ""))

        with tab3:
            st.markdown("#### " + ("തത്സമയ കാർഷിക വെബ്ബ് കണ്ടെത്തലുകൾ" if is_mal else "Live Agronomic Web Findings"))
            if web_results:
                for idx, w in enumerate(web_results, 1):
                    with st.container(border=True):
                        st.markdown(f"**{idx}. [{w['title']}]({w['url']})**")
                        st.write(w['snippet'])
                        if w.get('url'):
                            st.caption(f"🔗 [Visit Web Source]({w['url']})")
            else:
                st.info("വെബ്ബ് വിവരങ്ങൾ ലഭ്യമല്ല." if is_mal else "No web results retrieved.")

        st.caption(
            "നിരാകരണം: ഈ ഉപദേശങ്ങൾ കാർഷിക സർവകലാശാലാ നിർദ്ദേശങ്ങളും ശാസ്ത്രീയ വിവരങ്ങളും അടിസ്ഥാനമാക്കിയുള്ളതാണ്. വലിയ തോതിൽ മരുന്ന് തളിക്കുന്നതിന് മുൻപ് പ്രാദേശിക കൃഷിഭവനുമായി ബന്ധപ്പെടുക." if is_mal else
            "Disclaimer: Synthesized recommendations are based on KAU Package of Practices and verified agronomic research. Consult your local Krishi Bhavan before large-scale pesticide applications."
        )
    else:
        st.info("നിങ്ങളുടെ കൃഷി സംശയം മുകളിൽ ടൈപ്പ് ചെയ്യുക." if is_mal else "Type a farming question above to search KAU guidance and live agronomic advice.")
