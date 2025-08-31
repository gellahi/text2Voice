import streamlit as st
import os
import wave
import base64
import io
from pathlib import Path
from dotenv import load_dotenv
import tempfile
import PyPDF2
import docx
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Voice Synthesis Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern, aesthetic design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif !important;
        background: linear-gradient(135deg, #e86666 0%, #a04b4b 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .app-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #e86666 0%, #a04b4b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .app-subtitle {
        font-size: 1.25rem;
        color: #896363;
        font-weight: 400;
        margin-bottom: 0;
    }
    
    /* Input sections */
    .input-section {
        background: #f8fafc;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 2px solid #efe3e3;
        transition: all 0.3s ease;
    }
    
    .input-section:hover {
        border-color: #e86666;
        box-shadow: 0 4px 20px rgba(232, 102, 102, 0.1);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e86666 0%, #a04b4b 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(232, 102, 102, 0.3);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #efe3e3;
        border-radius: 12px;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #e86666;
        box-shadow: 0 0 0 3px rgba(232, 102, 102, 0.1);
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border: 2px solid #efe3e3;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
        background: white;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #e86666;
        box-shadow: 0 0 0 3px rgba(232, 102, 102, 0.1);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: white;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #e86666;
        background: #f8fafc;
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Audio player styling */
    .stAudio {
        margin: 1rem 0;
    }
    
    /* Voice selection grid */
    .voice-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .voice-card {
        background: white;
        border: 2px solid #efe3e3;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .voice-card:hover {
        border-color: #e86666;
        box-shadow: 0 4px 20px rgba(232, 102, 102, 0.1);
        transform: translateY(-2px);
    }
    
    .voice-card.selected {
        border-color: #e86666;
        background: linear-gradient(135deg, #e86666 0%, #a04b4b 100%);
        color: white;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2.5rem;
        }
        
        .main-container {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .input-section {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_file(uploaded_file):
    """Extract text from uploaded file based on file type"""
    try:
        if uploaded_file.type == "text/plain":
            return str(uploaded_file.read(), "utf-8")
        
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        else:
            st.error("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
            return None
    
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def save_wave_file(filename, pcm_data, channels=1, rate=24000, sample_width=2):
    """Save PCM data as WAV file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_data)

def generate_tts_audio(text, voice_name, api_key):
    """Generate TTS audio using Google Gemini Flash 2.5"""
    try:
        # Initialize the client
        client = genai.Client(api_key=api_key)
        
        # Generate audio
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice_name,
                        )
                    )
                ),
            )
        )
        
        # Extract audio data
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        return base64.b64decode(audio_data)
    
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

def main():
    # Header
    st.markdown("""
    <div class="main-container">
        <div class="app-header">
            <h1 class="app-title">🎙️ Voice Synthesis Studio</h1>
            <p class="app-subtitle">Transform your text into natural speech with AI-powered voice synthesis</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.95);
            border: 2px solid #e86666;
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            color: #1e293b;
            box-shadow: 0 10px 30px rgba(232, 102, 102, 0.15);
            animation: pulse 2s infinite;
        ">
            🚧 We’re hitting a little tech turbulence right now ✨  
            <br><br>
            Our crew’s on it 24/7, and we’ll be back flying smooth real soon.  
            <br><br>
            <span style="color:#e86666;">💜 Thanks for vibin’ with us in the meantime 🔥</span>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    
    # Voice options with descriptions
    voice_options = {
        "Kore": "Firm and authoritative",
        "Puck": "Upbeat and energetic",
        "Zephyr": "Bright and clear",
        "Charon": "Informative and professional",
        "Fenrir": "Excitable and dynamic",
        "Leda": "Youthful and vibrant",
        "Orus": "Firm and steady",
        "Aoede": "Breezy and light",
        "Callirrhoe": "Easy-going and relaxed",
        "Autonoe": "Bright and engaging",
        "Enceladus": "Breathy and soft",
        "Iapetus": "Clear and precise",
        "Umbriel": "Easy-going and friendly",
        "Algieba": "Smooth and polished",
        "Despina": "Smooth and flowing",
        "Erinome": "Clear and articulate",
        "Algenib": "Gravelly and distinctive",
        "Rasalgethi": "Informative and knowledgeable",
        "Laomedeia": "Upbeat and cheerful",
        "Achernar": "Soft and gentle",
        "Alnilam": "Firm and confident",
        "Schedar": "Even and balanced",
        "Gacrux": "Mature and wise",
        "Pulcherrima": "Forward and direct",
        "Achird": "Friendly and warm",
        "Zubenelgenubi": "Casual and relaxed",
        "Vindemiatrix": "Gentle and soothing",
        "Sadachbia": "Lively and animated",
        "Sadaltager": "Knowledgeable and wise",
        "Sulafat": "Warm and inviting"
    }
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input section
        st.markdown("""
        <div class="input-section">
            <h3 class="section-title">📝 Text Input</h3>
        """, unsafe_allow_html=True)
        
        # Tab selection for input method
        input_method = st.radio(
            "Choose your input method:",
            ["Type or Paste Text", "Upload Document"],
            horizontal=True
        )
        
        text_content = ""
        
        if input_method == "Type or Paste Text":
            text_content = st.text_area(
                "Enter your text here:",
                height=200,
                placeholder="Type or paste your text here. The AI will convert it to natural-sounding speech..."
            )
        
        else:  # Upload Document
            uploaded_file = st.file_uploader(
                "Upload your document",
                type=['txt', 'pdf', 'docx'],
                help="Supported formats: .txt, .pdf, .docx"
            )
            
            if uploaded_file:
                with st.spinner("📄 Extracting text from document..."):
                    text_content = extract_text_from_file(uploaded_file)
                
                if text_content:
                    st.success(f"✅ Successfully extracted {len(text_content.split())} words from {uploaded_file.name}")
                    
                    # Show preview
                    with st.expander("📖 Preview extracted text"):
                        st.write(text_content[:500] + "..." if len(text_content) > 500 else text_content)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Voice selection section
        st.markdown("""
        <div class="input-section">
            <h3 class="section-title">🎵 Voice Selection</h3>
        """, unsafe_allow_html=True)
        
        selected_voice = st.selectbox(
            "Choose a voice:",
            options=list(voice_options.keys()),
            format_func=lambda x: f"{x} - {voice_options[x]}",
            help="Each voice has its own unique personality and tone"
        )
        
        # Voice preview info
        st.info(f"🎭 **{selected_voice}**: {voice_options[selected_voice]}")
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            style_prompt = st.text_input(
                "Style instruction (optional):",
                placeholder="e.g., 'Say cheerfully:', 'Whisper:', 'Speak slowly:'"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Generate button
    if st.button("🎙️ Generate Voice", type="primary"):
        if not text_content.strip():
            st.warning("⚠️ Please enter some text or upload a document first.")
        else:
            # Prepare the final text with style if provided
            final_text = text_content
            if style_prompt.strip():
                final_text = f"{style_prompt.strip()} {text_content}"
            
            # Show generation info
            st.info(f"🎯 Generating audio with **{selected_voice}** voice...")
            
            with st.spinner("🎵 Creating your audio masterpiece..."):
                # Generate audio
                audio_data = generate_tts_audio(final_text, selected_voice, api_key)
                
                if audio_data:
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                        save_wave_file(tmp_file.name, audio_data)
                        
                        # Read the file back for display
                        with open(tmp_file.name, "rb") as audio_file:
                            audio_bytes = audio_file.read()
                    
                    # Success message
                    st.success("✅ Audio generated successfully!")
                    
                    # Display audio player
                    st.audio(audio_bytes, format="audio/wav")
                    
                    # Download button
                    st.download_button(
                        label="💾 Download Audio",
                        data=audio_bytes,
                        file_name=f"tts_output_{selected_voice.lower()}.wav",
                        mime="audio/wav"
                    )
                    
                    # Audio info
                    word_count = len(final_text.split())
                    char_count = len(final_text)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Words", word_count)
                    with col2:
                        st.metric("Characters", char_count)
                    with col3:
                        st.metric("Voice", selected_voice)
                    
                    # Clean up temp file
                    os.unlink(tmp_file.name)
    
    # Footer
    st.markdown("""
    </div>
    
    <div style="text-align: center; padding: 2rem; color: white; font-size: 0.9rem;">
        Powered by <strong>Google Gemini Flash 2.5 TTS</strong> • Built with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
