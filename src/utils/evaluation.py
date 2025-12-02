"""
Evaluation Module for Summarization Quality
Includes ROUGE metrics and human evaluation support
"""

from typing import List, Dict, Optional
import logging
from dataclasses import dataclass

try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    ROUGE_AVAILABLE = False
    logging.warning("rouge_score not installed. Install with: pip install rouge-score")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SummaryMetrics:
    """Container for summary evaluation metrics"""
    rouge_1_f: float = 0.0
    rouge_1_p: float = 0.0
    rouge_1_r: float = 0.0
    rouge_2_f: float = 0.0
    rouge_2_p: float = 0.0
    rouge_2_r: float = 0.0
    rouge_l_f: float = 0.0
    rouge_l_p: float = 0.0
    rouge_l_r: float = 0.0


class SummarizationEvaluator:
    """Evaluator for summarization quality"""
    
    def __init__(self):
        """Initialize evaluator with ROUGE scorer"""
        if ROUGE_AVAILABLE:
            self.rouge_scorer = rouge_scorer.RougeScorer(
                ['rouge1', 'rouge2', 'rougeL'],
                use_stemmer=True
            )
        else:
            self.rouge_scorer = None
            logger.warning("ROUGE scorer not available")
    
    def compute_rouge(
        self,
        reference: str,
        candidate: str
    ) -> SummaryMetrics:
        """
        Compute ROUGE scores between reference and candidate summaries
        
        Args:
            reference: Reference (ground truth) summary
            candidate: Generated summary to evaluate
            
        Returns:
            SummaryMetrics object with ROUGE scores
        """
        if not ROUGE_AVAILABLE or self.rouge_scorer is None:
            logger.warning("ROUGE not available, returning empty metrics")
            return SummaryMetrics()
        
        scores = self.rouge_scorer.score(reference, candidate)
        
        metrics = SummaryMetrics(
            rouge_1_f=scores['rouge1'].fmeasure,
            rouge_1_p=scores['rouge1'].precision,
            rouge_1_r=scores['rouge1'].recall,
            rouge_2_f=scores['rouge2'].fmeasure,
            rouge_2_p=scores['rouge2'].precision,
            rouge_2_r=scores['rouge2'].recall,
            rouge_l_f=scores['rougeL'].fmeasure,
            rouge_l_p=scores['rougeL'].precision,
            rouge_l_r=scores['rougeL'].recall,
        )
        
        return metrics
    
    def evaluate_batch(
        self,
        references: List[str],
        candidates: List[str]
    ) -> Dict[str, float]:
        """
        Evaluate a batch of summaries
        
        Args:
            references: List of reference summaries
            candidates: List of candidate summaries
            
        Returns:
            Dictionary with average ROUGE scores
        """
        if len(references) != len(candidates):
            raise ValueError("References and candidates must have same length")
        
        all_metrics = []
        for ref, cand in zip(references, candidates):
            metrics = self.compute_rouge(ref, cand)
            all_metrics.append(metrics)
        
        # Compute averages
        avg_metrics = {
            'rouge_1_f': sum(m.rouge_1_f for m in all_metrics) / len(all_metrics),
            'rouge_1_p': sum(m.rouge_1_p for m in all_metrics) / len(all_metrics),
            'rouge_1_r': sum(m.rouge_1_r for m in all_metrics) / len(all_metrics),
            'rouge_2_f': sum(m.rouge_2_f for m in all_metrics) / len(all_metrics),
            'rouge_2_p': sum(m.rouge_2_p for m in all_metrics) / len(all_metrics),
            'rouge_2_r': sum(m.rouge_2_r for m in all_metrics) / len(all_metrics),
            'rouge_l_f': sum(m.rouge_l_f for m in all_metrics) / len(all_metrics),
            'rouge_l_p': sum(m.rouge_l_p for m in all_metrics) / len(all_metrics),
            'rouge_l_r': sum(m.rouge_l_r for m in all_metrics) / len(all_metrics),
        }
        
        return avg_metrics
    
    def print_metrics(self, metrics: SummaryMetrics, title: str = "Evaluation Metrics"):
        """
        Print metrics in a readable format
        
        Args:
            metrics: SummaryMetrics object
            title: Title for the output
        """
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}")
        print(f"ROUGE-1 F1:  {metrics.rouge_1_f:.4f} (P: {metrics.rouge_1_p:.4f}, R: {metrics.rouge_1_r:.4f})")
        print(f"ROUGE-2 F1:  {metrics.rouge_2_f:.4f} (P: {metrics.rouge_2_p:.4f}, R: {metrics.rouge_2_r:.4f})")
        print(f"ROUGE-L F1:  {metrics.rouge_l_f:.4f} (P: {metrics.rouge_l_p:.4f}, R: {metrics.rouge_l_r:.4f})")
        print(f"{'='*60}\n")


def human_evaluation_template(
    text: str,
    alert: str,
    short: str,
    detailed: str
) -> Dict[str, Dict[str, int]]:
    """
    Template for human evaluation
    
    Returns a dictionary structure for rating summaries on:
    - Relevance (1-5)
    - Conciseness (1-5)
    - Fluency (1-5)
    
    Args:
        text: Original text
        alert: Alert summary
        short: Short summary
        detailed: Detailed summary
        
    Returns:
        Dictionary with evaluation structure
    """
    return {
        "alert": {
            "relevance": 0,  # Rate 1-5
            "conciseness": 0,  # Rate 1-5
            "fluency": 0  # Rate 1-5
        },
        "short": {
            "relevance": 0,
            "conciseness": 0,
            "fluency": 0
        },
        "detailed": {
            "relevance": 0,
            "conciseness": 0,
            "fluency": 0
        }
    }


if __name__ == "__main__":
    # Test evaluation
    if ROUGE_AVAILABLE:
        evaluator = SummarizationEvaluator()
        
        reference = "A severe earthquake struck the region, causing significant damage and casualties."
        candidate = "An earthquake hit the area, resulting in damage and injuries."
        
        metrics = evaluator.compute_rouge(reference, candidate)
        evaluator.print_metrics(metrics, "Test Evaluation")
    else:
        print("ROUGE not available. Install with: pip install rouge-score")

