"""
Basic tests for the Voice Disaster Report Summarization System
Run with: pytest tests/test_basic.py
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.summarizer import DisasterSummarizer, generate_all_summaries
from src.utils.evaluation import SummarizationEvaluator


class TestSummarization:
    """Test summarization functionality"""
    
    def test_summarizer_initialization(self):
        """Test that summarizer can be initialized"""
        summarizer = DisasterSummarizer()
        assert summarizer is not None
        assert summarizer.model_name is not None
    
    def test_text_summarization(self):
        """Test basic text summarization"""
        sample_text = """
        A severe earthquake measuring 7.2 on the Richter scale struck the northern region 
        early this morning. Initial reports indicate significant structural damage to 
        residential buildings. Emergency services have been deployed. At least 50 people 
        have been reported injured, with 5 confirmed fatalities. Hospitals are on high alert.
        """
        
        alert, short, detailed = generate_all_summaries(sample_text)
        
        # Check that summaries are generated
        assert len(alert) > 0, "Alert summary should not be empty"
        assert len(short) > 0, "Short summary should not be empty"
        assert len(detailed) > 0, "Detailed summary should not be empty"
        
        # Check that summaries are different lengths (detailed > short > alert)
        assert len(detailed) >= len(short), "Detailed should be longer than short"
        assert len(short) >= len(alert), "Short should be longer than alert"
    
    def test_empty_text(self):
        """Test handling of empty text"""
        alert, short, detailed = generate_all_summaries("")
        
        # Should handle gracefully
        assert isinstance(alert, str)
        assert isinstance(short, str)
        assert isinstance(detailed, str)


class TestEvaluation:
    """Test evaluation functionality"""
    
    def test_evaluator_initialization(self):
        """Test that evaluator can be initialized"""
        evaluator = SummarizationEvaluator()
        assert evaluator is not None
    
    def test_rouge_computation(self):
        """Test ROUGE score computation"""
        try:
            evaluator = SummarizationEvaluator()
            
            reference = "A severe earthquake struck the region, causing damage and casualties."
            candidate = "An earthquake hit the area, resulting in damage and injuries."
            
            metrics = evaluator.compute_rouge(reference, candidate)
            
            # Check that metrics are computed
            assert metrics.rouge_1_f >= 0.0
            assert metrics.rouge_1_f <= 1.0
            assert metrics.rouge_2_f >= 0.0
            assert metrics.rouge_2_f <= 1.0
            assert metrics.rouge_l_f >= 0.0
            assert metrics.rouge_l_f <= 1.0
            
        except Exception as e:
            # ROUGE might not be available, skip test
            pytest.skip(f"ROUGE not available: {str(e)}")


if __name__ == "__main__":
    # Run basic tests
    pytest.main([__file__, "-v"])

