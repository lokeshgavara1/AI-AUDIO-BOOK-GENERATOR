🎧 AI Audio Book Generator
Transform any text-based document into a professionally narrated audiobook using AI-powered text rewriting and text-to-speech (TTS) synthesis — all in one simple Streamlit web app.

🚀 Overview
The AI Audio Book Generator allows users to upload .pdf, .docx, or .txt files.
It then automatically:

Extracts text from the uploaded file.

Uses an AI model to rewrite the content in a natural storytelling style.

Converts the rewritten text into high-quality speech audio.

Lets users preview or download the audiobook instantly.

This project integrates Natural Language Processing (NLP) and Speech AI to make reading more accessible and engaging — ideal for students, audiobook enthusiasts, and visually impaired users.

🧠 Key Features
📄 Upload multiple file formats: .pdf, .docx, .txt

🪄 AI-powered text rewriting for natural narration

🔊 Text-to-speech (TTS) conversion with realistic voice output

💾 Downloadable .mp3 audiobook files

⚡ Simple, interactive Streamlit interface

🌐 Works locally or deployable on Streamlit Cloud

🧩 Tech Stack
Component	Technology
Frontend / UI	Streamlit
Backend	Python
AI Model	OpenAI GPT (for text rewriting)
Text-to-Speech	gTTS / OpenAI TTS
File Handling	PyPDF2, python-docx
Environment	Streamlit Cloud / Localhost

📂 Project Structure
php
Copy code
AI-AudioBook-Generator/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── assets/                # (Optional) Icons, logos, or test files
⚙️ Installation & Setup
1️⃣ Clone the repository
bash
Copy code
git clone https://github.com/your-username/ai-audiobook-generator.git
cd ai-audiobook-generator
2️⃣ Create a virtual environment
bash
Copy code
python -m venv venv
source venv/bin/activate    # On macOS/Linux
venv\Scripts\activate       # On Windows
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Set your OpenAI API key
Create a file named .streamlit/secrets.toml (for Streamlit Cloud) or set an environment variable:

bash
Copy code
export OPENAI_API_KEY="your_openai_api_key"
5️⃣ Run the app
bash
Copy code
streamlit run app.py
🖥️ Usage Guide
Open the app in your browser (http://localhost:8501)

Upload your document (PDF, DOCX, or TXT)

Wait while the app extracts and rewrites your text

Preview or download your AI-generated audiobook in MP3 format

🧪 Sample Code Snippet
python
Copy code
from gtts import gTTS
from PyPDF2 import PdfReader
import streamlit as st
import openai
import tempfile

st.title("🎧 AI Audio Book Generator")

uploaded_file = st.file_uploader("Upload your file", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Extract text
    text = ""
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text += page.extract_text()
    
    # AI rewrite
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Rewrite the text in a storytelling narration style."},
            {"role": "user", "content": text}
        ]
    )
    rewritten_text = response["choices"][0]["message"]["content"]
    
    # Text-to-speech
    tts = gTTS(rewritten_text)
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)

    st.audio(temp_audio.name)
    st.download_button("Download Audiobook", open(temp_audio.name, "rb"), file_name="audiobook.mp3")
💡 Future Enhancements
🌍 Multi-language support

🗣️ Voice customization (tone, gender, speed)

☁️ Cloud storage for generated files

🧩 Chapter-wise audiobook generation

🎙️ Integration with advanced TTS engines (OpenAI / ElevenLabs)

🤝 Contributing
Contributions are welcome!
Feel free to fork the repo and submit a pull request for new features, bug fixes, or improvements.

📜 License
This project is licensed under the MIT License.
You are free to use, modify, and distribute it with attribution.

📬 Contact
Author: [Your Name]
Email: [your.email@example.com]
LinkedIn: [linkedin.com/in/yourprofile]
GitHub: [github.com/your-username]
