# 🎙️ Voice-Enabled Disaster Report Summarization System

**Speech → Text → BART/T5 → Multi-Level Summaries**

A production-ready NLP system that transforms voice recordings of disaster reports into actionable multi-level summaries using state-of-the-art transformer models.

## 🌟 Features

- **🎤 Voice Input**: Record or upload audio files (WAV, MP3, M4A, FLAC, OGG)
- **🗣️ Speech Recognition**: Powered by OpenAI Whisper (offline, accurate, free)
- **📝 Multi-Level Summarization**:
  - 🔔 **1-line Alert**: Emergency notification
  - 📰 **Short Public Summary**: Media/public brief
  - 🚨 **Detailed Response Summary**: For emergency response teams
- **🤖 Transformer Models**: BART or T5 for summarization
- **📊 Evaluation**: ROUGE metrics and human evaluation support
- **💻 Web UI**: Beautiful Streamlit interface for easy demo

## 🧱 System Architecture

```
Microphone Input / Audio File
        ↓
Speech Recognition (Whisper ASR)
        ↓
Text Cleaning & Preprocessing
        ↓
T5 / BART Summarization
        ↓
Multi-Level Summaries
        ├── Alert (1-line)
        ├── Short Public Summary
        └── Detailed Response Summary
```

## 🚀 Quick Start

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd BART-T5-Summarization-for-Disaster-Reports
```

2. **Create virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

**Note**: For audio processing, you may need FFmpeg:

- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`

### Running the Application

**Launch Streamlit UI:**

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

### Web Interface (Streamlit)

1. **Upload Audio**: Click "Upload a disaster report audio file" and select your audio file
2. **Or Record**: Use the microphone input to record directly
3. **Process**: Click "🚀 Process Voice → Summaries"
4. **View Results**: See transcribed text and three levels of summaries
5. **Download**: Save all summaries as a text file

### Input/Output Specifications

#### **INPUT:**

- **Audio Files**: WAV, MP3, M4A, FLAC, OGG formats
- **Duration**: 10 seconds to 10 minutes (recommended)
- **Quality**: Clear audio with minimal background noise
- **Text Input** (for summarization only): 100-5000 characters

#### **OUTPUT:**

1. **Transcribed Text** (`str`): Full transcription of the audio
2. **Alert Summary** (`str`): 1-line emergency notification (8-20 words)
3. **Short Public Summary** (`str`): Media/public brief (25-60 words)
4. **Detailed Response Summary** (`str`): Comprehensive summary (60-150 words)

**Example Output:**

```
Transcribed: "A severe earthquake measuring 7.2 on the Richter scale..."

Alert: "7.2 magnitude earthquake hits northern region, 5 fatalities, 50 injured..."

Short: "A 7.2 magnitude earthquake struck the northern region early this morning,
causing significant structural damage. Emergency services deployed, 5 fatalities,
50 injured reported."

Detailed: "A severe earthquake measuring 7.2 on the Richter scale struck the
northern region at 3:45 AM, with epicenter 15 km northeast of city center.
Significant structural damage reported to residential buildings. Emergency services
deployed. At least 50 people injured, 5 confirmed fatalities. Hospitals on high alert."
```

📚 **For detailed documentation, see:**

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete system documentation, API reference, troubleshooting
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)** - Real-world examples with expected outputs

### Command Line Usage

#### Speech-to-Text Only

```python
from src.models.speech_to_text import transcribe_audio

text = transcribe_audio("disaster_report.wav")
print(text)
```

#### Summarization Only

```python
from src.models.summarizer import generate_all_summaries

alert, short, detailed = generate_all_summaries(
    "Long disaster report text here..."
)
```

#### Complete Pipeline

```python
from src.pipeline import voice_to_summary

transcribed, alert, short, detailed = voice_to_summary("disaster_report.wav")
```

## 🏗️ Project Structure

```
BART-T5-Summarization-for-Disaster-Reports/
│
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── src/
│   ├── __init__.py
│   ├── pipeline.py                 # Main pipeline: Voice → Summaries
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── speech_to_text.py       # Whisper ASR module
│   │   └── summarizer.py           # T5/BART summarization module
│   │
│   └── utils/
│       ├── __init__.py
│       └── evaluation.py           # ROUGE metrics & evaluation
│
├── data/                           # Dataset directory
├── tests/                          # Test files
└── venv/                           # Virtual environment (gitignored)
```

