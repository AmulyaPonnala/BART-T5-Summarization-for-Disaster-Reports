# Voice-driven disaster report summarization (BART / T5)

Disaster reports are long, and the people who read them need different things. A responder needs the details, a news desk needs a paragraph, and a phone alert needs one line. This project takes a report, typed or spoken, and writes all three at once with a transformer summarization model.

Research title: *Voice-Driven Multi-Granularity Summarization of Disaster Reports using Transformer Models.*

## What it produces

| Level | Length | For |
|---|---|---|
| Alert | 8 to 20 words | A one-line emergency notification |
| Short public summary | 25 to 60 words | Media and public briefings |
| Detailed response summary | 60 to 150 words | Emergency response teams |

Example, from an earthquake report:

```
Alert:    7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured...
Short:    A 7.2 magnitude earthquake struck the northern region early this morning,
          causing significant structural damage. Emergency services deployed,
          5 fatalities, 50 injured reported.
Detailed: A severe earthquake measuring 7.2 on the Richter scale struck the northern
          region at 3:45 AM, with epicenter 15 km northeast of city center ...
```

## How it works

```
Voice note ──► Whisper (speech to text) ──┐
                                          ├─► clean text ─► BART or T5 ─► alert / short / detailed
Typed report ─────────────────────────────┘                                   │
                                                                   structured report (optional)
```

1. `src/models/speech_to_text.py` transcribes audio with OpenAI Whisper (`base` by default; wav, mp3, m4a, flac and ogg are accepted).
2. `src/models/summarizer.py` runs the same text through the summarizer three times with different length limits. BART (`facebook/bart-large-cnn`) is the default. T5 (`t5-base` or `t5-large`) is a config switch.
3. `src/models/structured_report.py` turns the summaries into a structured, abstractive incident report.
4. `src/utils/evaluation.py` scores output against reference summaries with ROUGE. The docs also include a 1 to 5 human rating sheet for relevance, conciseness and fluency.
5. `app.py` is the Streamlit interface for typed reports: paste a report, pick a model, get the three summaries, and download them as a text file.

Length limits, model names, the Whisper size and GPU use all live in `config.py`.

## Run it

```bash
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py         # opens http://localhost:8501
```

The first run downloads the model weights from Hugging Face. The voice path (`src/pipeline.py`) also needs `pip install openai-whisper` and ffmpeg on your PATH.

From Python:

```python
from src.models.summarizer import DisasterSummarizer

summarizer = DisasterSummarizer()                      # BART
# summarizer = DisasterSummarizer(use_t5=True, model_name="t5-base")
alert, short, detailed = summarizer.generate_all_summaries(report_text)
```

Run `python src/models/summarizer.py` for a quick test on a sample report, or `pytest tests/` for the basic test suite.

## Project layout

```
app.py                     Streamlit UI
config.py                  model names, summary lengths, audio formats
example_usage.py           end-to-end usage examples
src/pipeline.py            voice → text → summaries
src/models/                speech_to_text, summarizer, structured_report
src/utils/evaluation.py    ROUGE scoring
tests/                     basic tests
Report of disaster summary.pdf   project report
```

More detail is in [DOCUMENTATION.md](DOCUMENTATION.md), [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) and [QUICKSTART.md](QUICKSTART.md).

## Stack

Python, PyTorch, Hugging Face Transformers, OpenAI Whisper, rouge-score, Streamlit.
