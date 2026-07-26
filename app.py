import os
import streamlit as st
from google import genai
from PIL import Image
import json

st.set_page_config(page_title="Bharat's Biology AI", page_icon="🧬", layout="wide") 
st.title("🧬 Bharat Mor's Class 11 & 12 Biology AI Assistant")
st.write("Ask any question related to Class 11th or 12th Biology, upload a diagram, or take a targeted MCQ practice quiz!")

# --- BIOLOGY SYSTEM INSTRUCTION BLOCK ---
biology_rule = (
    "You are an expert Class 11 and Class 12 Biology Teacher. "
    "You must ONLY answer questions related to Class 11th and 12th Biology topics "
    "(e.g., Plant physiology, Human physiology, Genetics, Evolution, Ecology, Cell Biology). "
    "If the user asks about ANY other subject (like physics, math, coding, history, or general chat), "
    "you must politely refuse to answer and say: 'I am specialized only in Class 11 & 12 Biology topics. "
    "Please ask a biology-related question.'"
)

# Connect to the Gemini client
client = genai.Client()

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("⚙️ AI Settings")

# Slider to control creativity
creativity = st.sidebar.slider("Explanation Detail (Temperature)", min_value=0.0, max_value=2.0, value=0.7, step=0.1)

# File uploader for diagrams
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
    if "quiz_data" in st.session_state:
        del st.session_state.quiz_data
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

# --- MCQ TEST CENTER FEATURE ---
st.sidebar.write("---")
st.sidebar.title("📝 MCQ Test Center")

# Drop-down menu selection
selected_topic = st.sidebar.selectbox(
    "Choose a topic for your test:",
    [
        "Overall Syllabus (Mixed)",
        "Cell Structure and Function",
        "Plant Physiology",
        "Human Physiology",
        "Genetics and Evolution",
        "Biology in Human Welfare",
        "Biotechnology",
        "Ecology and Environment"
    ]
)

if st.sidebar.button("🎯 Start Selective MCQ Test", use_container_width=True):
    with st.spinner(f"Generating 3 questions on {selected_topic}..."):
        try:
            quiz_prompt = (
                f"Generate exactly 3 multiple choice questions for Class 11 or 12 Biology specifically focusing on the topic: '{selected_topic}'. "
                "Provide the output strictly in a valid JSON format with no markdown wrappers, no backticks, and no extra text. "
                "The JSON must be a list of objects exactly structured like this example: "
                '[{"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Lysosome"], "correct": "Mitochondria"}]'
            )
            
            # Updated to the newer model
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=quiz_prompt,
                config={'temperature': 1.0}
            )
            
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            st.session_state.quiz_data = json.loads(clean_json)
            st.session_state.current_quiz_topic = selected_topic
            st.session_state.quiz_submitted = False
        except Exception as e:
            st.sidebar.error(f"Could not generate quiz: {e}")

# --- FOOTER CREDITS ---
st.sidebar.write("---") 
st.sidebar.markdown("### 👨‍💻 Developed by:\n**Bharat Mor**")


# --- DISPLAY INTERACTIVE QUIZ IF GENERATED ---
if "quiz_data" in st.session_state and st.session_state.quiz_data:
    st.info(f"📝 **Class 11 & 12 Biology Test Topic: {st.session_state.current_quiz_topic}**")
    user_answers = {}
    
    for i, q in enumerate(st.session_state.quiz_data):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        user_answers[i] = st.radio(f"Select option for Q{i+1}:", q['options'], key=f"q_{i}", label_visibility="collapsed")
        st.write("")
        
    if st.button("Submit Quiz Answers"):
        st.session_state.quiz_submitted = True
        
    if st.session_state.get("quiz_submitted", False):
        score = 0
        st.markdown("### 📊 Quiz Results:")
        for i, q in enumerate(st.session_state.quiz_data):
            if user_answers[i] == q['correct']:
                score += 1
                st.success(f"✔️ **Question {i+1}**: Correct! ({q['correct']})")
            else:
                st.error(f"❌ **Question {i+1}**: Incorrect. You chose {user_answers[i]}. Correct Answer: **{q['correct']}**")
        
        st.metric(label="Your Total Score", value=f"{score} / {len(st.session_state.quiz_data)}")
    st.write("---")


# --- CHAT INTERFACE ---
if "messages" not in st.session_state: 
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages: 
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

# User chat input box
if user_prompt := st.chat_input("Ask about Photosynthesis, Genetics, Human Anatomy..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    content_payload = [user_prompt]
    if uploaded_file:
        content_payload.append(img)

    with st.chat_message("assistant"):
        with st.spinner("Gemini is analyzing..."):
            try:
                # Updated to the newer model
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=content_payload,
                    config={
                        'temperature': creativity,
                        'system_instruction': biology_rule
                    }
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")
