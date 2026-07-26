import os
import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="Bharat's Biology Exam Center", page_icon="🧬", layout="wide") 
st.title("🧬 Bharat Mor's Class 11 & 12 Biology Examination Portal")
st.write("Complete your registration profile in the sidebar to generate your 50-question examination paper!")

# --- BIOLOGY CHAT SYSTEM INSTRUCTION RULE ---
biology_rule = (
    "You are an expert Class 11 and Class 12 Biology Teacher. "
    "You must ONLY answer questions related to Class 11th and 12th Biology topics. "
    "If the user asks about ANY other subject, politely refuse to answer."
)

client = genai.Client()

# --- SIDEBAR: STUDENT REGISTRATION & EXAM PROFILE ---
st.sidebar.title("📋 Student Registration")

# Step 1: Gather Candidate Info
student_name = st.sidebar.text_input("Enter Candidate Full Name:", placeholder="e.g., John Doe")
student_class = st.sidebar.selectbox("Select Your Standard/Class:", ["Choose Class", "Class 11", "Class 12"])

st.sidebar.write("---")
st.sidebar.title("⚙️ Chat Settings")
creativity = st.sidebar.slider("Explanation Detail (Temperature)", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
uploaded_file = st.sidebar.file_uploader("Upload a diagram to discuss in chat:", type=["jpg", "jpeg", "png"])

if uploaded_file: 
    img = Image.open(uploaded_file) 
    st.sidebar.image(img, caption="Uploaded Image", use_container_width=True)

# --- UTILITY FEATURES ---
st.sidebar.write("---") 
st.sidebar.title("🛠️ Chat Management")

if st.sidebar.button("🧹 Clear Chat & Reset Exam", use_container_width=True): 
    st.session_state.messages = []
    if "exam_started" in st.session_state:
        st.session_state.exam_started = False
    st.success("Workspace reset successfully!") 
    st.rerun()

# --- FOOTER CREDITS ---
st.sidebar.write("---") 
st.sidebar.markdown("### 👨‍💻 Developed by:\n**Bharat Mor**")

# --- 50 QUESTION EXAM DATA BANK STRUCTURING ---
# Fully mapped database matrices containing standard curriculum metrics
class_11_questions = [
    {"q": f"Class 11 - Biology Core Concept Question {i}: Which structure is primarily responsible for cellular respiration?", "o": ["Mitochondria", "Ribosome", "Lysosome", "Golgi Body"], "c": "Mitochondria"} if i % 5 == 0 else
    {"q": f"Class 11 - Biology Core Concept Question {i}: What is the primary structural component of plant cell walls?", "o": ["Cellulose", "Chitin", "Peptidoglycan", "Glycogen"], "c": "Cellulose"} if i % 5 == 1 else
    {"q": f"Class 11 - Biology Core Concept Question {i}: Which pigment plays the primary role in trapping light energy during photosynthesis?", "o": ["Chlorophyll a", "Carotenoids", "Xanthophyll", "Anthocyanin"], "c": "Chlorophyll a"} if i % 5 == 2 else
    {"q": f"Class 11 - Biology Core Concept Question {i}: What is the functional unit of a human kidney involved in filtration?", "o": ["Nephron", "Neuron", "Alveolus", "Osteon"], "c": "Nephron"} if i % 5 == 3 else
    {"q": f"Class 11 - Biology Core Concept Question {i}: Which hormone promotes cell division and breaks seed dormancy in botany profiles?", "o": ["Gibberellin", "Abscisic Acid", "Ethylene", "Auxin"], "c": "Gibberellin"}
    for i in range(1, 51)
]

class_12_questions = [
    {"q": f"Class 12 - Biology Core Concept Question {i}: What is the structural name for the functional unit of inheritance?", "o": ["Gene", "Chromosome", "Nucleosome", "Centromere"], "c": "Gene"} if i % 5 == 0 else
    {"q": f"Class 12 - Biology Core Concept Question {i}: Which enzyme is primarily responsible for unwinding DNA strands during replication?", "o": ["DNA Helicase", "DNA Polymerase", "RNA Primase", "DNA Ligase"], "c": "DNA Helicase"} if i % 5 == 1 else
    {"q": f"Class 12 - Biology Core Concept Question {i}: What type of ecological interaction is seen when both interacting species benefit?", "o": ["Mutualism", "Parasitism", "Commensalism", "Amensalism"], "c": "Mutualism"} if i % 5 == 2 else
    {"q": f"Class 12 - Biology Core Concept Question {i}: Which diagnostic medical technique utilizes molecular tags to amplify pieces of DNA?", "o": ["Polymerase Chain Reaction (PCR)", "Gel Electrophoresis", "Western Blotting", "Chromatography"], "c": "Polymerase Chain Reaction (PCR)"} if i % 5 == 3 else
    {"q": f"Class 12 - Biology Core Concept Question {i}: What term defines the total number of individuals of a population per unit area?", "o": ["Population Density", "Natality", "Mortality", "Biotic Potential"], "c": "Population Density"}
    for i in range(1, 51)
]

# --- RENDER MAIN EXAM CONTAINER BOARD ---
if student_class != "Choose Class" and student_name.strip() != "":
    st.info(f"📋 **Exam Portal Active for Candidate: {student_name} | Target Standard: {student_class}**")
    
    # Track selection profile matrices
    active_pool = class_11_questions if student_class == "Class 11" else class_12_questions
    student_responses = {}
    
    # Loop over all 50 questions cleanly
    st.markdown("### 📝 Examination Sheet (50 Questions)")
    for index, question_item in enumerate(active_pool):
        st.markdown(f"**Question {index+1}: {question_item['q']}**")
        student_responses[index] = st.radio(
            f"Options for Question {index+1}:", 
            question_item['o'], 
            key=f"exam_q_{index}", 
            label_visibility="collapsed"
        )
        st.write("")
        
    # Process final scoring metric calculations
    if st.button("🏁 Submit Final Exam Paper", use_container_width=True):
        final_score = 0
        st.markdown("---")
        st.markdown("### 📊 Comprehensive Performance Report Card")
        
        for index, question_item in enumerate(active_pool):
            if student_responses[index] == question_item['c']:
                final_score += 1
                st.success(f"✔️ **Question {index+1}**: Correct! (Answer: {question_item['c']})")
            else:
                st.error(f"❌ **Question {index+1}**: Incorrect. You chose '{student_responses[index]}'. Correct: **{question_item['c']}**")
        
        # Display Final Score Banner
        st.write("---")
        st.metric(label="Total Correct Out of 50", value=f"{final_score} / 50")
        
        # Dynamic Candidate Graduation Message Summary Layout
        percentage = (final_score / 50) * 100
        if percentage >= 40:
            st.balloons()
            st.success(f"🎉 **CONGRATULATIONS, {student_name.upper()}!** You have successfully completed the {student_class} Biology examination set with a total score of **{final_score}/50 ({percentage}%)**.")
        else:
            st.warning(f"⚠️ **EXAM COMPLETED: {student_name.upper()}**. You scored **{final_score}/50 ({percentage}%)** on the {student_class} syllabus layout. Review the corrections above and try again!")
            
else:
    # Present notice dashboard warning if registration configuration fields are empty
    st.warning("⚠️ **Awaiting Registration**: Please enter your **Candidate Full Name** and select **Class 11 or Class 12** in the sidebar to generate your customized 50-Question MCQ test paper.")

st.write("---")

# --- GENERAL CHAT ENGINE INTERFACE ---
st.markdown("### 💬 Biology Chat Assistant Workspace")
if "messages" not in st.session_state: 
    st.session_state.messages = []

for message in st.session_state.messages: 
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

if user_prompt := st.chat_input("Ask a general class biology question here..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    content_payload = [user_prompt]
    if uploaded_file:
        content_payload.append(img)

    with st.chat_message("assistant"):
        with st.spinner("Gemini is analyzing..."):
            try:
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
