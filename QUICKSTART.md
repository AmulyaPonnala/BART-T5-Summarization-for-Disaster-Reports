# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**Note**: First-time installation will download models (~1-2 GB), so it may take a few minutes.

## Step 2: Test Text Summarization (No Audio Needed)

```bash
python src/models/summarizer.py
```

This will test the summarization with a sample disaster report text.

## Step 3: Run the Web Interface

```bash
streamlit run app.py
```

The app will open in your browser. You can:

- Upload an audio file
- Record audio directly
- See real-time transcription and summaries

## Step 4: Test with Your Own Audio

```bash
python example_usage.py your_audio_file.wav
```

## Troubleshooting

### FFmpeg Not Found

If you get FFmpeg errors:

- **Windows**: Install from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`

### Out of Memory

- Use smaller Whisper model: `tiny` or `base` instead of `large`
- Use `t5-base` instead of `bart-large-cnn`

### Slow Processing

- First run downloads models (one-time)
- Use GPU if available (automatic)
- Consider smaller models for faster processing

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [example_usage.py](example_usage.py) for code examples
3. Explore the code in `src/` directory
4. Add your own disaster report audio files to `data/`

## Need Help?

- Check the main README.md
- Review example_usage.py for code examples
- Open an issue on GitHub

Happy summarizing! 🎙️
