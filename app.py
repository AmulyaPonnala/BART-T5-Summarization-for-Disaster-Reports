"""
Streamlit UI for BART/T5 Disaster Report Summarization System
Main demo application
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models.summarizer import DisasterSummarizer
from models.structured_report import StructuredReportGenerator

# Page configuration
st.set_page_config(
    page_title="Disaster Report Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .summary-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        color: #000000;
    }
    .alert-box {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .short-box {
        background-color: #d1ecf1;
        border-left-color: #17a2b8;
    }
    .detailed-box {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📝 Audience-Adaptive Disaster Report Summarizer</h1>', unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem;">
            Transform disaster reports into audience-specific multi-level summaries using BART/T5 transformers
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    use_t5 = st.checkbox(
        "Use T5 Model (instead of BART)",
        value=False,
        help="T5 is an alternative transformer model"
    )
    
    if use_t5:
        summarizer_model = st.selectbox(
            "T5 Model",
            ["t5-base", "t5-large"],
            index=0
        )
    else:
        summarizer_model = st.selectbox(
            "BART Model",
            ["facebook/bart-large-cnn", "facebook/bart-base"],
            index=1,  # Default to bart-base for faster processing
            help="bart-base is faster, bart-large-cnn is more accurate"
        )
    
    # Performance options
    st.markdown("---")
    st.markdown("### ⚡ Performance Options")
    fast_mode = st.checkbox(
        "Fast Mode (Skip Structured Report)",
        value=False,
        help="Skip detailed structured report generation for faster results (3 summaries only)"
    )
    use_smaller_model = st.checkbox(
        "Use Smaller Model (Faster)",
        value=False,
        help="Use smaller model variant for faster processing (may reduce quality slightly)"
    )
    
    st.markdown("---")
    st.markdown("### 📊 System Pipeline")
    st.markdown("""
        1. **Text Input** → Disaster Report Text
        2. **Text Preprocessing** → Cleaning & Normalization
        3. **Audience-Adaptive Summarization** → T5/BART Transformers guided by audience role & abstraction level
        4. **Multi-Level Outputs** → General Public, Emergency Responders, Authorities
    """)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    This system uses:
    - **NLP** (Text Processing)
    - **Deep Learning** (BART/T5 Transformers)
    - **Audience-Aware Multi-Level Summarization** (General Public, Emergency Responders, Authorities)
    - **Real-world Application** (Disaster Response)
    """)

# Main content area
st.markdown("## 📝 Enter Disaster Report Text")

# Text input area
input_text = st.text_area(
    "Paste or type your disaster report text here",
    height=200,
    placeholder="Example: A severe earthquake measuring 7.2 on the Richter scale struck the northern region early this morning at 3:45 AM. The epicenter was located 15 kilometers northeast of the city center. Initial reports indicate significant structural damage to residential buildings in the downtown area. Emergency services have been deployed to assess the situation. At least 50 people have been reported injured, with 5 confirmed fatalities. Hospitals are on high alert and accepting casualties. Power outages have been reported in several districts. The government has activated the emergency response protocol and is coordinating rescue operations.",
    help="Enter a disaster report text (recommended: 100-5000 characters)"
)

# Process button
if input_text and len(input_text.strip()) > 0:
    if st.button("🚀 Generate Summaries", type="primary", use_container_width=True):
        with st.spinner("🔄 Generating summaries... This may take a minute..."):
            try:
                # Ensure summarizer matches current configuration; re-initialize if needed
                current_config = {
                    "model_name": summarizer_model,
                    "use_t5": use_t5,
                }

                if (
                    "summarizer" not in st.session_state
                    or "summarizer_config" not in st.session_state
                    or st.session_state.summarizer is None
                    or st.session_state.summarizer_config != current_config
                ):
                    st.session_state.summarizer = DisasterSummarizer(**current_config)
                    st.session_state.summarizer_config = current_config
                    # Initialize structured report generator
                    st.session_state.report_generator = StructuredReportGenerator(st.session_state.summarizer)
                elif "report_generator" not in st.session_state:
                    st.session_state.report_generator = StructuredReportGenerator(st.session_state.summarizer)

                # Generate summaries based on mode
                if fast_mode:
                    # Fast mode: Only generate the 3 audience-specific summaries (skip structured report)
                    alert, short, detailed = st.session_state.summarizer.generate_all_summaries(input_text.strip())
                    structured_report = None
                else:
                    # Full mode: Generate all summaries including structured report
                    alert, short, structured_report = st.session_state.report_generator.generate_all_summaries_with_structured_report(input_text.strip())
                
                # Display results
                st.markdown("---")
                st.markdown("## 📋 Audience-Specific Results")
                
                # General public – alert summary
                st.markdown("### 🔔 General Public Alert (1-line, high-abstraction)")
                st.markdown(f'<div class="summary-box alert-box">{alert}</div>', unsafe_allow_html=True)
                
                # Emergency responders – operational summary
                st.markdown("### 🧑‍🚒 Emergency Responder Operational Summary (medium abstraction)")
                st.markdown(f'<div class="summary-box short-box">{short}</div>', unsafe_allow_html=True)
                
                # Authorities – structured detailed report (only if not in fast mode)
                if structured_report:
                    # Display structured report with heading inside the styled box
                    # Convert markdown formatting to HTML for proper rendering inside the div
                    formatted_report = structured_report
                    # Convert markdown bold (**text**) to HTML bold
                    import re
                    formatted_report = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_report)
                    # Convert newlines to HTML line breaks
                    formatted_report = formatted_report.replace('\n', '<br>')
                    
                    box_content = f'<h4 style="margin-top: 0; margin-bottom: 1rem;">🏛️ Authorities Strategic Structured Disaster Assessment Report (low abstraction)</h4>{formatted_report}'
                    st.markdown(f'<div class="summary-box detailed-box">{box_content}</div>', unsafe_allow_html=True)
                else:
                    # In fast mode, show the detailed summary instead
                    st.markdown("### 🏛️ Authorities Strategic Summary (low abstraction)")
                    st.markdown(f'<div class="summary-box detailed-box">{detailed}</div>', unsafe_allow_html=True)
                
                # Download options
                st.markdown("---")
                st.markdown("### 💾 Download Summaries")
                
                summary_text = f"""DISASTER REPORT SUMMARIES

🔔 GENERAL PUBLIC ALERT (1-line, high-abstraction):
{alert}

🧑‍🚒 EMERGENCY RESPONDER OPERATIONAL SUMMARY (medium abstraction):
{short}

🏛️ AUTHORITIES STRATEGIC STRUCTURED DISASTER ASSESSMENT REPORT (low abstraction):
{structured_report}

---
Original Text:
{input_text}
"""
                
                st.download_button(
                    label="📥 Download All Summaries",
                    data=summary_text,
                    file_name="disaster_report_summaries.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating summaries: {str(e)}")
                st.exception(e)
elif input_text and len(input_text.strip()) == 0:
    st.warning("⚠️ Please enter some text to generate summaries.")
else:
    st.info("💡 Enter disaster report text above and click 'Generate Summaries' to get multi-level summaries.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; padding: 2rem;">
    <p>BART/T5 Disaster Report Summarization System</p>
    <p>Powered by Transformers (BART/T5)</p>
</div>
""", unsafe_allow_html=True)