## 🔧 Configuration

### Whisper Models

Available model sizes (larger = more accurate, slower):

- `tiny`: Fastest, least accurate
- `base`: **Recommended** - Good balance
- `small`: Better accuracy
- `medium`: High accuracy
- `large`: Best accuracy, slowest

### Summarization Models

**BART (Default)**:

- `facebook/bart-large-cnn`: Best for news/summaries
- `facebook/bart-base`: Faster, smaller

**T5**:

- `t5-base`: Base T5 model
- `t5-large`: Larger T5 model

## 📊 Evaluation

### ROUGE Metrics

```python
from src.utils.evaluation import SummarizationEvaluator

evaluator = SummarizationEvaluator()
metrics = evaluator.compute_rouge(reference_summary, generated_summary)
evaluator.print_metrics(metrics)
```

### Human Evaluation

Rate summaries on:

- **Relevance** (1-5): How relevant is the summary to the original?
- **Conciseness** (1-5): Is it appropriately concise?
- **Fluency** (1-5): Is it grammatically correct and fluent?

## 🧪 Testing

### Test Speech-to-Text

```bash
python src/models/speech_to_text.py sample_audio.wav
```

### Test Summarization

```bash
python src/models/summarizer.py
```

### Test Complete Pipeline

```bash
python src/pipeline.py sample_audio.wav
```

## 🎯 Use Cases

1. **Emergency Response**: Quick understanding of disaster situations
2. **Media Briefings**: Generate public-facing summaries
3. **Internal Reports**: Detailed summaries for response teams
4. **Research**: Academic research on disaster reporting
5. **Training**: Dataset creation and model fine-tuning

## 🔬 Research & Innovation

### Research Title

**Voice-Driven Multi-Granularity Summarization of Disaster Reports using Transformer Models**

### Key Innovations

- ✅ Combining speech input with granular summarization levels
- ✅ Optimizing summaries for different audiences:
  - Public alert notifications
  - Media briefs
  - Response team coordination
- ✅ End-to-end voice-to-summary pipeline
- ✅ Real-world emergency domain application

### Patent System Flow

```
Voice Input
    ↓
ASR (Automatic Speech Recognition)
    ↓
Noise Filtering & Preprocessing
    ↓
Domain NLP Pipeline
    ↓
Multi-tier Transformer Summarization
    ↓
Emergency Outputs (Alert, Short, Detailed)
```

## 📈 Performance Considerations

- **First Run**: Models download automatically (~1-2 GB)
- **Processing Time**:
  - Whisper transcription: ~1-2x audio duration
  - Summarization: ~5-10 seconds per summary
- **Memory**: ~4-8 GB RAM recommended
- **GPU**: Optional but recommended for faster processing

## 🛠️ Development

### Team Roles

- **Lead Dev (NLP + Integration)**: T5/BART summarizer, pipeline integration
- **Research + Training**: Dataset prep, fine-tuning, evaluation metrics
- **Frontend + Data**: Streamlit UI, dataset gathering, annotation support

### 4-Week Timeline

- **Week 1**: Setup, baseline summarizer, data collection
- **Week 2**: Full pipeline integration, Streamlit demo, labeled dataset
- **Week 3**: Fine-tuning, optimization, keyword extraction, evaluation
- **Week 4**: Paper writing, patent diagrams, final polish

## 📝 License

[Specify your license here]

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- HuggingFace Transformers for BART/T5 models
- Streamlit for web interface

## 📧 Contact

[Add contact information]

## 🔮 Future Enhancements

- [ ] Fine-tuning on disaster report datasets
- [ ] Keyword extraction for alerts
- [ ] Multi-language support
- [ ] Real-time streaming transcription
- [ ] Mobile app integration
- [ ] API endpoint for integration
- [ ] Advanced evaluation metrics
- [ ] Model quantization for faster inference

---

**Built for Emergency Response and Disaster Management**
