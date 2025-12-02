"""
Streamlit UI for Voice-Enabled Disaster Report Summarization System
Main demo application
"""

import streamlit as st
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pipeline import VoiceToSummaryPipeline

# Page configuration
st.set_page_config(
    page_title="Voice Disaster Report Summarizer",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .summary-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        color: #000000;
    }
    .alert-box {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .short-box {
        background-color: #d1ecf1;
        border-left-color: #17a2b8;
    }
    .detailed-box {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">🎙️ Voice Disaster Report Summarizer</h1>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem;">
            Transform voice recordings into actionable multi-level summaries for emergency response
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    whisper_model = st.selectbox(
        "Whisper Model Size",
        ["tiny", "base", "small", "medium", "large"],
        index=1,
        help="Larger models are more accurate but slower"
    )
    
    use_t5 = st.checkbox(
        "Use T5 Model (instead of BART)",
        value=False,
        help="T5 is an alternative transformer model"
    )
    
    if use_t5:
        summarizer_model = st.selectbox(
            "T5 Model",
            ["t5-base", "t5-large"],
            index=0
        )
    else:
        summarizer_model = st.selectbox(
            "BART Model",
            ["facebook/bart-large-cnn", "facebook/bart-base"],
            index=0
        )
    
    st.markdown("---")
    st.markdown("### 📊 System Pipeline")
    st.markdown("""
        1. **Microphone Input** → Audio Recording
        2. **Speech Recognition** → Whisper ASR
        3. **Text Cleaning** → Preprocessing
        4. **Summarization** → T5/BART Transformers
        5. **Multi-Level Outputs** → Alert, Short, Detailed
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This system combines:
    - **Speech Processing** (Whisper)
    - **NLP** (Text Processing)
    - **Deep Learning** (Transformers)
    - **Real-world Application** (Disaster Response)
    """)

# Main content area
st.markdown("## 📤 Upload or Record Audio")

# File uploader
uploaded_file = st.file_uploader(
    "Upload a disaster report audio file",
    type=["wav", "mp3", "m4a", "flac", "ogg"],
    help="Supported formats: WAV, MP3, M4A, FLAC, OGG"
)

# Audio recording (if browser supports it)
st.markdown("### 🎤 Or Record Audio")
audio_bytes = st.audio_input("Record a disaster report")

# Process audio
audio_to_process = None
audio_source = None

if uploaded_file is not None:
    audio_to_process = uploaded_file.read()
    audio_source = uploaded_file.name
    st.audio(uploaded_file, format=uploaded_file.type)
    
elif audio_bytes is not None:
    # st.audio_input() returns UploadedFile; read bytes for processing
    audio_to_process = audio_bytes.read()
    audio_source = "recorded_audio.wav"
    # Reset stream position so audio can be played back in the UI
    audio_bytes.seek(0)
    st.audio(audio_bytes, format="audio/wav")

# Process button
if audio_to_process is not None:
    if st.button("🚀 Process Voice → Summaries", type="primary", use_container_width=True):
        with st.spinner("🔄 Processing... This may take a minute..."):
            try:
                # Ensure pipeline matches current configuration; re-initialize if needed
                current_config = {
                    "whisper_model": whisper_model,
                    "summarizer_model": summarizer_model,
                    "use_t5": use_t5,
                }

                if (
                    "pipeline" not in st.session_state
                    or "pipeline_config" not in st.session_state
                    or st.session_state.pipeline is None
                    or st.session_state.pipeline_config != current_config
                ):
                    st.session_state.pipeline = VoiceToSummaryPipeline(**current_config)
                    st.session_state.pipeline_config = current_config

                # Process through pipeline
                transcribed_text, alert, short, detailed = st.session_state.pipeline.process_audio_bytes(
                    audio_to_process,
                    temp_suffix=Path(audio_source).suffix if audio_source else ".wav"
                )
                
                # Display results
                st.markdown("---")
                st.markdown("## 📋 Results")
                
                # Transcribed text
                with st.expander("📝 View Transcribed Text", expanded=False):
                    st.text_area("Transcription", transcribed_text, height=150, disabled=True)
                
                # Alert summary
                st.markdown("### 🔔 Alert (1-line Emergency Notification)")
                st.markdown(f'<div class="summary-box alert-box">{alert}</div>', unsafe_allow_html=True)
                
                # Short summary
                st.markdown("### 📰 Short Public Summary")
                st.markdown(f'<div class="summary-box short-box">{short}</div>', unsafe_allow_html=True)
                
                # Detailed summary
                st.markdown("### 🚨 Detailed Response Summary")
                st.markdown(f'<div class="summary-box detailed-box">{detailed}</div>', unsafe_allow_html=True)
                
                # Download options
                st.markdown("---")
                st.markdown("### 💾 Download Summaries")
                
                summary_text = f"""DISASTER REPORT SUMMARIES
Generated from: {audio_source}

🔔 ALERT (1-line):
{alert}

📰 SHORT PUBLIC SUMMARY:
{short}

🚨 DETAILED RESPONSE SUMMARY:
{detailed}

---
Transcribed Text:
{transcribed_text}
"""
                
                st.download_button(
                    label="📥 Download All Summaries",
                    data=summary_text,
                    file_name="disaster_report_summaries.txt",
                    mime="text/plain"
                )
                
            except FileNotFoundError as e:
                error_msg = str(e)
                if "FFmpeg" in error_msg or "ffmpeg" in error_msg:
                    st.error("❌ FFmpeg Not Found")
                    st.markdown("""
                    **Whisper requires FFmpeg to process audio files.**
                    
                    Please install FFmpeg:
                    - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
                    - **Linux**: `sudo apt-get install ffmpeg`
                    - **macOS**: `brew install ffmpeg`
                    
                    After installing, restart the application.
                    """)
                else:
                    st.error(f"❌ File Not Found: {error_msg}")
            except Exception as e:
                st.error(f"❌ Error processing audio: {str(e)}")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 2rem;">
    <p>Voice-Enabled Disaster Report Summarization System</p>
    <p>Powered by Whisper ASR + T5/BART Transformers</p>
</div>
""", unsafe_allow_html=True)

