"""
Structured Disaster Report Generator
Converts standard summaries into structured, abstractive disaster reports
"""

from typing import Tuple
import logging
import sys
from datetime import datetime
from .summarizer import DisasterSummarizer

# Setup logging with clear format
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)-8s %(message)s',
    datefmt='%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


class StructuredReportGenerator:
    """Generates structured disaster reports with specific sections"""
    
    def __init__(self, summarizer: DisasterSummarizer):
        """
        Initialize with an existing summarizer
        
        Args:
            summarizer: DisasterSummarizer instance
        """
        self.summarizer = summarizer
    
    def _create_structured_prompt(self, text: str) -> str:
        """
        Create a prompt for generating structured disaster report
        
        Args:
            text: Original disaster report text
            
        Returns:
            Formatted prompt string
        """
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Detect disaster type from text for better title generation
        disaster_type = self._detect_disaster_type(text)
        
        prompt = f"""Create a professional disaster assessment report from the following information. 
Write an abstractive summary (rewrite in your own words, do not copy sentences) with this structure:

**TITLE & BYLINE**
Title: Create a concise, specific title about this {disaster_type} disaster
Byline: Disaster Assessment Report | Generated on {current_date}

**INTRODUCTION (What, When, Where)**
Summarize what happened, when it occurred, and where it happened based on the information provided.

**DETAILS OF THE EVENT (How)**
Explain how the disaster unfolded - describe weather conditions, causes, progression, and sequence of events.

**IMPACT & DAMAGE (Figures & Facts)**
Report human impact (casualties, injuries, displacement) ONLY if mentioned in the text. 
Report property and infrastructure damage (homes, roads, power, communication) ONLY if mentioned.
Always use phrases like "according to reports", "preliminary estimates", "initial reports indicate" when citing numbers.
DO NOT make up or invent numbers that are not in the original text.

**RESPONSE & RELIEF EFFORTS**
Summarize any rescue operations, government actions, emergency services deployment, and aid efforts mentioned.

**AFTERMATH & LESSONS LEARNED**
Describe ongoing risks, recovery challenges, and lessons learned about preparedness, resilience, or early warning systems if mentioned in the text.

Original Disaster Report:
{text}

Now generate the structured report following the format above:"""
        
        return prompt
    
    def _detect_disaster_type(self, text: str) -> str:
        """
        Detect disaster type from text for better title generation
        
        Args:
            text: Input text
            
        Returns:
            Disaster type string
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['earthquake', 'seismic', 'tremor', 'richter']):
            return "earthquake"
        elif any(word in text_lower for word in ['flood', 'flooding', 'inundation', 'water']):
            return "flood"
        elif any(word in text_lower for word in ['cyclone', 'hurricane', 'typhoon', 'storm']):
            return "cyclone"
        elif any(word in text_lower for word in ['wildfire', 'fire', 'blaze', 'burning']):
            return "wildfire"
        elif any(word in text_lower for word in ['tsunami', 'tidal wave']):
            return "tsunami"
        elif any(word in text_lower for word in ['drought', 'dry', 'water shortage']):
            return "drought"
        else:
            return "disaster"
    
    def generate_structured_report(self, text: str) -> str:
        """
        Generate a structured disaster report from input text
        
        Args:
            text: Original disaster report text
            
        Returns:
            Structured disaster report string
        """
        text_length = len(text)
        logger.info(f"[STRUCTURED REPORT] Starting structured disaster report generation (input: {text_length} characters)")
        
        current_date = datetime.now().strftime("%B %d, %Y")
        disaster_type = self._detect_disaster_type(text)
        logger.info(f"[STRUCTURED REPORT] Detected disaster type: {disaster_type.upper()}")
        
        # Generate title first
        logger.info("[STRUCTURED REPORT] Step 1/6: Generating Title & Byline...")
        title_prompt = f"Create a concise, professional title for this {disaster_type} disaster report: {text[:200]}"
        title = self.summarizer.generate_summary(title_prompt, max_length=15, min_length=5)
        title = title.strip().rstrip('.')
        logger.info(f"[STRUCTURED REPORT] ✓ Title generated: '{title}'")
        
        # Generate each section separately for better control
        sections = {}
        
        # Introduction (What, When, Where) - Focus on basic facts only
        logger.info("[STRUCTURED REPORT] Step 2/6: Generating Introduction (What, When, Where)...")
        intro_prompt = f"Question: What type of disaster, when did it occur, and where? Answer ONLY these three questions in 2-3 sentences. Do not describe how it happened or its impact. Text: {text}"
        sections['introduction'] = self.summarizer.generate_summary(intro_prompt, max_length=80, min_length=30)
        # Clean up to ensure it's different
        if sections['introduction'].lower().startswith('a powerful'):
            sections['introduction'] = sections['introduction'].replace('A powerful', 'The disaster', 1)
        logger.info(f"[STRUCTURED REPORT] ✓ Introduction generated ({len(sections['introduction'])} characters)")
        
        # Details (How) - Focus on sequence and mechanism
        logger.info("[STRUCTURED REPORT] Step 3/6: Generating Details of the Event (How)...")
        details_prompt = f"Question: How did this disaster develop and progress? Describe the sequence, intensity changes, weather conditions, and physical processes. Do NOT mention what/when/where or casualties. Text: {text}"
        sections['details'] = self.summarizer.generate_summary(details_prompt, max_length=100, min_length=40)
        logger.info(f"[STRUCTURED REPORT] ✓ Event details generated ({len(sections['details'])} characters)")
        
        # Impact & Damage - Focus on numbers and specific damage
        logger.info("[STRUCTURED REPORT] Step 4/6: Generating Impact & Damage section...")
        impact_prompt = f"Question: What are the human casualties, injuries, deaths, displaced people, and damage to buildings and infrastructure? Extract ONLY numbers and damage facts. Use 'according to reports' or 'preliminary estimates'. If no numbers, say 'assessment ongoing'. Do NOT describe the disaster event. Text: {text}"
        sections['impact'] = self.summarizer.generate_summary(impact_prompt, max_length=100, min_length=40)
        logger.info(f"[STRUCTURED REPORT] ✓ Impact & Damage section generated ({len(sections['impact'])} characters)")
        
        # Response & Relief - Focus on actions taken
        logger.info("[STRUCTURED REPORT] Step 5/6: Generating Response & Relief Efforts section...")
        response_prompt = f"Question: What rescue operations, emergency services, government actions, relief efforts, and aid were deployed? Extract ONLY response actions. Do NOT describe the disaster or impact. Text: {text}"
        sections['response'] = self.summarizer.generate_summary(response_prompt, max_length=80, min_length=30)
        logger.info(f"[STRUCTURED REPORT] ✓ Response & Relief section generated ({len(sections['response'])} characters)")
        
        # Aftermath & Lessons - Focus on future implications
        logger.info("[STRUCTURED REPORT] Step 6/6: Generating Aftermath & Lessons Learned section...")
        aftermath_prompt = f"Question: What are the ongoing risks, recovery challenges, and lessons about preparedness or early warning systems? Focus on future implications. If not mentioned, briefly note recovery will be challenging. Do NOT repeat disaster or response details. Text: {text}"
        sections['aftermath'] = self.summarizer.generate_summary(aftermath_prompt, max_length=80, min_length=30)
        logger.info(f"[STRUCTURED REPORT] ✓ Aftermath & Lessons section generated ({len(sections['aftermath'])} characters)")
        
        # Post-process sections to ensure they're distinct
        sections = self._ensure_section_diversity(sections)
        
        # Assemble structured report
        structured_report = f"""**TITLE & BYLINE**
{title}
Disaster Assessment Report | Generated on {current_date}

