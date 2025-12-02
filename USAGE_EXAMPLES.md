# 📝 Usage Examples & Expected Outputs

This document provides real-world examples of how to use the system and what outputs to expect.

---

## Example 1: Complete Pipeline via Web Interface

### Step-by-Step Process

1. **Start the application:**

   ```bash
   python -m streamlit run app.py
   ```

2. **Upload audio file:**

   - Click "Upload a disaster report audio file"
   - Select `disaster_report.wav` (2 minutes, clear audio)

3. **Process:**
   - Click "🚀 Process Voice → Summaries"
   - Wait for processing (approximately 2-3 minutes)

### Expected Output in UI

```
┌─────────────────────────────────────────────────────────────┐
│  📝 TRANSCRIBED TEXT                                         │
├─────────────────────────────────────────────────────────────┤
│  A severe earthquake measuring 7.2 on the Richter scale    │
│  struck the northern region early this morning at 3:45 AM.  │
│  The epicenter was located 15 kilometers northeast of the   │
│  city center. Initial reports indicate significant          │
│  structural damage to residential buildings in the          │
│  downtown area. Emergency services have been deployed to     │
│  assess the situation. At least 50 people have been          │
│  reported injured, with 5 confirmed fatalities. Hospitals  │
│  are on high alert and accepting casualties. Power outages  │
│  have been reported in several districts.                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  🔔 ALERT (1-line Emergency Notification)                   │
├─────────────────────────────────────────────────────────────┤
│  7.2 magnitude earthquake hits northern region, 5           │
│  fatalities, 50 injured, major structural damage reported. │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  📰 SHORT PUBLIC SUMMARY                                     │
├─────────────────────────────────────────────────────────────┤
│  A 7.2 magnitude earthquake struck the northern region      │
│  early this morning, causing significant structural damage   │
│  to residential buildings. Emergency services have been      │
│  deployed, with 5 confirmed fatalities and 50 people        │
│  reported injured. Hospitals are on high alert and          │
│  accepting casualties.                                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  🚨 DETAILED RESPONSE SUMMARY                                │
├─────────────────────────────────────────────────────────────┤
│  A severe earthquake measuring 7.2 on the Richter scale      │
│  struck the northern region at 3:45 AM, with the epicenter   │
│  located 15 kilometers northeast of the city center.         │
│  Significant structural damage has been reported to          │
│  residential buildings in the downtown area. Emergency       │
│  services have been deployed to assess the situation, with   │
│  at least 50 people reported injured and 5 confirmed        │
│  fatalities. Hospitals are on high alert and accepting        │
│  casualties. Power outages have been reported in several     │
│  districts. The government has activated the emergency       │
│  response protocol and is coordinating rescue operations.   │
└─────────────────────────────────────────────────────────────┘
```

---

## Example 2: Python Script - Complete Pipeline

### Input Code

```python
from src.pipeline import voice_to_summary

# Process audio file
transcribed, alert, short, detailed = voice_to_summary(
    "data/disaster_report.wav",
    whisper_model="base",
    summarizer_model="facebook/bart-large-cnn"
)

# Display results
print("=" * 60)
print("TRANSCRIBED TEXT:")
print("=" * 60)
print(transcribed)
print()

print("=" * 60)
print("ALERT SUMMARY:")
print("=" * 60)
print(alert)
print()

print("=" * 60)
print("SHORT SUMMARY:")
print("=" * 60)
print(short)
print()

print("=" * 60)
print("DETAILED SUMMARY:")
print("=" * 60)
print(detailed)
```

### Expected Console Output

```
Loading Whisper model: base
Whisper model loaded successfully
Transcribing audio: data/disaster_report.wav
Transcription completed. Length: 245 characters
Loading BART model: facebook/bart-large-cnn
Using device: CUDA
Summarization model loaded successfully
Generating multi-level summaries...
All summaries generated successfully

============================================================
TRANSCRIBED TEXT:
============================================================
A severe earthquake measuring 7.2 on the Richter scale struck the northern region
early this morning at 3:45 AM. The epicenter was located 15 kilometers northeast
of the city center. Initial reports indicate significant structural damage to
residential buildings in the downtown area. Emergency services have been deployed
to assess the situation. At least 50 people have been reported injured, with 5
confirmed fatalities. Hospitals are on high alert and accepting casualties. Power
outages have been reported in several districts. The government has activated the
emergency response protocol and is coordinating rescue operations.

============================================================
ALERT SUMMARY:
============================================================
7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured, major
structural damage reported.

============================================================
SHORT SUMMARY:
============================================================
A 7.2 magnitude earthquake struck the northern region early this morning, causing
significant structural damage to residential buildings. Emergency services have
been deployed, with 5 confirmed fatalities and 50 people reported injured.
Hospitals are on high alert and accepting casualties.

============================================================
DETAILED SUMMARY:
============================================================
A severe earthquake measuring 7.2 on the Richter scale struck the northern region
at 3:45 AM, with the epicenter located 15 kilometers northeast of the city center.
Significant structural damage has been reported to residential buildings in the
downtown area. Emergency services have been deployed to assess the situation, with
at least 50 people reported injured and 5 confirmed fatalities. Hospitals are on
high alert and accepting casualties. Power outages have been reported in several
districts. The government has activated the emergency response protocol and is
coordinating rescue operations.
```

