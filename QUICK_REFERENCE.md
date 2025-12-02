# ⚡ Quick Reference Guide

## 🚀 Quick Commands

### Start Web Interface

```bash
python -m streamlit run app.py
```

### Test Summarization (No Audio Needed)

```bash
python src/models/summarizer.py
```

### Test Complete Pipeline

```bash
python example_usage.py your_audio.wav
```

---

## 📥 Input Formats

| Format | Extension | Supported |
| ------ | --------- | --------- |
| WAV    | `.wav`    | ✅ Yes    |
| MP3    | `.mp3`    | ✅ Yes    |
| M4A    | `.m4a`    | ✅ Yes    |
| FLAC   | `.flac`   | ✅ Yes    |
| OGG    | `.ogg`    | ✅ Yes    |

**Requirements:**

- Duration: 10 seconds - 10 minutes
- Quality: Clear audio recommended
- Sample rate: Any (auto-handled)

---

## 📤 Output Format

```python
(transcribed_text, alert, short_summary, detailed_summary)
```

### Output Types

| Output          | Type  | Length       | Use Case               |
| --------------- | ----- | ------------ | ---------------------- |
| **Transcribed** | `str` | Full text    | Complete transcription |
| **Alert**       | `str` | 8-20 words   | SMS/Notifications      |
| **Short**       | `str` | 25-60 words  | Media/Public           |
| **Detailed**    | `str` | 60-150 words | Response Teams         |

---

## 💻 Code Examples

### Minimal Example

```python
from src.pipeline import voice_to_summary

transcribed, alert, short, detailed = voice_to_summary("audio.wav")
print(alert)
```

### With Options

```python
from src.pipeline import voice_to_summary

transcribed, alert, short, detailed = voice_to_summary(
    "audio.wav",
    whisper_model="base",           # tiny, base, small, medium, large
    summarizer_model="facebook/bart-large-cnn",  # or "t5-base"
    use_t5=False,                    # True for T5
    language="en"                     # or None for auto-detect
)
```

### Step-by-Step

```python
from src.models.speech_to_text import transcribe_audio
from src.models.summarizer import generate_all_summaries

# Step 1: Transcribe
text = transcribe_audio("audio.wav")

# Step 2: Summarize
alert, short, detailed = generate_all_summaries(text)
```

---

## ⚙️ Model Options

### Whisper Models

- `tiny` - Fastest, least accurate
- `base` - **Recommended** - Good balance
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Best accuracy, slowest

### Summarization Models

- `facebook/bart-large-cnn` - **Default** - Best for summaries
- `facebook/bart-base` - Faster, smaller
- `t5-base` - Alternative model
- `t5-large` - Larger T5 model

---

## ⏱️ Processing Times

### Base Model (CPU)

- 30 sec audio: ~1-2 minutes
- 1 min audio: ~2-3 minutes
- 2 min audio: ~3-5 minutes

### Base Model (GPU)

- 30 sec audio: ~20-40 seconds
- 1 min audio: ~35-70 seconds
- 2 min audio: ~1-2.5 minutes

---

## 🐛 Common Issues

| Issue                 | Solution                                   |
| --------------------- | ------------------------------------------ |
| `streamlit not found` | Use `python -m streamlit run app.py`       |
| `File not found`      | Check file path, use absolute path         |
| `CUDA out of memory`  | Use smaller models or CPU                  |
| `No text transcribed` | Check audio quality, ensure speech present |
| `FFmpeg not found`    | Install FFmpeg (see README)                |

---

## 📊 Expected Output Example

```
Transcribed: "A severe earthquake measuring 7.2..."

Alert: "7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured..."

Short: "A 7.2 magnitude earthquake struck the northern region early this morning,
causing significant structural damage. Emergency services deployed, 5 fatalities,
50 injured reported."

Detailed: "A severe earthquake measuring 7.2 on the Richter scale struck the
northern region at 3:45 AM, with epicenter 15 km northeast of city center.
Significant structural damage reported. Emergency services deployed. 50 injured,
5 fatalities. Hospitals on high alert."
```

---

## 📚 Documentation Links

- **[README.md](README.md)** - Main documentation
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete system docs
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Detailed examples
- **[QUICKSTART.md](QUICKSTART.md)** - Installation guide

---

## 🔗 Key Files

| File                           | Purpose                    |
| ------------------------------ | -------------------------- |
| `app.py`                       | Streamlit web interface    |
| `src/pipeline.py`              | Main pipeline orchestrator |
| `src/models/speech_to_text.py` | Whisper ASR module         |
| `src/models/summarizer.py`     | BART/T5 summarization      |
| `src/utils/evaluation.py`      | ROUGE metrics              |
| `example_usage.py`             | Usage examples             |

---

**Last Updated:** 2025-01-12
