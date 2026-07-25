import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

st.set_page_config(page_title="Advanced Gemini App", page_icon="🚀", layout="wide")
st.title("🚀 My Advanced GenAI Web App")

client = genai.Client()

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("⚙️ AI Settings")

# Slider to control creativity (0.0 = factual, 1.0 = creative)
creativity = st.sidebar.slider("Creativity (Temperature)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

# File uploader for images in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload an image to discuss:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.sidebar.image(img, caption="Uploaded Image", use_container_width=True)

# --- NEW UTILITY FEATURES ---
st.sidebar.write("---")
st.sidebar.title("🛠️ Chat Management")

# Initialize chat log file name
LOG_FILE = "gemini_chat_history.txt"

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
            st.sidebar.success(f"Saved to local folder as `{LOG_FILE}`!")
        except Exception as e:
            st.sidebar.error(f"Failed to save file: {e}")
    else:
        st.sidebar.warning("No chat history available to export yet.")


# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User chat input box
if user_prompt := st.chat_input("Ask something or discuss the uploaded image..."):
    
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
                # Use types.GenerateContentConfig to pass generation settings smoothly
                config = types.GenerateContentConfig(temperature=creativity)
                
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=content_payload,
                    config=config,
                )
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")
# --- FOOTER CREDITS ---
st.sidebar.write("---")
st.sidebar.markdown("### 👨‍💻 Developed by:\n**Bharat Mor**")