---

## Example 3: Step-by-Step Processing

### Input Code

```python
from src.models.speech_to_text import transcribe_audio
from src.models.summarizer import generate_all_summaries

# Step 1: Transcribe audio
print("Step 1: Transcribing audio...")
text = transcribe_audio("disaster_report.wav", model_size="base")
print(f"✓ Transcription complete: {len(text)} characters\n")

# Step 2: Generate summaries
print("Step 2: Generating summaries...")
alert, short, detailed = generate_all_summaries(text)
print("✓ All summaries generated\n")

# Step 3: Display results
print("RESULTS:")
print("-" * 60)
print(f"Alert ({len(alert.split())} words): {alert}")
print(f"Short ({len(short.split())} words): {short}")
print(f"Detailed ({len(detailed.split())} words): {detailed}")
```

### Expected Output

```
Step 1: Transcribing audio...
Loading Whisper model: base
Whisper model loaded successfully
Transcribing audio: disaster_report.wav
Transcription completed. Length: 245 characters
✓ Transcription complete: 245 characters

Step 2: Generating summaries...
Loading BART model: facebook/bart-large-cnn
Using device: CUDA
Summarization model loaded successfully
Generating multi-level summaries...
All summaries generated successfully
✓ All summaries generated

RESULTS:
------------------------------------------------------------
Alert (15 words): 7.2 magnitude earthquake hits northern region, 5 fatalities,
50 injured, major structural damage reported.
Short (38 words): A 7.2 magnitude earthquake struck the northern region early this
morning, causing significant structural damage to residential buildings. Emergency
services have been deployed, with 5 confirmed fatalities and 50 people reported injured.
Detailed (89 words): A severe earthquake measuring 7.2 on the Richter scale struck
the northern region at 3:45 AM, with the epicenter located 15 kilometers northeast
of the city center. Significant structural damage has been reported to residential
buildings in the downtown area. Emergency services have been deployed to assess the
situation, with at least 50 people reported injured and 5 confirmed fatalities.
```

---

## Example 4: Using T5 Model Instead of BART

### Input Code

```python
from src.pipeline import voice_to_summary

# Use T5 model
transcribed, alert, short, detailed = voice_to_summary(
    "disaster_report.wav",
    whisper_model="base",
    summarizer_model="t5-base",
    use_t5=True
)

print("Alert:", alert)
print("Short:", short)
print("Detailed:", detailed)
```

### Expected Output

```
Loading Whisper model: base
Whisper model loaded successfully
Transcribing audio: disaster_report.wav
Transcription completed. Length: 245 characters
Loading T5 model: t5-base
Using device: CUDA
Summarization model loaded successfully
Generating multi-level summaries...
All summaries generated successfully

Alert: 7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured
Short: A 7.2 magnitude earthquake struck the northern region early this morning,
causing significant structural damage. Emergency services deployed, 5 fatalities,
50 injured reported.
Detailed: A severe earthquake measuring 7.2 on the Richter scale struck the
northern region at 3:45 AM. The epicenter was located 15 kilometers northeast of
the city center. Significant structural damage reported to residential buildings.
Emergency services deployed. At least 50 people injured, 5 confirmed fatalities.
Hospitals on high alert.
```

---

## Example 5: Text-Only Summarization (No Audio)

### Input Code

```python
from src.models.summarizer import generate_all_summaries

# Sample disaster report text
text = """
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

alert, short, detailed = generate_all_summaries(text)

print("🔔 Alert:", alert)
print("\n📰 Short:", short)
print("\n🚨 Detailed:", detailed)
```

### Expected Output

```
Loading BART model: facebook/bart-large-cnn
Using device: CUDA
Summarization model loaded successfully
Generating multi-level summaries...
All summaries generated successfully

🔔 Alert: 7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured,
major structural damage reported.

📰 Short: A 7.2 magnitude earthquake struck the northern region early this morning,
causing significant structural damage to residential buildings. Emergency services
have been deployed, with 5 confirmed fatalities and 50 people reported injured.
Hospitals are on high alert and accepting casualties.

🚨 Detailed: A severe earthquake measuring 7.2 on the Richter scale struck the
northern region at 3:45 AM, with the epicenter located 15 kilometers northeast of
the city center. Significant structural damage has been reported to residential
buildings in the downtown area. Emergency services have been deployed to assess the
situation, with at least 50 people reported injured and 5 confirmed fatalities.
Hospitals are on high alert and accepting casualties. Power outages have been
reported in several districts. The government has activated the emergency response
protocol and is coordinating rescue operations.
```

