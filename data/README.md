# Data Directory

This directory is for storing disaster report datasets and audio files.

## Directory Structure

```
data/
├── raw/              # Raw audio files and transcripts
├── processed/        # Processed/cleaned data
├── annotations/      # Human annotations and evaluations
└── samples/          # Sample audio files for testing
```

## Dataset Collection Guidelines

1. **Audio Formats**: WAV, MP3, M4A, FLAC, OGG
2. **Duration**: 30 seconds to 5 minutes recommended
3. **Quality**: Clear audio, minimal background noise
4. **Content**: Disaster reports, emergency situations, crisis updates

## Annotation Format

For human evaluation, use the following structure:

```json
{
  "audio_file": "disaster_report_001.wav",
  "transcript": "Full transcribed text...",
  "reference_summaries": {
    "alert": "1-line alert summary",
    "short": "Short public summary",
    "detailed": "Detailed response summary"
  },
  "human_ratings": {
    "alert": {
      "relevance": 5,
      "conciseness": 5,
      "fluency": 5
    },
    "short": {...},
    "detailed": {...}
  }
}
```

## Privacy & Ethics

- Ensure all audio data is properly anonymized
- Obtain necessary permissions for data collection
- Follow data protection regulations (GDPR, etc.)

