# services/chatbot.py
"""Chatbot service that uses a hosted LLM if an API key is provided.
   Falls back to a retrieval‑only answer (existing `services.retrieval`).
   The LLM key is read from the .env variable ``LLM_API_KEY``.
   Currently supports OpenAI compatible APIs (ChatCompletion endpoint).
"""
import os
import json
import streamlit as st
import requests
from services.retrieval import retrieve_answer  # existing retrieval function

# Load API key once
LLM_API_KEY = os.getenv("LLM_API_KEY")
# You can override the endpoint via env var if needed
LLM_ENDPOINT = os.getenv("LLM_ENDPOINT", "https://api.openai.com/v1/chat/completions")

def _call_llm(messages):
    """Call the LLM with a list of message dicts.
       Returns the generated text or raises.
    """
    if not LLM_API_KEY:
        raise RuntimeError("LLM_API_KEY not set")
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",  # generic; you can change via env if needed
        "messages": messages,
        "temperature": 0.2,
    }
    resp = requests.post(LLM_ENDPOINT, headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # OpenAI returns a list under "choices"
    return data["choices"][0]["message"]["content"].strip()

def answer_question(user_question: str, context_chunks: list) -> str:
    """Combine retrieved evidence with LLM generation.
       `context_chunks` is a list of strings (knowledge base excerpts).
       Returns a ready‑to‑display answer.
    """
    # Build the system prompt – include citation instruction
    system_prompt = (
        "You are an agricultural assistant. Answer the farmer's question using the provided "
        "knowledge base excerpts. Cite the source after each fact in the form [source]. "
        "If you are not sure, say so. Keep the answer concise (max 3 sentences)."
    )
    # Build messages for the LLM
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]
    if context_chunks:
        # Append the retrieved chunks as a single "assistant"‑style message
        chunks_text = "\n\n".join(context_chunks)
        messages.append({"role": "assistant", "content": f"Relevant excerpts:\n{chunks_text}"})
    try:
        answer = _call_llm(messages)
        return answer
    except Exception as e:
        # If the LLM call fails (network blocked, key missing, etc.) fall back
        st.warning(f"LLM call failed ({e}), falling back to extractive answer.")
        # Simple extractive fallback – just echo first chunk
        if context_chunks:
            return f"Based on the documents: {context_chunks[0]}"
        return "I could not find any relevant information."

# Helper for the Streamlit page
def chat(user_input: str) -> str:
    """Retrieve evidence then generate answer via LLM (or fallback)."""
    # Retrieve relevant chunks (existing retrieval function expects a query string)
    chunks = retrieve_answer(user_input)
    # `chunks` is expected to be a list of strings – adapt if your retrieval returns dicts
    if isinstance(chunks, dict) and "chunks" in chunks:
        chunks = chunks["chunks"]
    return answer_question(user_input, chunks)