---

## Example 6: Error Handling

### Input Code

```python
from src.pipeline import voice_to_summary

try:
    transcribed, alert, short, detailed = voice_to_summary("nonexistent_file.wav")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please check that the audio file exists and the path is correct.")
except ValueError as e:
    print(f"Error: {e}")
    print("The audio file may be too short or corrupted.")
except Exception as e:
    print(f"Unexpected error: {e}")
    print("Please check your setup and try again.")
```

### Expected Output (Error Case)

```
Loading Whisper model: base
Whisper model loaded successfully
Transcribing audio: nonexistent_file.wav
Error: Audio file not found: nonexistent_file.wav
Please check that the audio file exists and the path is correct.
```

---

## Example 7: Evaluation Metrics

### Input Code

```python
from src.utils.evaluation import SummarizationEvaluator

evaluator = SummarizationEvaluator()

# Reference summary (ground truth)
reference = "7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured, major damage."

# Generated summary
candidate = "7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured, major structural damage reported."

# Compute metrics
metrics = evaluator.compute_rouge(reference, candidate)
evaluator.print_metrics(metrics, "Alert Summary Evaluation")
```

### Expected Output

```
============================================================
Alert Summary Evaluation
============================================================
ROUGE-1 F1:  0.8571 (P: 0.8571, R: 0.8571)
ROUGE-2 F1:  0.7500 (P: 0.7500, R: 0.7500)
ROUGE-L F1:  0.8571 (P: 0.8571, R: 0.8571)
============================================================
```

---

## Example 8: Batch Processing Multiple Files

### Input Code

```python
from src.pipeline import voice_to_summary
import os

# List of audio files
audio_files = [
    "data/report1.wav",
    "data/report2.wav",
    "data/report3.wav"
]

results = []

for audio_file in audio_files:
    if os.path.exists(audio_file):
        print(f"Processing {audio_file}...")
        transcribed, alert, short, detailed = voice_to_summary(audio_file)
        results.append({
            "file": audio_file,
            "alert": alert,
            "short": short,
            "detailed": detailed
        })
        print(f"✓ Completed {audio_file}\n")

# Display all results
for result in results:
    print(f"File: {result['file']}")
    print(f"Alert: {result['alert']}\n")
```

### Expected Output

```
Processing data/report1.wav...
Loading Whisper model: base
Whisper model loaded successfully
Transcribing audio: data/report1.wav
Transcription completed. Length: 245 characters
Loading BART model: facebook/bart-large-cnn
Using device: CUDA
Summarization model loaded successfully
Generating multi-level summaries...
All summaries generated successfully
✓ Completed data/report1.wav

Processing data/report2.wav...
Transcribing audio: data/report2.wav
Transcription completed. Length: 312 characters
Generating multi-level summaries...
All summaries generated successfully
✓ Completed data/report2.wav

File: data/report1.wav
Alert: 7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured, major structural damage reported.

File: data/report2.wav
Alert: Flooding reported in coastal areas, evacuation orders issued for low-lying regions.
```

---

## Output Format Summary

### Data Types

All outputs are Python strings (`str`):

```python
transcribed_text: str      # Full transcription
alert: str                 # 1-line alert
short_summary: str         # Short public summary
detailed_summary: str      # Detailed response summary
```

### Word Count Ranges

- **Alert**: 8-20 words (typically 12-15)
- **Short**: 25-60 words (typically 35-45)
- **Detailed**: 60-150 words (typically 80-120)

### Character Count Ranges

- **Alert**: 50-150 characters
- **Short**: 150-400 characters
- **Detailed**: 400-1000 characters

---

## Performance Expectations

### Processing Times (Base Model, CPU)

| Audio Duration | Transcription | Summarization | Total Time |
| -------------- | ------------- | ------------- | ---------- |
| 30 seconds     | 30-60 sec     | 15-30 sec     | 1-2 min    |
| 1 minute       | 1-2 min       | 15-30 sec     | 2-3 min    |
| 2 minutes      | 2-4 min       | 15-30 sec     | 3-5 min    |
| 5 minutes      | 5-10 min      | 15-30 sec     | 6-11 min   |

### Processing Times (Base Model, GPU)

| Audio Duration | Transcription | Summarization | Total Time |
| -------------- | ------------- | ------------- | ---------- |
| 30 seconds     | 15-30 sec     | 5-10 sec      | 20-40 sec  |
| 1 minute       | 30-60 sec     | 5-10 sec      | 35-70 sec  |
| 2 minutes      | 1-2 min       | 5-10 sec      | 1-2.5 min  |
| 5 minutes      | 2.5-5 min     | 5-10 sec      | 3-6 min    |

---

**Note**: Actual processing times may vary based on hardware, model size, and audio quality.
