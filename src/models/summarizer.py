"""
Text Summarization Module using T5 and BART Transformers
Generates multi-level summaries for disaster reports
"""

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from typing import Tuple, Optional, Literal
from enum import Enum
import logging
import sys
from pathlib import Path

# Setup logging with clear format
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)-8s %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class AudienceRole(str, Enum):
    """
    Supported audience roles for audience-adaptive summarization.
    
    NOTE: These are deliberately simple string enums so they can be
    logged, displayed in the UI, and (if desired later) exposed as
    part of an external API without extra mapping logic.
    """

    GENERAL_PUBLIC = "general_public"
    EMERGENCY_RESPONDERS = "emergency_responders"
    AUTHORITIES = "authorities"


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
            logger.info(f"[MODEL] Initializing T5 summarization model: {model_name}")
        else:
            logger.info(f"[MODEL] Initializing BART summarization model: {model_name}")
        
        self.device = 0 if torch.cuda.is_available() else -1
        device_name = 'CUDA (GPU)' if self.device == 0 else 'CPU'
        logger.info(f"[MODEL] Computing device: {device_name}")
        
        try:
            logger.info(f"[MODEL] Downloading/loading model and tokenizer... (this may take a minute on first run)")
            # Initialize summarization pipeline
            self.summarizer = pipeline(
                "summarization",
                model=model_name,
                tokenizer=model_name,
                device=self.device
            )
            self.model_name = model_name
            logger.info(f"[MODEL] ✓ Model '{model_name}' loaded successfully on {device_name}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to load model '{model_name}': {str(e)}")
            raise
    
    def generate_summary(
        self,
        text: str,
        max_length: int = 100,
        min_length: int = 30,
        do_sample: bool = False,
        audience_role: Optional[AudienceRole] = None,
        abstraction_level: Optional[Literal["high", "medium", "low"]] = None,
    ) -> str:
        """
        Generate a single summary
        
        Args:
            text: Input text to summarize (raw disaster report text)
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            do_sample: Whether to use sampling (False for deterministic)
            audience_role: Optional audience role this summary is intended for.
                           If provided, the summarization will be *guided*
                           towards that audience via a lightweight control
                           prefix rather than a separate model.
            abstraction_level: Optional abstraction level for the summary:
                               - "high": very short, coarse, non-technical
                               - "medium": balanced operational detail
                               - "low": detailed, analytical/administrative
            
        Returns:
            Summarized text
        """
        if not text or len(text.strip()) == 0:
            return "No text provided for summarization."
        
        # Truncate input if too long (most models have token limits)
        # BART/T5 typically handle up to 1024 tokens
        max_input_length = 1024
        
        try:
            # For very long texts, we might need to chunk, but for now we'll truncate.
            # In production, you'd want smarter chunking by sentence/paragraph.
            base_text = text[: max_input_length * 4]  # Rough character estimate
            if len(text) > len(base_text):
                logger.warning(
                    f"[SUMMARIZATION] Input text truncated from {len(text)} to {len(base_text)} characters"
                )

            # Inject lightweight audience/abstraction control as a prefix.
            # This preserves the single underlying transformer model
            # while making the system explicitly audience-aware.
            if audience_role or abstraction_level:
                guidance_parts = []

                if audience_role:
                    if audience_role == AudienceRole.GENERAL_PUBLIC:
                        guidance_parts.append(
                            "AUDIENCE: GENERAL PUBLIC. "
                            "TASK: Write a simple, non-technical, easy-to-understand summary "
                            "that explains what happened and basic safety implications."
                        )
                    elif audience_role == AudienceRole.EMERGENCY_RESPONDERS:
                        guidance_parts.append(
                            "AUDIENCE: EMERGENCY RESPONDERS. "
                            "TASK: Write an operational situation summary focusing on "
                            "affected areas, current conditions, access constraints, and "
                            "information useful for field coordination."
                        )
                    elif audience_role == AudienceRole.AUTHORITIES:
                        guidance_parts.append(
                            "AUDIENCE: GOVERNMENT AUTHORITIES. "
                            "TASK: Write a strategic overview focusing on overall impact, "
                            "key figures, priorities, and coordination needs for decision-makers."
                        )

                if abstraction_level:
                    if abstraction_level == "high":
                        guidance_parts.append(
                            "ABSTRACTION LEVEL: HIGH. Focus on only the most critical points, "
                            "avoid technical details, and keep the summary very short."
                        )
                    elif abstraction_level == "medium":
                        guidance_parts.append(
                            "ABSTRACTION LEVEL: MEDIUM. Balance brevity with operationally "
                            "useful details while keeping the text readable."
                        )
                    elif abstraction_level == "low":
                        guidance_parts.append(
                            "ABSTRACTION LEVEL: LOW. Include key figures, concrete impacts, "
                            "and nuanced context while remaining concise."
                        )

                guidance_prefix = " ".join(guidance_parts).strip()
                if guidance_prefix:
                    input_text = f"{guidance_prefix}\n\nDisaster report:\n{base_text}"
                else:
                    input_text = base_text
            else:
                # Backwards-compatible behaviour: generic summarization
                input_text = base_text
            
            result = self.summarizer(
                input_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=do_sample,
                truncation=True
            )
            
            summary = result[0]["summary_text"]
            summary_length = len(summary.strip())
            logger.debug(f"[SUMMARIZATION] Generated summary: {summary_length} characters (target: {min_length}-{max_length} tokens)")
            return summary.strip()
            
        except Exception as e:
            logger.error(f"[ERROR] Summarization failed: {str(e)}")
            return f"Error generating summary: {str(e)}"
    
    def generate_all_summaries(self, text: str) -> Tuple[str, str, str]:
        """
        Generate three levels of summaries:
        1. General-public alert summary (high abstraction)
        2. Emergency responder operational summary (medium abstraction)
        3. Authority / administrative strategic summary (low abstraction)
        
        Args:
            text: Input disaster report text
            
        Returns:
            Tuple of (alert, short_summary, detailed_summary)
        """
        text_length = len(text)
        logger.info(
            f"[SUMMARIZATION] Starting audience-adaptive multi-level summary generation "
            f"(input text: {text_length} characters)"
        )
        
        # 1. General public – very short, high-abstraction alert
        logger.info(
            "[SUMMARIZATION] Step 1/3: Generating GENERAL PUBLIC alert summary "
            "(1-line, high-abstraction, non-technical)..."
        )
        alert = self.generate_summary(
            text,
            max_length=20,
            min_length=8,
            audience_role=AudienceRole.GENERAL_PUBLIC,
            abstraction_level="high",
        )
        logger.info(f"[SUMMARIZATION] ✓ Alert generated ({len(alert)} characters)")
        
        # 2. Emergency responders – operational, medium abstraction
        logger.info(
            "[SUMMARIZATION] Step 2/3: Generating EMERGENCY RESPONDER operational summary "
            "(medium-length, situation + operations focus)..."
        )
        short = self.generate_summary(
            text,
            max_length=60,
            min_length=25,
            audience_role=AudienceRole.EMERGENCY_RESPONDERS,
            abstraction_level="medium",
        )
        logger.info(f"[SUMMARIZATION] ✓ Short summary generated ({len(short)} characters)")
        
        # 3. Authorities – detailed, low abstraction strategic overview
        logger.info(
            "[SUMMARIZATION] Step 3/3: Generating AUTHORITY strategic summary "
            "(longer, low-abstraction, impact + coordination focus)..."
        )
        detailed = self.generate_summary(
            text,
            max_length=150,
            min_length=60,
            audience_role=AudienceRole.AUTHORITIES,
            abstraction_level="low",
        )
        logger.info(f"[SUMMARIZATION] ✓ Detailed summary generated ({len(detailed)} characters)")
        
        logger.info("[SUMMARIZATION] ✓ All three summary levels generated successfully")
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

