# 🚀 My Advanced Gemini GenAI Web App

A clean, interactive Generative AI chat application built from scratch using Python, the official Google Gemini SDK, and Streamlit. This app allows users to chat with AI, upload images for analysis, adjust creativity levels, and export chat histories locally.

## ✨ Key Features
- **Live AI Chat**: Real-time conversational streams powered by `gemini-3.5-flash`.
- **Multimodal Support**: Upload images (`.jpg`, `.png`) directly into the sidebar to chat about visual content.
- **Creativity Control**: Live temperature slider to alter model response styles from strict/factual to highly creative.
- **Chat Management**: One-click dashboard clearing and instant chat logs export to local `.txt` file archives.
- **Responsive Web UI**: Built purely in Python with an optimized desktop/mobile friendly configuration layout.

## 🛠️ Technical Stack
- **Language**: Python
- **AI SDK**: `google-genai`
- **Frontend Framework**: `streamlit`
- **Image Processing**: `pillow`
- **Hosting**: GitHub & Streamlit Community Cloud

## 🚀 How to Run Locally

1. **Clone or Download** this directory folder onto your local computer.
2. Open your terminal/PowerShell inside the folder and install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Google AI Studio developer token string environment variable:
   ```powershell
   \$env:GEMINI_API_KEY="your_api_key_here"
   ```
4. Run the local Streamlit application framework server:
   ```bash
   streamlit run app.py
   ```

---
👨‍💻 **Developed by Bharat Mor**
