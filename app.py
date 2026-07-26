import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

st.set_page_config(page_title="Bharat's Biology AI", page_icon="🧬", layout="wide") 
st.title("🧬 Bharat Mor's Class 11 & 12 Biology AI Assistant")
st.write("Ask any question related to Class 11th or 12th Biology, or upload a diagram to analyze!")

client = genai.Client()

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("⚙️ AI Settings")

# Slider to control creativity (0.0 = factual/scientific, 1.0 = creative)
creativity = st.sidebar.slider("Explanation Detail (Temperature)", min_value=0.0, max_value=2.0, value=0.7, step=0.1)

# File uploader for diagrams in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload a Biology diagram to discuss:", type=["jpg", "jpeg", "png"])

if uploaded_file: 
    img = Image.open(uploaded_file) 
    st.sidebar.image(img, caption="Uploaded Image", use_container_width=True)

# --- UTILITY FEATURES ---
st.sidebar.write("---") 
st.sidebar.title("🛠️ Chat Management")

LOG_FILE = "biology_chat_history.txt"

# Feature 1: Clear Chat Button
if st.sidebar.button("🧹 Clear Chat History", use_container_width=True): 
    st.session_state.messages = [] 
    st.success("Chat history cleared from screen!") 
    st.rerun()

# Feature 2: Local File Backup Tool
if st.sidebar.button("💾 Export Chat to TXT", use_container_width=True): 
    if "messages" in st.session_state and st.session_state.messages: 
        try: 
            with open(LOG_FILE, "w", encoding="utf-8") as f: 
                for msg in st.session_state.messages: 
                    f.write(f"{msg['role'].upper()}: {msg['content']}\n\n") 
            st.sidebar.success(f"Saved to local folder as {LOG_FILE}!") 
        except Exception as e: 
            st.sidebar.error(f"Failed to save file: {e}") 
    else: 
        st.sidebar.warning("No chat history available to export yet.")

# --- FOOTER CREDITS ---
st.sidebar.write("---") 
st.sidebar.markdown("### 👨‍💻 Developed by:\n**Bharat Mor**")

# --- CHAT INTERFACE ---
if "messages" not in st.session_state: 
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages: 
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

# User chat input box
if user_prompt := st.chat_input("Ask about Photosynthesis, Genetics, Human Anatomy..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Prepare data payload for Gemini
    content_payload = [user_prompt]
    if uploaded_file:
        content_payload.append(img)

    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is analyzing..."):
            try:
                # --- BIOLOGY SYSTEM INSTRUCTION BLOCK ---
                # This locks the model down to strictly Class 11 and 12 Biology topics
                biology_rule = (
                    "You are an expert Class 11 and Class 12 Biology Teacher. "
                    "You must ONLY answer questions related to Class 11th and 12th Biology topics "
                    "(e.g., Plant physiology, Human physiology, Genetics, Evolution, Ecology, Cell Biology). "
                    "If the user asks about ANY other subject (like physics, math, coding, history, or general chat), "
                    "you must politely refuse to answer and say: 'I am specialized only in Class 11 & 12 Biology topics. "
                    "Please ask a biology-related question.'"
                )
                
                # Pass both the temperature and the strict system instruction ruleset
                config = types.GenerateContentConfig(
                    temperature=creativity,
                    system_instruction=biology_rule
                )
                
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=content_payload,
                    config=config,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")
