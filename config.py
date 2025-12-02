"""
Configuration file for Voice Disaster Report Summarization System
Modify these settings to change model behavior
"""

# Whisper Model Configuration
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
WHISPER_LANGUAGE = None  # None for auto-detect, or 'en', 'es', etc.

# Summarization Model Configuration
USE_T5 = False  # Set to True to use T5 instead of BART
SUMMARIZER_MODEL = "facebook/bart-large-cnn"  # BART model
# If USE_T5 is True, use one of these:
# T5_MODEL = "t5-base"  # or "t5-large"

# Summary Length Configuration
ALERT_MAX_LENGTH = 20
ALERT_MIN_LENGTH = 8

SHORT_MAX_LENGTH = 60
SHORT_MIN_LENGTH = 25

DETAILED_MAX_LENGTH = 150
DETAILED_MIN_LENGTH = 60

# Processing Configuration
USE_GPU = True  # Automatically uses GPU if available
MAX_INPUT_LENGTH = 1024  # Maximum tokens for input text

# Streamlit UI Configuration
PAGE_TITLE = "Voice Disaster Report Summarizer"
PAGE_ICON = "🎙️"
LAYOUT = "wide"

# Supported Audio Formats
SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "m4a", "flac", "ogg"]

