import os
import streamlit as st
from google import genai
from PIL import Image

# --- PAGE INITIALIZATION ---
st.set_page_config(page_title="Bharat's Biology Exam Center", page_icon="🧬", layout="wide") 
st.title("🧬 Bharat Mor's Class 11 & 12 Biology Examination Portal")
st.write("Complete your registration profile in the sidebar to generate your 50-question examination paper or practice with our new AI Pop Quiz!")

# --- BIOLOGY CHAT SYSTEM INSTRUCTION RULE ---
biology_rule = (
    "You are an expert Class 11 and Class 12 Biology Teacher. "
    "You must ONLY answer questions related to Class 11th and 12th Biology topics. "
    "If the user asks about ANY other subject, politely refuse to answer."
)

# Initialize GenAI Client
client = genai.Client()

# --- INITIALIZE SESSION STATES ---
if "messages" not in st.session_state: 
    st.session_state.messages = []
if "exam_submitted" not in st.session_state:
    st.session_state.exam_submitted = False
if "ai_quiz_questions" not in st.session_state:
    st.session_state.ai_quiz_questions = None

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
    st.session_state.exam_submitted = False
    st.session_state.ai_quiz_questions = None
    st.success("Workspace reset successfully!") 
    st.rerun()

# --- FOOTER CREDITS ---
st.sidebar.write("---") 
st.sidebar.markdown("### 👨‍💻 Developed by:\n**Bharat Mor**")

# --- 50 QUESTION EXAM DATA BANK STRUCTURING ---
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

# --- CHECK REGISTRATION STATUS UPFRONT ---
if student_class == "Choose Class" or student_name.strip() == "":
    st.warning("⚠️ **Awaiting Registration**: Please enter your **Candidate Full Name** and select **Class 11 or Class 12** in the sidebar to generate your customized 50-Question MCQ test paper.")
    st.stop() # Stops execution here so no weird indent loops happen below

# --- RENDER MAIN EXAM CONTAINER BOARD ---
# This block runs only if registration validation passed above
tab1, tab2 = st.tabs(["📝 Standard 50-Q Exam", "🤖 Dynamic AI Chapter Quiz"])

with tab1:
    st.info(f"📋 **Exam Portal Active for Candidate: {student_name} | Target Standard: {student_class}**")
    active_pool = class_11_questions if student_class == "Class 11" else class_12_questions
    student_responses = {}
    
    st.markdown("### 📝 Examination Sheet (50 Questions)")
    
    with st.form(key="biology_exam_form"):
        for index, question_item in enumerate(active_pool):
            st.markdown(f"**Question {index+1}: {question_item['q']}**")
            student_responses[index] = st.radio(
                f"Options for Question {index+1}:", 
                question_item['o'], 
                index=None,
                key=f"exam_q_{index}", 
                label_visibility="collapsed"
            )
            st.write("")
        
        submit_exam = st.form_submit_button("🏁 Submit Final Exam Paper", use_container_width=True)
        
    if submit_exam or st.session_state.exam_submitted:
        st.session_state.exam_submitted = True
        final_score = 0
        st.markdown("---")
        st.markdown("### 📊 Comprehensive Performance Report Card")
        
        incorrect_topics = []
        for index, question_item in enumerate(active_pool):
            if student_responses[index] is None:
                st.warning(f"⚠️ **Question {index+1}**: Skipped / Unanswered. Correct: **{question_item['c']}**")
                incorrect_topics.append(question_item['q'])
            elif student_responses[index] == question_item['c']:
                final_score += 1
                st.success(f"✔️ **Question {index+1}**: Correct! (Answer: {question_item['c']})")
            else:
                st.error(f"❌ **Question {index+1}**: Incorrect. You chose '{student_responses[index]}'. Correct: **{question_item['c']}**")
                incorrect_topics.append(question_item['q'])
        
        st.write("---")
        st.metric(label="Total Correct Out of 50", value=f"{final_score} / 50")
        
        percentage = (final_score / 50) * 100
        if percentage >= 40:
            st.balloons()
            st.success(f"🎉 **CONGRATULATIONS, {student_name.upper()}!** You completed the exam with **{final_score}/50 ({percentage}%)**.")
        else:
            st.warning(f"⚠️ **EXAM COMPLETED: {student_name.upper()}**. You scored **{final_score}/50 ({percentage}%)**.")
        
        if incorrect_topics:
            st.markdown("#### 💡 Need help with missed questions?")
            if st.button("🤖 Ask Assistant to analyze my weak areas", key="explain_errors_btn"):
                analysis_prompt = f"Hi Teacher, I just took my {student_class} Biology exam and missed several conceptual questions including: {', '.join(incorrect_topics[:3])}. Can you briefly explain the core biological concepts behind these systems?"
                st.session_state.messages.append({"role": "user", "content": analysis_prompt})
                st.info("Added request to the Workspace below! Scroll down to chat.")
                st.rerun()

with tab2:
    st.markdown("### 🧬 AI-Generated Targeted Chapter Quiz")
    st.write("Pick a chapter topic below, and our AI will dynamically curate an analytical practice question.")
    
    chapter_topic = st.text_input("Enter Topic/Chapter Name:", placeholder="e.g., Human Circulatory System, Photosynthesis, Genetics")
    
    if st.button("✨ Generate AI Practice Question", use_container_width=True):
        if chapter_topic.strip():
            with st.spinner("AI is generating your question..."):
                quiz_prompt = f"Generate 1 high-quality conceptual multiple-choice question for {student_class} level on the topic: '{chapter_topic}'. Provide the question, 4 choices options labeled A, B, C, D, and clearly specify the correct answer at the bottom."
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[quiz_prompt],
                        config={'system_instruction': biology_rule}
                    )
                    st.session_state.ai_quiz_questions = response.text
                except Exception as e:
                    st.error(f"Error calling Gemini: {e}")
        else:
            st.warning("Please specify a topic or chapter name.")
            
    if st.session_state.ai_quiz_questions:
        st.info("📖 **AI Question Card:**")
        st.markdown(st.session_state.ai_quiz_questions)

st.write("---")

# --- GENERAL CHAT ENGINE INTERFACE ---
