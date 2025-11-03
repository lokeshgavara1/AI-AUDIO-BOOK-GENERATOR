"""
AI Audio Book Generator - Main Streamlit Application
Turn your documents into narrated audiobooks instantly!
"""

import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Import custom modules
from text_extractor import TextExtractor
from ai_rewriter import AIRewriter
from tts_generator import TTSGenerator
from utils import (
    get_file_extension, format_file_size, estimate_reading_time,
    generate_output_filename, truncate_text, validate_text_length,
    init_session_state, display_progress_bar
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Audio Book Generator",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .step-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_app():
    """Initialize application and session state"""
    init_session_state()
    
    # Additional session state variables
    if 'temp_files' not in st.session_state:
        st.session_state.temp_files = []


def render_header():
    """Render the application header"""
    st.markdown("""
        <div class="main-header">
            <h1>🎧 AI Audio Book Generator</h1>
            <p>Turn your documents into narrated audiobooks instantly!</p>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with settings"""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Get API key from environment (no user input needed)
        openai_api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Show API status
        if openai_api_key:
            st.success("✅ API Key Configured")
        else:
            st.warning("⚠️ No API Key Found")
        
        st.divider()
        
        # TTS Engine Selection
        st.subheader("🎤 Text-to-Speech Engine")
        tts_engine = st.selectbox(
            "Select TTS Engine",
            options=["gTTS (Free)", "OpenAI TTS (Premium)", "pyttsx3 (Offline)"],
            help="Choose your preferred text-to-speech engine"
        )
        
        st.divider()
        
        # Voice Settings
        st.subheader("🗣️ Voice Settings")
        
        if "OpenAI" in tts_engine:
            voice = st.selectbox(
                "Voice",
                options=TTSGenerator.get_available_openai_voices(),
                help="Select OpenAI voice"
            )
            speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
            accent = None
        elif "gTTS" in tts_engine:
            accents = TTSGenerator.get_available_gtts_accents()
            accent_name = st.selectbox("Accent", options=list(accents.keys()))
            accent = accents[accent_name]
            voice = None
            speed_slow = st.checkbox("Slower Speed")
            speed = speed_slow
        else:  # pyttsx3
            voice = st.selectbox("Voice Gender", options=["Female", "Male"])
            speed = st.slider("Speech Rate (WPM)", 100, 250, 150, 10)
            accent = None
        
        st.divider()
        
        # AI Rewriting Settings
        st.subheader("🤖 AI Rewriting")
        enable_rewriting = st.checkbox("Enable AI Rewriting", value=True)
        
        if enable_rewriting:
            narration_style = st.selectbox(
                "Narration Style",
                options=["storytelling", "professional", "casual"],
                help="Choose how the AI should rewrite your text"
            )
            creativity = st.slider(
                "Creativity Level",
                0.0, 1.0, 0.7, 0.1,
                help="Higher values = more creative rewriting"
            )
        else:
            narration_style = None
            creativity = None
        
        st.divider()
        
        # Advanced Settings
        with st.expander("🔧 Advanced Settings"):
            max_chunk_size = st.number_input(
                "Text Chunk Size",
                min_value=1000,
                max_value=10000,
                value=4000,
                help="Maximum characters per processing chunk"
            )
        
        return {
            'openai_api_key': openai_api_key,
            'tts_engine': tts_engine,
            'voice': voice,
            'speed': speed,
            'accent': accent,
            'enable_rewriting': enable_rewriting,
            'narration_style': narration_style,
            'creativity': creativity,
            'max_chunk_size': max_chunk_size
        }


def process_uploaded_file(uploaded_file, settings):
    """Process the uploaded file and generate audiobook"""
    
    # Step 1: Extract Text
    st.markdown("### 📄 Step 1: Extracting Text")
    with st.spinner("Extracting text from document..."):
        try:
            file_type = get_file_extension(uploaded_file.name)
            extracted_text = TextExtractor.extract_text(uploaded_file, file_type)
            
            # Validate text
            is_valid, error_msg = validate_text_length(extracted_text)
            if not is_valid:
                st.error(error_msg)
                return
            
            st.session_state.extracted_text = extracted_text
            
            # Display extraction stats
            reading_time = estimate_reading_time(extracted_text)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Word Count", f"{reading_time['word_count']:,}")
            with col2:
                st.metric("Characters", f"{len(extracted_text):,}")
            with col3:
                st.metric("Est. Reading Time", f"{reading_time['minutes']}m {reading_time['seconds']}s")
            
            st.success("✅ Text extracted successfully!")
            
            # Show preview
            with st.expander("📖 Preview Extracted Text"):
                st.text_area("Extracted Text", truncate_text(extracted_text, 1000), height=200)
        
        except Exception as e:
            st.error(f"❌ Error extracting text: {str(e)}")
            return
    
    # Step 2: AI Rewriting (Optional)
    if settings['enable_rewriting']:
        st.markdown("### 🤖 Step 2: AI Text Rewriting")
        
        if not settings['openai_api_key']:
            st.error("❌ OpenAI API Key required for AI rewriting. Please enter it in the sidebar.")
            return
        
        with st.spinner("Rewriting text for audiobook narration..."):
            try:
                # Initialize AI Rewriter
                rewriter = AIRewriter(settings['openai_api_key'])
                
                # Chunk text if necessary
                chunks = TextExtractor.chunk_text(extracted_text, settings['max_chunk_size'])
                
                if len(chunks) > 1:
                    st.info(f"Processing {len(chunks)} text chunks...")
                    progress_bar = st.progress(0)
                    
                    def update_progress(current, total):
                        progress_bar.progress(current / total)
                    
                    rewritten_text = rewriter.rewrite_chunks(
                        chunks,
                        creativity=settings['creativity'],
                        style=settings['narration_style'],
                        progress_callback=update_progress
                    )
                else:
                    rewritten_text = rewriter.rewrite_text(
                        extracted_text,
                        creativity=settings['creativity'],
                        style=settings['narration_style']
                    )
                
                st.session_state.rewritten_text = rewritten_text
                st.success("✅ Text rewritten successfully!")
                
                # Show preview
                with st.expander("📖 Preview Rewritten Text"):
                    st.text_area("Rewritten Text", truncate_text(rewritten_text, 1000), height=200)
            
            except Exception as e:
                st.error(f"❌ Error rewriting text: {str(e)}")
                return
    else:
        st.markdown("### ⏭️ Step 2: Skipping AI Rewriting")
        st.info("Using original extracted text for audio generation.")
        st.session_state.rewritten_text = st.session_state.extracted_text
    
    # Step 3: Generate Audio
    st.markdown("### 🎵 Step 3: Generating Audio")
    
    # Determine which text to use
    text_for_audio = st.session_state.rewritten_text or st.session_state.extracted_text
    
    with st.spinner("Converting text to speech..."):
        try:
            # Prepare TTS parameters based on engine
            if "OpenAI" in settings['tts_engine']:
                if not settings['openai_api_key']:
                    st.error("❌ OpenAI API Key required for OpenAI TTS. Please enter it in the sidebar.")
                    return
                
                audio_path = TTSGenerator.generate_with_openai(
                    text=text_for_audio,
                    api_key=settings['openai_api_key'],
                    voice=settings['voice'],
                    speed=settings['speed']
                )
            
            elif "gTTS" in settings['tts_engine']:
                audio_path = TTSGenerator.generate_with_gtts(
                    text=text_for_audio,
                    speed=settings['speed'],
                    accent=settings['accent']
                )
            
            else:  # pyttsx3
                audio_path = TTSGenerator.generate_with_pyttsx3(
                    text=text_for_audio,
                    rate=settings['speed'],
                    voice_gender=settings['voice'].lower()
                )
            
            st.session_state.audio_file_path = audio_path
            st.session_state.temp_files.append(audio_path)
            st.success("✅ Audio generated successfully!")
        
        except Exception as e:
            st.error(f"❌ Error generating audio: {str(e)}")
            return
    
    # Step 4: Display Audio Player and Download
    st.markdown("### 🎧 Step 4: Your Audiobook is Ready!")
    
    if st.session_state.audio_file_path and os.path.exists(st.session_state.audio_file_path):
        # Audio Player
        with open(st.session_state.audio_file_path, 'rb') as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
        
        # Download Button
        output_filename = generate_output_filename(uploaded_file.name)
        st.download_button(
            label="📥 Download Audiobook",
            data=audio_bytes,
            file_name=output_filename,
            mime="audio/mp3"
        )
        
        # Stats
        file_size = os.path.getsize(st.session_state.audio_file_path)
        st.info(f"📊 Audio file size: {format_file_size(file_size)}")


def main():
    """Main application function"""
    
    # Initialize
    initialize_app()
    
    # Render UI
    render_header()
    settings = render_sidebar()
    
    # Main content area
    st.markdown("## 📤 Upload Your Document")
    
    uploaded_file = st.file_uploader(
        "Choose a file (PDF, DOCX, or TXT)",
        type=["pdf", "docx", "txt"],
        help="Upload any text-based document to convert into an audiobook"
    )
    
    if uploaded_file:
        # Display file info
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📄 **File Name:** {uploaded_file.name}")
        with col2:
            st.info(f"📦 **File Size:** {format_file_size(uploaded_file.size)}")
        
        st.divider()
        
        # Process button
        if st.button("🚀 Generate Audiobook", type="primary", use_container_width=True):
            process_uploaded_file(uploaded_file, settings)
    
    else:
        # Instructions when no file is uploaded
        st.info("""
            👋 **Welcome!** To get started:
            1. Upload a document (PDF, DOCX, or TXT)
            2. Configure settings in the sidebar (optional)
            3. Click "Generate Audiobook"
            4. Listen and download your audiobook!
        """)
        
        # Feature highlights
        st.markdown("### ✨ Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                **📚 Multiple Formats**
                - PDF documents
                - Word documents (.docx)
                - Plain text files (.txt)
            """)
        
        with col2:
            st.markdown("""
                **🤖 AI Enhancement**
                - Smart text rewriting
                - Natural narration style
                - Multiple voice options
            """)
        
        with col3:
            st.markdown("""
                **🎵 Quality Audio**
                - Multiple TTS engines
                - Customizable voices
                - Adjustable speed
            """)
    
    # Footer
    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 2rem 0;'>
            Made with ❤️ using Streamlit | Powered by OpenAI
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