**INTRODUCTION (What, When, Where)**
{sections['introduction']}

**DETAILS OF THE EVENT (How)**
{sections['details']}

**IMPACT & DAMAGE (Figures & Facts)**
{sections['impact']}

**RESPONSE & RELIEF EFFORTS**
{sections['response']}

**AFTERMATH & LESSONS LEARNED**
{sections['aftermath']}"""
        
        total_length = len(structured_report)
        logger.info(f"[STRUCTURED REPORT] ✓ Structured disaster report generated successfully ({total_length} characters, 6 sections)")
        return structured_report
    
    def _ensure_section_diversity(self, sections: dict) -> dict:
        """
        Ensure sections are distinct and don't repeat the same content
        
        Args:
            sections: Dictionary of section content
            
        Returns:
            Dictionary with diversified sections
        """
        # Check if sections are too similar (first 50 chars match)
        intro_start = sections['introduction'][:50].lower().strip()
        details_start = sections['details'][:50].lower().strip()
        impact_start = sections['impact'][:50].lower().strip()
        
        # If introduction and details start the same, modify details
        if intro_start == details_start and len(intro_start) > 20:
            logger.warning("[STRUCTURED REPORT] Introduction and Details sections are too similar, adjusting...")
            # Try to extract different part of the text for details
            if "how" in sections['details'].lower() or "developed" in sections['details'].lower():
                # Already has some differentiation, keep it
                pass
            else:
                # Prepend to make it about progression
                sections['details'] = f"The disaster progressed as follows: {sections['details']}"
        
        # If impact section repeats disaster description, extract numbers only
        if impact_start == intro_start or impact_start == details_start:
            logger.warning("[STRUCTURED REPORT] Impact section is repeating disaster description, adjusting...")
            # Try to focus on numbers and damage
            impact_lower = sections['impact'].lower()
            if any(word in impact_lower for word in ['casualties', 'injured', 'damage', 'destroyed', 'evacuated']):
                # Has relevant content, keep it but maybe rephrase start
                if sections['impact'].startswith('A powerful') or sections['impact'].startswith('The disaster'):
                    sections['impact'] = sections['impact'].replace('A powerful', 'According to initial reports,', 1)
                    sections['impact'] = sections['impact'].replace('The disaster', 'Initial assessments indicate', 1)
        
        return sections
    
    def _post_process_report(self, report: str) -> str:
        """
        Post-process the generated report to ensure proper structure
        
        Args:
            report: Generated report text
            
        Returns:
            Formatted report with proper section headers
        """
        # Clean up the report
        report = report.strip()
        
        # Ensure proper section formatting
        # Look for section markers and format them consistently
        sections_map = {
            "TITLE": "**TITLE & BYLINE**",
            "BYLINE": "**TITLE & BYLINE**",
            "INTRODUCTION": "**INTRODUCTION (What, When, Where)**",
            "DETAILS": "**DETAILS OF THE EVENT (How)**",
            "IMPACT": "**IMPACT & DAMAGE (Figures & Facts)**",
            "RESPONSE": "**RESPONSE & RELIEF EFFORTS**",
            "AFTERMATH": "**AFTERMATH & LESSONS LEARNED**",
            "LESSONS": "**AFTERMATH & LESSONS LEARNED**"
        }
        
        lines = report.split('\n')
        formatted_lines = []
        last_section = None
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                formatted_lines.append('')
                continue
                
            line_upper = line_stripped.upper()
            
            # Check if this line is a section header
            section_found = None
            for key, section_name in sections_map.items():
                if key in line_upper and (len(line_stripped) < 100):  # Likely a header
                    section_found = section_name
                    break
            
            if section_found and section_found != last_section:
                formatted_lines.append('')  # Add spacing before section
                formatted_lines.append(section_found)
                formatted_lines.append('')
                last_section = section_found
            else:
                formatted_lines.append(line_stripped)
        
        result = '\n'.join(formatted_lines)
        
        # Clean up excessive newlines (more than 2 consecutive)
        import re
        result = re.sub(r'\n{3,}', '\n\n', result)
        
        # Ensure title and byline are at the top
        if "**TITLE & BYLINE**" not in result:
            # Try to add it if missing
            current_date = datetime.now().strftime("%B %d, %Y")
            result = f"**TITLE & BYLINE**\nDisaster Assessment Report | Generated on {current_date}\n\n{result}"
        
        return result.strip()
    
    def generate_all_summaries_with_structured_report(
        self, 
        text: str
    ) -> Tuple[str, str, str]:
        """
        Generate Alert, Short, and Structured Detailed Report
        
        Args:
            text: Input disaster report text
            
        Returns:
            Tuple of (alert, short_summary, structured_detailed_report)
        """
        logger.info("[PIPELINE] Generating Alert and Short summaries (standard format)...")
        # Generate standard alert and short summaries (unchanged)
        alert, short, _ = self.summarizer.generate_all_summaries(text)
        logger.info("[PIPELINE] ✓ Alert and Short summaries completed")
        
        # Generate structured detailed report
        logger.info("[PIPELINE] Generating Structured Detailed Report...")
        structured_report = self.generate_structured_report(text)
        logger.info("[PIPELINE] ✓ All summaries generated: Alert, Short, and Structured Report")
        
        return alert, short, structured_report

