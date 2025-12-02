"""
Example Usage Script
Demonstrates how to use the Voice-to-Summary pipeline
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.pipeline import voice_to_summary
from src.models.speech_to_text import transcribe_audio
from src.models.summarizer import generate_all_summaries


def example_text_summarization():
    """Example: Summarize text directly"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Text Summarization")
    print("="*60)
    
    sample_text = """
    A severe earthquake measuring 7.2 on the Richter scale struck the northern region 
    early this morning at 3:45 AM. The epicenter was located 15 kilometers northeast 
    of the city center. Initial reports indicate significant structural damage to 
    residential buildings in the downtown area. Emergency services have been deployed 
    to assess the situation. At least 50 people have been reported injured, with 5 
    confirmed fatalities. Hospitals are on high alert and accepting casualties. 
    Power outages have been reported in several districts. The government has activated 
    the emergency response protocol and is coordinating rescue operations. Search and 
    rescue teams are being dispatched to the most affected areas. Citizens are advised 
    to stay indoors and avoid damaged structures.
    """
    
    alert, short, detailed = generate_all_summaries(sample_text)
    
    print("\n🔔 ALERT (1-line):")
    print(alert)
    print("\n📰 SHORT PUBLIC SUMMARY:")
    print(short)
    print("\n🚨 DETAILED RESPONSE SUMMARY:")
    print(detailed)


def example_speech_to_text(audio_file: str):
    """Example: Transcribe audio to text"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Speech-to-Text")
    print("="*60)
    
    if not Path(audio_file).exists():
        print(f"❌ Audio file not found: {audio_file}")
        print("Please provide a valid audio file path.")
        return
    
    print(f"Transcribing: {audio_file}")
    text = transcribe_audio(audio_file)
    print(f"\n📝 Transcribed Text:\n{text}")


def example_full_pipeline(audio_file: str):
    """Example: Complete voice-to-summary pipeline"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Complete Voice-to-Summary Pipeline")
    print("="*60)
    
    if not Path(audio_file).exists():
        print(f"❌ Audio file not found: {audio_file}")
        print("Please provide a valid audio file path.")
        return
    
    print(f"Processing: {audio_file}")
    print("This may take a few minutes...")
    
    transcribed, alert, short, detailed = voice_to_summary(audio_file)
    
    print("\n📝 TRANSCRIBED TEXT:")
    print("-" * 60)
    print(transcribed)
    
    print("\n🔔 ALERT (1-line):")
    print("-" * 60)
    print(alert)
    
    print("\n📰 SHORT PUBLIC SUMMARY:")
    print("-" * 60)
    print(short)
    
    print("\n🚨 DETAILED RESPONSE SUMMARY:")
    print("-" * 60)
    print(detailed)


if __name__ == "__main__":
    print("🎙️ Voice-Enabled Disaster Report Summarization System")
    print("Example Usage Script\n")
    
    # Example 1: Text summarization (no audio needed)
    example_text_summarization()
    
    # Example 2 & 3: Require audio file
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        
        # Example 2: Just transcription
        example_speech_to_text(audio_file)
        
        # Example 3: Full pipeline
        example_full_pipeline(audio_file)
    else:
        print("\n" + "="*60)
        print("To test with audio, provide an audio file:")
        print("  python example_usage.py <audio_file.wav>")
        print("="*60)

