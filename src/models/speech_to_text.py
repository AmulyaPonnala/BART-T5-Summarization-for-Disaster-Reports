"""
Speech-to-Text Module using OpenAI Whisper
Handles audio transcription for disaster reports
"""

import whisper
import os
import tempfile
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SpeechToText:
    """Wrapper class for Whisper speech recognition"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
                       Default: 'base' for good balance of speed and accuracy
        """
        logger.info(f"Loading Whisper model: {model_size}")
        self.model = whisper.load_model(model_size)
        self.model_size = model_size
        logger.info("Whisper model loaded successfully")
    
    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file (wav, mp3, etc.)
            language: Optional language code (e.g., 'en'). Auto-detected if None
            
        Returns:
            Transcribed text string
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        logger.info(f"Transcribing audio: {audio_path}")
        
        try:
            # Transcribe with optional language specification
            result = self.model.transcribe(
                audio_path,
                language=language,
                task="transcribe"
            )
            
            text = result["text"].strip()
            logger.info(f"Transcription completed. Length: {len(text)} characters")
            
            return text
            
        except FileNotFoundError as e:
            # Check if it's an FFmpeg-related error
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower() or "The system cannot find the file specified" in error_msg:
                logger.error("FFmpeg not found. Whisper requires FFmpeg to process audio files.")
                raise FileNotFoundError(
                    "FFmpeg is not installed or not in PATH. "
                    "Please install FFmpeg:\n"
                    "- Windows: Download from https://ffmpeg.org/download.html or use 'choco install ffmpeg'\n"
                    "- Linux: 'sudo apt-get install ffmpeg'\n"
                    "- macOS: 'brew install ffmpeg'"
                ) from e
            else:
                logger.error(f"File not found: {error_msg}")
                raise
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            # Check if it's an FFmpeg-related error in the exception message
            error_msg = str(e).lower()
            if "ffmpeg" in error_msg or "cannot find the file" in error_msg:
                raise FileNotFoundError(
                    "FFmpeg is not installed or not in PATH. "
                    "Please install FFmpeg:\n"
                    "- Windows: Download from https://ffmpeg.org/download.html or use 'choco install ffmpeg'\n"
                    "- Linux: 'sudo apt-get install ffmpeg'\n"
                    "- macOS: 'brew install ffmpeg'"
                ) from e
            raise
    
    def transcribe_from_bytes(self, audio_bytes: bytes, temp_suffix: str = ".wav") -> str:
        """
        Transcribe audio from bytes (useful for Streamlit file uploads)
        
        Args:
            audio_bytes: Audio file as bytes
            temp_suffix: File extension for temporary file
            
        Returns:
            Transcribed text string
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=temp_suffix) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            text = self.transcribe_audio(tmp_path)
            return text
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


# Convenience function for direct use
def transcribe_audio(audio_path: str, model_size: str = "base", language: Optional[str] = None) -> str:
    """
    Convenience function to transcribe audio file
    
    Args:
        audio_path: Path to audio file
        model_size: Whisper model size
        language: Optional language code
        
    Returns:
        Transcribed text
    """
    stt = SpeechToText(model_size=model_size)
    return stt.transcribe_audio(audio_path, language=language)


if __name__ == "__main__":
    # Test the module
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        print(f"Transcribing: {audio_file}")
        text = transcribe_audio(audio_file)
        print(f"\nTranscribed Text:\n{text}")
    else:
        print("Usage: python speech_to_text.py <audio_file>")

