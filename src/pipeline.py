"""
Main Pipeline: Voice → Text → Multi-Level Summaries
Connects speech recognition with summarization
"""

import os
import sys
import logging
from typing import Tuple, Optional, Union
from pathlib import Path

# Handle imports for both direct execution and module import
try:
    from src.models.speech_to_text import SpeechToText
    from src.models.summarizer import DisasterSummarizer
except ImportError:
    # Fallback for direct execution from src/ directory
    from models.speech_to_text import SpeechToText
    from models.summarizer import DisasterSummarizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceToSummaryPipeline:
    """End-to-end pipeline from voice input to multi-level summaries"""
    
    def __init__(
        self,
        whisper_model: str = "base",
        summarizer_model: str = "facebook/bart-large-cnn",
        use_t5: bool = False
    ):
        """
        Initialize the complete pipeline
        
        Args:
            whisper_model: Whisper model size (tiny, base, small, medium, large)
            summarizer_model: Summarization model name
            use_t5: Whether to use T5 instead of BART
        """
        logger.info("Initializing Voice-to-Summary Pipeline...")
        
        # Initialize components
        self.stt = SpeechToText(model_size=whisper_model)
        self.summarizer = DisasterSummarizer(
            model_name=summarizer_model,
            use_t5=use_t5
        )
        
        logger.info("Pipeline initialized successfully")
    
    def process_audio_file(
        self,
        audio_path: str,
        language: Optional[str] = None
    ) -> Tuple[str, str, str, str]:
        """
        Process audio file through complete pipeline
        
        Args:
            audio_path: Path to audio file
            language: Optional language code for transcription
            
        Returns:
            Tuple of (transcribed_text, alert, short_summary, detailed_summary)
        """
        logger.info(f"Processing audio file: {audio_path}")
        
        # Step 1: Speech to Text
        logger.info("Step 1: Transcribing audio...")
        transcribed_text = self.stt.transcribe_audio(audio_path, language=language)
        
        if not transcribed_text or len(transcribed_text.strip()) == 0:
            raise ValueError("No text was transcribed from the audio file.")
        
        logger.info(f"Transcription completed: {len(transcribed_text)} characters")
        
        # Step 2: Generate summaries
        logger.info("Step 2: Generating summaries...")
        alert, short, detailed = self.summarizer.generate_all_summaries(transcribed_text)
        
        logger.info("Pipeline processing completed successfully")
        
        return transcribed_text, alert, short, detailed
    
    def process_audio_bytes(
        self,
        audio_bytes: bytes,
        temp_suffix: str = ".wav",
        language: Optional[str] = None
    ) -> Tuple[str, str, str, str]:
        """
        Process audio from bytes (for Streamlit file uploads)
        
        Args:
            audio_bytes: Audio file as bytes
            temp_suffix: File extension for temporary file
            language: Optional language code for transcription
            
        Returns:
            Tuple of (transcribed_text, alert, short_summary, detailed_summary)
        """
        import tempfile
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=temp_suffix) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            return self.process_audio_file(tmp_path, language=language)
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


# Convenience function for direct use
def voice_to_summary(
    audio_file: Union[str, bytes],
    whisper_model: str = "base",
    summarizer_model: str = "facebook/bart-large-cnn",
    use_t5: bool = False,
    language: Optional[str] = None
) -> Tuple[str, str, str, str]:
    """
    Convenience function to process audio file
    
    Args:
        audio_file: Path to audio file or raw audio bytes
        whisper_model: Whisper model size
        summarizer_model: Summarization model name
        use_t5: Whether to use T5
        language: Optional language code
        
    Returns:
        Tuple of (transcribed_text, alert, short_summary, detailed_summary)
    """
    pipeline = VoiceToSummaryPipeline(
        whisper_model=whisper_model,
        summarizer_model=summarizer_model,
        use_t5=use_t5
    )
    
    if isinstance(audio_file, bytes):
        return pipeline.process_audio_bytes(audio_file, language=language)
    else:
        return pipeline.process_audio_file(audio_file, language=language)


if __name__ == "__main__":
    # Test the pipeline
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        print(f"Processing: {audio_file}")
        
        transcribed, alert, short, detailed = voice_to_summary(audio_file)
        
        print("\n" + "="*60)
        print("📝 TRANSCRIBED TEXT:")
        print("="*60)
        print(transcribed)
        
        print("\n" + "="*60)
        print("🔔 ALERT (1-line):")
        print("="*60)
        print(alert)
        
        print("\n" + "="*60)
        print("📰 SHORT PUBLIC SUMMARY:")
        print("="*60)
        print(short)
        
        print("\n" + "="*60)
        print("🚨 DETAILED RESPONSE SUMMARY:")
        print("="*60)
        print(detailed)
    else:
        print("Usage: python pipeline.py <audio_file>")

