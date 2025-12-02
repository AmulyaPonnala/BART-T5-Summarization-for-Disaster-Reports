"""
Setup script for Voice-Enabled Disaster Report Summarization System
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="voice-disaster-summarizer",
    version="1.0.0",
    description="Voice-Enabled Disaster Report Summarization System using Whisper and T5/BART",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Team Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/BART-T5-Summarization-for-Disaster-Reports",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "streamlit>=1.28.0",
        "openai-whisper>=20231117",
        "sounddevice>=0.4.6",
        "scipy>=1.10.0",
        "rouge-score>=0.1.2",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "audio": [
            "pydub>=0.25.1",
            "ffmpeg-python>=0.2.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "voice-summarizer=src.pipeline:main",
        ],
    },
)

