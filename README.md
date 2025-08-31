# 🎙️ Voice Synthesis Studio

A modern, aesthetic Streamlit application for converting text to speech using Google's Gemini Flash 2.5 TTS API.

## ✨ Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Text Input**: Direct text input with paste functionality
- **30 Voice Options**: Choose from various voice personalities (Kore, Puck, Zephyr, etc.)
- **Style Control**: Add natural language instructions for tone and style
- **Modern UI**: Beautiful, responsive design with gradient backgrounds
- **Audio Download**: Save generated audio as WAV files
- **Multi-language Support**: Automatic language detection for 24+ languages

## 🚀 Quick Start

### 1. Clone or Download Files
Save all the provided files in a directory:
- `app.py` (main application)
- `requirements.txt`
- `.env` (create from template)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### 4. Setup Environment
Create a `.env` file in your project directory:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎵 Available Voices

The app includes 30 different voice options:

| Voice | Personality | Voice | Personality |
|-------|-------------|-------|-------------|
| Kore | Firm & authoritative | Puck | Upbeat & energetic |
| Zephyr | Bright & clear | Charon | Informative & professional |
| Fenrir | Excitable & dynamic | Leda | Youthful & vibrant |
| Orus | Firm & steady | Aoede | Breezy & light |
| And 22 more... | | | |

## 📋 Supported File Types

- **PDF** (.pdf) - Extracts text from PDF documents
- **Word** (.docx) - Reads Microsoft Word documents  
- **Text** (.txt) - Plain text files

## 🎛️ Style Controls

Add natural language instructions to control speech style:
- `"Say cheerfully:"` - Happy, upbeat tone
- `"Whisper:"` - Quiet, intimate delivery
- `"Speak slowly:"` - Deliberate, measured pace
- `"In a professional tone:"` - Business-appropriate delivery

## 🌍 Language Support

Automatic detection for 24 languages including:
- English (US/India)
- Spanish, French, German
- Japanese, Korean, Chinese
- Arabic, Hindi, Bengali
- And many more...

## 🛠️ Technical Details

- **TTS Model**: Google Gemini 2.5 Flash Preview TTS
- **Audio Format**: 24kHz, 16-bit WAV
- **Context Limit**: 32k tokens
- **Framework**: Streamlit with custom CSS

## 📱 Responsive Design

The app features a modern, mobile-responsive design with:
- Gradient backgrounds
- Glass-morphism effects
- Smooth animations
- Intuitive controls

## 🔧 Troubleshooting

**API Key Issues**: Make sure your `.env` file is in the same directory as `app.py` and contains the correct API key.

**File Upload Problems**: Ensure uploaded files are under 200MB and in supported formats.

**Audio Generation Fails**: Check your internet connection and verify the API key has TTS permissions.

## 📄 License

This project uses Google's Gemini API. Please review Google's terms of service for API usage.