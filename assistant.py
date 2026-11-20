import streamlit as st
from services.retrieval import search

def main():
    """AI Crop Assistant page.

    Uses the pre‑computed ONNX embeddings to retrieve relevant document chunks
    for the farmer's question. The results are shown with similarity scores and
    source citations (PDF page and chunk ID). No external LLM is called – the
    answer is the extracted passages.
    """
    st.subheader(" Crop‑specific AI Assistant")

    # The main app (app.py) already defines `crop` via a selectbox earlier in the
    # script. We can safely reference that variable if it exists in the global
    # namespace; otherwise fall back to "rice".
    try:
        crop = globals().get("crop", "rice")
    except Exception:
        crop = "rice"

    query = st.text_input("Enter your agricultural question:", key="assistant_query")
    if query:
        with st.spinner("Searching knowledge base…"):
            results = search(query, crop, top_k=5)
        if not results:
            st.info("No matching documents were found for the selected crop.")
            return
        for res in results:
            st.markdown(f"**Result {res['rank']}**  ")
            st.write(f"Similarity: {res['similarity']:.4f}")
            st.write(f"PDF page: {res.get('pdf_page')}, Chunk ID: {res.get('chunk_id')}")
            st.write(res['text'][:700] + ("…" if len(res['text']) > 700 else ""))
            st.divider()
        st.caption(
            "Source pages refer to the original KAU PDF (2016). "
            "Recommendations may be outdated; always verify with current official guidance."
        )
    else:
        st.info("Type a question above to retrieve relevant information.")
