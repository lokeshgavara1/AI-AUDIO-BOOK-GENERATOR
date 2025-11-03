🎧 AI Audio Book Generator
Transform text documents into narrated audiobooks using AI-powered rewriting and text-to-speech (TTS).
Built with Python and Streamlit — no paid APIs required for basic use.

🧠 Overview
AI Audio Book Generator is an intelligent web application that allows users to:

Upload .pdf, .docx, or .txt files

Automatically extract text

Rewrite the content into a storytelling, audiobook-style narration using AI

Convert it into natural-sounding audio

Download or preview the generated audiobook instantly

This project demonstrates the integration of Natural Language Processing (NLP) and Speech Synthesis (TTS) to make reading more engaging and accessible.

⚙️ Features
✅ Upload and process PDF, DOCX, or TXT files
✅ AI-powered rewriting for smooth narration
✅ Natural Text-to-Speech audio generation
✅ Streamlit interface for real-time interaction
✅ MP3 file download support
✅ 100% client-friendly — deployable on Streamlit Cloud (Free)

🧩 Tech Stack
Component	Technology Used
Frontend / UI	Streamlit
Backend Logic	Python
AI Text Rewriting	OpenAI GPT API
Text-to-Speech (TTS)	gTTS / OpenAI TTS
File Handling	PyPDF2, python-docx
Deployment	Streamlit Cloud / Localhost

📂 Project Structure
php
Copy code
AI-AudioBook-Generator/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── assets/                # (Optional) logos, icons, sample files
🛠️ Installation & Setup
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-username/ai-audiobook-generator.git
cd ai-audiobook-generator
2. Create a Virtual Environment
bash
Copy code
python -m venv venv
# Activate it
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On macOS/Linux
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Add Your OpenAI API Key
If using Streamlit Cloud, add it to .streamlit/secrets.toml
Otherwise, set it as an environment variable:

bash
Copy code
export OPENAI_API_KEY="your_api_key_here"
5. Run the App
bash
Copy code
streamlit run app.py
Then open the local URL (e.g., http://localhost:8501) in your browser.

🖥️ Usage Guide
Upload your document (PDF, DOCX, or TXT)

Wait while the app:

Extracts text

Rewrites it using AI

Converts it into speech

Listen to your generated audiobook

Click Download to save the MP3 file

🧪 Example Code (Snippet)
python
Copy code
import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
from gtts import gTTS
import openai
import tempfile

st.title("🎧 AI Audio Book Generator")
st.write("Upload your document and get a narrated audiobook instantly!")

uploaded_file = st.file_uploader("Upload File", type=["pdf", "docx", "txt"])

if uploaded_file:
    text = ""
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        text = uploaded_file.read().decode("utf-8")

    st.success("✅ Text extracted successfully!")

    # Rewrite text with AI
    openai.api_key = "YOUR_API_KEY"
    with st.spinner("Rewriting text for narration..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert audiobook narrator."},
                {"role": "user", "content": f"Rewrite this text in storytelling style:\n{text}"}
            ]
        )
        rewritten_text = response["choices"][0]["message"]["content"]

    # Convert to speech
    with st.spinner("Generating audio..."):
        tts = gTTS(rewritten_text)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)

    st.audio(temp_audio.name)
    st.download_button("Download Audiobook", open(temp_audio.name, "rb"), file_name="audiobook.mp3")
🧾 requirements.txt
Here’s what to include in your requirements.txt file for easy deployment:

nginx
Copy code
streamlit
openai
PyPDF2
python-docx
gtts
💡 Future Enhancements
🌍 Support for multiple languages

🗣️ Voice customization (tone, gender, speed)

☁️ Cloud document history and storage

🧩 Chapter-wise audiobook generation

🎙️ Advanced TTS integration (OpenAI / ElevenLabs)

🤝 Contributing
Contributions are welcome!
If you’d like to enhance features, fix bugs, or optimize code:

Fork this repository

Create a new branch (feature/your-feature)

Commit your changes

Submit a pull request

📜 License
This project is licensed under the MIT License.
You are free to use, modify, and distribute it — just give credit.

📬 Contact
👤 Author: [Your Name]
📧 Email: [your.email@example.com]
🔗 LinkedIn: [linkedin.com/in/yourprofile]
💻 GitHub: [github.com/your-username]
