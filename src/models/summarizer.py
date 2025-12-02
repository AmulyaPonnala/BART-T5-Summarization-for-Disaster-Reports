"""
Text Summarization Module using T5 and BART Transformers
Generates multi-level summaries for disaster reports
"""

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from typing import Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DisasterSummarizer:
    """Multi-level summarization for disaster reports using T5/BART"""
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn", use_t5: bool = False):
        """
        Initialize summarization model
        
        Args:
            model_name: HuggingFace model name
                       - "facebook/bart-large-cnn" (default, best for news/summaries)
                       - "t5-base" or "t5-large" for T5 models
            use_t5: If True, use T5 model instead of BART
        """
        if use_t5:
            model_name = "t5-base" if "t5" not in model_name.lower() else model_name
            logger.info(f"Loading T5 model: {model_name}")
        else:
            logger.info(f"Loading BART model: {model_name}")
        
        self.device = 0 if torch.cuda.is_available() else -1
        logger.info(f"Using device: {'CUDA' if self.device == 0 else 'CPU'}")
        
        try:
            # Initialize summarization pipeline
            self.summarizer = pipeline(
                "summarization",
                model=model_name,
                tokenizer=model_name,
                device=self.device
            )
            self.model_name = model_name
            logger.info("Summarization model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def generate_summary(
        self,
        text: str,
        max_length: int = 100,
        min_length: int = 30,
        do_sample: bool = False
    ) -> str:
        """
        Generate a single summary
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            do_sample: Whether to use sampling (False for deterministic)
            
        Returns:
            Summarized text
        """
        if not text or len(text.strip()) == 0:
            return "No text provided for summarization."
        
        # Truncate input if too long (most models have token limits)
        # BART/T5 typically handle up to 1024 tokens
        max_input_length = 1024
        
        try:
            # For very long texts, we might need to chunk, but for now we'll truncate
            # In production, you'd want smarter chunking
            result = self.summarizer(
                text[:max_input_length * 4],  # Rough character estimate
                max_length=max_length,
                min_length=min_length,
                do_sample=do_sample,
                truncation=True
            )
            
            summary = result[0]["summary_text"]
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            return f"Error generating summary: {str(e)}"
    
    def generate_all_summaries(self, text: str) -> Tuple[str, str, str]:
        """
        Generate three levels of summaries:
        1. Alert (1-line, very short)
        2. Short public summary
        3. Detailed response summary
        
        Args:
            text: Input disaster report text
            
        Returns:
            Tuple of (alert, short_summary, detailed_summary)
        """
        logger.info("Generating multi-level summaries...")
        
        # 1. Alert - 1-line emergency alert
        alert = self.generate_summary(
            text,
            max_length=20,
            min_length=8
        )
        
        # 2. Short public summary - for media/public
        short = self.generate_summary(
            text,
            max_length=60,
            min_length=25
        )
        
        # 3. Detailed summary - for response teams
        detailed = self.generate_summary(
            text,
            max_length=150,
            min_length=60
        )
        
        logger.info("All summaries generated successfully")
        return alert, short, detailed


# Convenience function for direct use
def generate_all_summaries(
    text: str,
    model_name: str = "facebook/bart-large-cnn",
    use_t5: bool = False
) -> Tuple[str, str, str]:
    """
    Convenience function to generate all summary levels
    
    Args:
        text: Input text
        model_name: Model to use
        use_t5: Whether to use T5 instead of BART
        
    Returns:
        Tuple of (alert, short_summary, detailed_summary)
    """
    summarizer = DisasterSummarizer(model_name=model_name, use_t5=use_t5)
    return summarizer.generate_all_summaries(text)


if __name__ == "__main__":
    # Test the module
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
    
    print("Testing summarization...")
    alert, short, detailed = generate_all_summaries(sample_text)
    
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

