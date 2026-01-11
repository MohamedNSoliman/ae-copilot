"""
AE Copilot - Streamlit app for ROI calculation, Gong enrichment, and CRM integration.
Focused on structured enrichment + ROI calculation (no narrative generation).
"""

import streamlit as st
import sys
from pathlib import Path
import os

# Load custom JavaScript and CSS
def load_custom_assets():
    """Load custom JavaScript and CSS files."""
    js_path = Path(__file__).parent / "static" / "js" / "enhancements.js"
    css_path = Path(__file__).parent / "static" / "css" / "custom.css"
    
    if js_path.exists():
        with open(js_path, 'r') as f:
            st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)
    
    if css_path.exists():
        with open(css_path, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.schemas import ROIInputs, ROIOutputs, ExtractedSignals, CRMContext
from src.roi_calculator import calculate_roi
from src.gong_client import GongClient
from src.crm_client import HubSpotClient
from src.export import create_narrative_pack, export_narrative_pack
from src.business_case import generate_business_case
from src.storage import (
    save_roi_calculator, save_business_case,
    get_roi_calculators, get_business_cases,
    load_roi_calculator, load_business_case,
    get_companies
)


# Modern Superhuman/Grammarly/ChatGPT-inspired CSS
MODERN_UI_CSS = """
<style>
    /* Base styling - Superhuman inspired */
    .stApp {
        background: #ffffff;
        color: #1a1a1a;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth transitions */
    * {
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Typography - Grammarly inspired */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        letter-spacing: -0.02em;
        color: #0a0a0a;
        margin-top: 0;
    }
    
    h1 {
        font-size: 2rem;
        line-height: 1.2;
    }
    
    h2 {
        font-size: 1.5rem;
        line-height: 1.3;
    }
    
    /* Input fields - Superhuman style */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #ffffff;
        color: #1a1a1a;
        border: 1.5px solid #e5e5e5;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 14px;
        font-weight: 400;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af;
    }
    
    /* Buttons - Modern, clean */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    button[kind="secondary"] {
        background-color: #f9fafb !important;
        color: #374151 !important;
        border: 1.5px solid #e5e7eb !important;
        box-shadow: none !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: #f3f4f6 !important;
        border-color: #d1d5db !important;
    }
    
    /* Tabs - ChatGPT style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 0;
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-radius: 8px 8px 0 0;
        color: #6b7280;
        padding: 12px 20px;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #f9fafb;
        color: #374151;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #6366f1;
        border-bottom: 2px solid #6366f1;
        font-weight: 600;
    }
    
    /* Metrics - Clean cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: #0a0a0a;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    /* Success/Error/Info - Grammarly style */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border: none;
        color: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        border: none;
        color: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border: none;
        color: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border: none;
        color: white;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
    }
    
    /* Sidebar - Clean, minimal */
    .css-1d391kg {
        background-color: #fafafa;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Expanders - Modern cards */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        color: #1a1a1a;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px;
        font-weight: 500;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f9fafb;
        border-color: #d1d5db;
    }
    
    /* Forms - Clean spacing */
    .stForm {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 24px;
        background: #ffffff;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    }
    
    /* Selectbox/Dropdown */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 1.5px solid #e5e5e5;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Slider */
    .stSlider > div > div {
        padding: 8px 0;
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #374151;
        font-weight: 400;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 32px 0;
    }
    
    /* Code blocks */
    code {
        background: #f3f4f6;
        color: #dc2626;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.875em;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
    }
    
    /* Scrollbar - Modern */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f9fafb;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
    /* Caption styling */
    .stMarkdown p {
        color: #6b7280;
        font-size: 0.875rem;
        line-height: 1.5;
    }
    
    /* Main container padding */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Title styling */
    h1 {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    /* JSON viewer */
    .stJson {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px;
    }
</style>
"""


# Initialize session state
if "roi_inputs" not in st.session_state:
    st.session_state.roi_inputs = None
if "roi_outputs" not in st.session_state:
    st.session_state.roi_outputs = None
if "gong_signals" not in st.session_state:
    st.session_state.gong_signals = None
if "crm_context" not in st.session_state:
    st.session_state.crm_context = None
if "account_name" not in st.session_state:
    st.session_state.account_name = None


def render_roi_calculator():
    """Render ROI Calculator section."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin-bottom: 4px;">ROI Calculator</h2>
        <p style="color: #6b7280; font-size: 14px; margin: 0;">Calculate developer productivity ROI for Cursor</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("roi_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            team_size = st.number_input(
                "Team Size (Engineering)",
                min_value=1,
                value=st.session_state.roi_inputs.team_size_engineering if st.session_state.roi_inputs else 10,
                step=1,
                help="Number of engineers on the team"
            )
            
            fully_loaded_cost = st.number_input(
                "Fully Loaded Cost per Engineer ($)",
                min_value=0.0,
                value=st.session_state.roi_inputs.fully_loaded_cost_per_engineer if st.session_state.roi_inputs else 220000.0,
                step=10000.0,
                help="Annual fully loaded cost per engineer"
            )
            
            hours_saved = st.number_input(
                "Hours Saved per Engineer per Week",
                min_value=0.0,
                value=st.session_state.roi_inputs.hours_saved_per_engineer_per_week if st.session_state.roi_inputs else 5.0,
                step=0.5,
                help="Hours saved per engineer per week"
            )
        
        with col2:
            adoption_rate = st.slider(
                "Adoption Rate",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.roi_inputs.adoption_rate if st.session_state.roi_inputs else 0.7,
                step=0.05,
                format="%.0%",
                help="Expected adoption rate (0-100%)"
            )
            
            weeks_per_year = st.number_input(
                "Weeks per Year",
                min_value=1,
                max_value=52,
                value=st.session_state.roi_inputs.weeks_per_year if st.session_state.roi_inputs else 48,
                step=1,
                help="Working weeks per year"
            )
            
            cursor_cost = st.number_input(
                "Cursor Annual Cost ($)",
                min_value=0.0,
                value=st.session_state.roi_inputs.cursor_annual_cost if st.session_state.roi_inputs else 0.0,
                step=1000.0,
                help="Annual cost of Cursor"
            )
        
        submitted = st.form_submit_button("Calculate ROI", use_container_width=True)
        
        if submitted:
            try:
                inputs = ROIInputs(
                    team_size_engineering=team_size,
                    fully_loaded_cost_per_engineer=fully_loaded_cost,
                    hours_saved_per_engineer_per_week=hours_saved,
                    adoption_rate=adoption_rate,
                    weeks_per_year=weeks_per_year,
                    cursor_annual_cost=cursor_cost
                )
                
                outputs = calculate_roi(inputs)
                
                st.session_state.roi_inputs = inputs
                st.session_state.roi_outputs = outputs
                
                st.success("✅ ROI calculated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error calculating ROI: {str(e)}")
    
    # Display results if available
    if st.session_state.roi_outputs:
        st.markdown("---")
        st.markdown("### ROI Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Annual Hours Saved",
                f"{st.session_state.roi_outputs.annual_hours_saved:,.0f}"
            )
        
        with col2:
            st.metric(
                "Annual Cost Saved",
                f"${st.session_state.roi_outputs.annual_cost_saved:,.0f}"
            )
        
        with col3:
            st.metric(
                "Net Annual Value",
                f"${st.session_state.roi_outputs.net_annual_value:,.0f}"
            )
        
        with col4:
            payback = st.session_state.roi_outputs.payback_months
            if payback != float('inf'):
                st.metric("Payback Period", f"{payback:.1f} months")
            else:
                st.metric("Payback Period", "N/A")
        
        # Save ROI Calculator
        st.markdown("---")
        company_name_for_save = st.text_input(
            "Company Name",
            value=st.session_state.account_name or "",
            placeholder="Enter company name to save ROI calculator",
            key="roi_save_company"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save ROI Calculator", use_container_width=True, type="primary"):
                if not company_name_for_save:
                    st.error("Please enter a company name.")
                else:
                    try:
                        # Save ROI calculator
                        roi_path = save_roi_calculator(
                            company_name=company_name_for_save,
                            roi_inputs=st.session_state.roi_inputs,
                            roi_outputs=st.session_state.roi_outputs,
                            gong_signals=st.session_state.gong_signals,
                            crm_context=st.session_state.crm_context
                        )
                        
                        # Auto-generate business case
                        business_case_content = generate_business_case(
                            company_name=company_name_for_save,
                            roi_inputs=st.session_state.roi_inputs,
                            roi_outputs=st.session_state.roi_outputs,
                            gong_signals=st.session_state.gong_signals,
                            crm_context=st.session_state.crm_context
                        )
                        
                        # Get version from saved ROI calculator
                        import json
                        with open(roi_path, 'r') as f:
                            roi_data = json.load(f)
                            version = roi_data.get("version", 1)
                        
                        bc_path = save_business_case(
                            company_name=company_name_for_save,
                            business_case_content=business_case_content,
                            version=version
                        )
                        
                        st.success(f"✅ ROI calculator saved! Business case draft created.")
                        st.info(f"**ROI Calculator:** `{roi_path}`\n**Business Case:** `{bc_path}`")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error saving: {str(e)}")


def render_gong_integration():
    """Render Gong transcript enrichment section."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin-bottom: 4px;">Gong Transcript Enrichment</h2>
        <p style="color: #6b7280; font-size: 14px; margin: 0;">Extract structured signals from Gong call transcripts</p>
    </div>
    """, unsafe_allow_html=True)
    
    gong_call_input = st.text_input(
        "Gong Call ID or URL",
        placeholder="Enter Gong call ID or URL",
        help="Paste a Gong call ID or full URL"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fetch_transcript = st.button("Fetch Transcript", use_container_width=True)
    
    with col2:
        if st.session_state.gong_signals:
            clear_signals = st.button("Clear Signals", use_container_width=True, type="secondary")
            if clear_signals:
                st.session_state.gong_signals = None
                st.rerun()
    
    if fetch_transcript and gong_call_input:
        try:
            with st.spinner("Fetching transcript..."):
                gong_client = GongClient()
                call_id = gong_client.extract_call_id(gong_call_input)
                transcript_data = gong_client.fetch_transcript(call_id)
                
                st.session_state.gong_transcript = transcript_data
                
                # Extract signals
                signals = gong_client.extract_signals(transcript_data)
                st.session_state.gong_signals = signals
                
                st.success("✅ Transcript fetched and signals extracted!")
                st.rerun()
        except Exception as e:
            st.error(f"Error fetching transcript: {str(e)}")
    
    # Display transcript preview
    if "gong_transcript" in st.session_state:
        with st.expander("📄 Transcript Preview", expanded=False):
            transcript = st.session_state.gong_transcript
            if "transcript" in transcript:
                if isinstance(transcript["transcript"], dict):
                    st.text(transcript["transcript"].get("text", "No transcript text available"))
                else:
                    st.text(transcript["transcript"])
    
    # Display extracted signals
    if st.session_state.gong_signals:
        st.markdown("---")
        st.markdown("### Extracted Signals")
        
        signals = st.session_state.gong_signals
        
        col1, col2 = st.columns(2)
        
        with col1:
            if signals.team_size_engineering:
                st.info(f"**Team Size:** {signals.team_size_engineering} engineers")
            
            if signals.current_tooling:
                st.info(f"**Current Tooling:** {', '.join(signals.current_tooling)}")
            
            if signals.hours_saved_per_engineer_per_week:
                st.info(f"**Hours Saved/Week:** {signals.hours_saved_per_engineer_per_week} hours")
        
        with col2:
            st.info(f"**Buying Stage:** {signals.buying_stage.title()}")
            
            if signals.pain_points:
                st.info(f"**Pain Points:** {', '.join(signals.pain_points)}")
            
            if signals.initiatives:
                st.info(f"**Initiatives:** {', '.join(signals.initiatives)}")
        
        if signals.evidence:
            with st.expander("📋 Evidence Quotes", expanded=False):
                for ev in signals.evidence:
                    st.markdown(f"**{ev.field_name}** (t={ev.timestamp_seconds or 'N/A'}s)")
                    st.markdown(f"> {ev.quote}")
                    st.markdown("")
        
        # Apply to ROI inputs
        if st.button("Apply Signals to ROI Calculator", use_container_width=True):
            if st.session_state.gong_signals:
                signals = st.session_state.gong_signals
                
                # Update ROI inputs if we have them
                if st.session_state.roi_inputs:
                    updated_inputs = ROIInputs(
                        team_size_engineering=signals.team_size_engineering or st.session_state.roi_inputs.team_size_engineering,
                        fully_loaded_cost_per_engineer=st.session_state.roi_inputs.fully_loaded_cost_per_engineer,
                        hours_saved_per_engineer_per_week=signals.hours_saved_per_engineer_per_week or st.session_state.roi_inputs.hours_saved_per_engineer_per_week,
                        adoption_rate=st.session_state.roi_inputs.adoption_rate,
                        weeks_per_year=st.session_state.roi_inputs.weeks_per_year,
                        cursor_annual_cost=st.session_state.roi_inputs.cursor_annual_cost
                    )
                    st.session_state.roi_inputs = updated_inputs
                    
                    # Recalculate ROI
                    st.session_state.roi_outputs = calculate_roi(updated_inputs)
                    st.success("✅ Signals applied to ROI calculator!")
                    st.rerun()
                else:
                    # Create new ROI inputs
                    if signals.team_size_engineering and signals.hours_saved_per_engineer_per_week:
                        new_inputs = ROIInputs(
                            team_size_engineering=signals.team_size_engineering,
                            hours_saved_per_engineer_per_week=signals.hours_saved_per_engineer_per_week,
                            cursor_annual_cost=0.0  # User will need to fill this
                        )
                        st.session_state.roi_inputs = new_inputs
                        st.success("✅ Signals applied! Please fill in remaining ROI inputs.")
                        st.rerun()
                    else:
                        st.warning("⚠️ Need team size and hours saved to apply signals.")


def render_crm_integration():
    """Render CRM enrichment section."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin-bottom: 4px;">CRM Enrichment</h2>
        <p style="color: #6b7280; font-size: 14px; margin: 0;">Pull account and contact context from HubSpot</p>
    </div>
    """, unsafe_allow_html=True)
    
    crm_account_input = st.text_input(
        "Account Name or Domain",
        placeholder="Enter company name or domain",
        help="Company name or domain to search in CRM"
    )
    
    fetch_crm = st.button("Fetch CRM Context", use_container_width=True)
    
    if fetch_crm and crm_account_input:
        try:
            with st.spinner("Fetching CRM data..."):
                crm_client = HubSpotClient()
                context = crm_client.fetch_account_context(crm_account_input)
                
                st.session_state.crm_context = context
                st.session_state.account_name = context.account_name or crm_account_input
                
                st.success("✅ CRM context fetched!")
                st.rerun()
        except Exception as e:
            st.error(f"Error fetching CRM data: {str(e)}")
    
    # Display CRM context
    if st.session_state.crm_context:
        st.markdown("---")
        st.markdown("### Source Context")
        
        context = st.session_state.crm_context
        
        col1, col2 = st.columns(2)
        
        with col1:
            if context.account_name:
                st.text(f"**Account:** {context.account_name}")
            if context.domain:
                st.text(f"**Domain:** {context.domain}")
            if context.industry:
                st.text(f"**Industry:** {context.industry}")
            if context.employee_count:
                st.text(f"**Employees:** {context.employee_count:,}")
            if context.region:
                st.text(f"**Region:** {context.region}")
        
        with col2:
            if context.opp_stage:
                st.text(f"**Opp Stage:** {context.opp_stage}")
            if context.opp_amount:
                st.text(f"**Opp Amount:** ${context.opp_amount:,.2f}")
            if context.opp_close_date:
                st.text(f"**Close Date:** {context.opp_close_date}")
        
        if context.key_contacts:
            st.markdown("**Key Contacts:**")
            for contact in context.key_contacts:
                contact_str = contact.name or "Unknown"
                if contact.title:
                    contact_str += f" ({contact.title})"
                if contact.email:
                    contact_str += f" - {contact.email}"
                st.text(f"- {contact_str}")
        
        if context.last_activity_notes:
            st.markdown("**Last Activity:**")
            st.text(context.last_activity_notes)


def render_export():
    """Render export/handoff section."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin-bottom: 4px;">Export Narrative Pack</h2>
        <p style="color: #6b7280; font-size: 14px; margin: 0;">Export structured data for narrative generation tools</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.roi_inputs or not st.session_state.roi_outputs:
        st.warning("⚠️ Please calculate ROI first before exporting.")
        return
    
    account_name = st.text_input(
        "Account Name",
        value=st.session_state.account_name or "",
        placeholder="Enter account name for export",
        help="Account name used in export filenames"
    )
    
    if st.button("Export Narrative Pack", use_container_width=True, type="primary"):
        if not account_name:
            st.error("Please enter an account name.")
            return
        
        try:
            pack = create_narrative_pack(
                roi_inputs=st.session_state.roi_inputs,
                roi_outputs=st.session_state.roi_outputs,
                gong_signals=st.session_state.gong_signals,
                crm_context=st.session_state.crm_context,
                account_name=account_name
            )
            
            json_path, markdown_path = export_narrative_pack(pack, account_name)
            
            st.success(f"✅ Narrative pack exported!")
            st.info(f"**JSON:** `{json_path}`\n**Markdown:** `{markdown_path}`")
            
            # Provide download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                with open(json_path, 'r') as f:
                    st.download_button(
                        "📥 Download JSON",
                        f.read(),
                        file_name=json_path.name,
                        mime="application/json",
                        use_container_width=True
                    )
            
            with col2:
                with open(markdown_path, 'r') as f:
                    st.download_button(
                        "📥 Download Markdown",
                        f.read(),
                        file_name=markdown_path.name,
                        mime="text/markdown",
                        use_container_width=True
                    )
        except Exception as e:
            st.error(f"Error exporting narrative pack: {str(e)}")


def render_saved_roi_calculators():
    """Render saved ROI calculators section."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin-bottom: 4px;">Saved ROI Calculators</h2>
        <p style="color: #6b7280; font-size: 14px; margin: 0;">View and manage saved ROI calculations, grouped by company</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter by company
    companies = get_companies()
    if companies:
        selected_company = st.selectbox(
            "Filter by Company",
            options=["All Companies"] + companies,
            key="roi_filter_company"
        )
    else:
        selected_company = "All Companies"
        st.info("No saved ROI calculators yet. Calculate and save an ROI to get started.")
    
    if selected_company != "All Companies":
        calculators = get_roi_calculators(selected_company)
    else:
        calculators = get_roi_calculators()
    
    if not calculators:
        if selected_company == "All Companies":
            st.info("No saved ROI calculators yet.")
        else:
            st.info(f"No ROI calculators found for {selected_company}.")
        return
    
    # Group by company
    from collections import defaultdict
    grouped = defaultdict(list)
    for calc in calculators:
        grouped[calc["company"]].append(calc)
    
    # Display grouped by company
    for company, calcs in sorted(grouped.items()):
        with st.expander(f"🏢 {company} ({len(calcs)} version{'s' if len(calcs) > 1 else ''})", expanded=False):
            for calc in sorted(calcs, key=lambda x: x["version"], reverse=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**Version {calc['version']}**")
                    st.caption(f"Created: {calc['created_at'][:10] if calc['created_at'] else 'Unknown'}")
                    if calc.get("roi_outputs"):
                        roi = calc["roi_outputs"]
                        st.text(f"Net Value: ${roi.get('net_annual_value', 0):,.0f} | Payback: {roi.get('payback_months', 0):.1f} months")
                
                with col2:
                    if st.button("📄 View", key=f"view_roi_{company}_{calc['version']}", use_container_width=True):
                        st.session_state.viewing_roi = calc["file_path"]
                        st.rerun()
                
                with col3:
                    if st.button("📥 Download", key=f"dl_roi_{company}_{calc['version']}", use_container_width=True):
                        with open(calc["file_path"], 'r') as f:
                            st.download_button(
                                "Download",
                                f.read(),
                                file_name=f"{company.replace(' ', '-')}-v{calc['version']}.json",
                                mime="application/json",
                                key=f"dl_btn_roi_{company}_{calc['version']}",
                                use_container_width=True
                            )
    
    # View selected ROI calculator
    if "viewing_roi" in st.session_state and st.session_state.viewing_roi:
        st.markdown("---")
        st.markdown("### ROI Calculator Details")
        
        try:
            data = load_roi_calculator(st.session_state.viewing_roi)
            st.json(data)
            
            if st.button("Close", key="close_roi_view"):
                del st.session_state.viewing_roi
                st.rerun()
        except Exception as e:
            st.error(f"Error loading ROI calculator: {str(e)}")


def render_saved_business_cases():
    """Render saved business cases section."""
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin-bottom: 4px;">Saved Business Cases</h2>
        <p style="color: #6b7280; font-size: 14px; margin: 0;">View and manage saved business cases, grouped by company</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter by company
    companies = get_companies()
    if companies:
        selected_company = st.selectbox(
            "Filter by Company",
            options=["All Companies"] + companies,
            key="bc_filter_company"
        )
    else:
        selected_company = "All Companies"
        st.info("No saved business cases yet. Save an ROI calculator to auto-generate a business case.")
    
    if selected_company != "All Companies":
        cases = get_business_cases(selected_company)
    else:
        cases = get_business_cases()
    
    if not cases:
        if selected_company == "All Companies":
            st.info("No saved business cases yet.")
        else:
            st.info(f"No business cases found for {selected_company}.")
        return
    
    # Group by company
    from collections import defaultdict
    grouped = defaultdict(list)
    for case in cases:
        grouped[case["company"]].append(case)
    
    # Display grouped by company
    for company, company_cases in sorted(grouped.items()):
        with st.expander(f"🏢 {company} ({len(company_cases)} version{'s' if len(company_cases) > 1 else ''})", expanded=False):
            for case in sorted(company_cases, key=lambda x: x["version"], reverse=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**Version {case['version']}**")
                    st.caption(f"Created: {case['created_at'][:10] if case['created_at'] else 'Unknown'}")
                
                with col2:
                    if st.button("📄 View", key=f"view_bc_{company}_{case['version']}", use_container_width=True):
                        st.session_state.viewing_bc = case["file_path"]
                        st.rerun()
                
                with col3:
                    if st.button("📥 Download", key=f"dl_bc_{company}_{case['version']}", use_container_width=True):
                        with open(case["file_path"], 'r', encoding='utf-8') as f:
                            st.download_button(
                                "Download",
                                f.read(),
                                file_name=f"{company.replace(' ', '-')}-v{case['version']}.md",
                                mime="text/markdown",
                                key=f"dl_btn_bc_{company}_{case['version']}",
                                use_container_width=True
                            )
    
    # View selected business case
    if "viewing_bc" in st.session_state and st.session_state.viewing_bc:
        st.markdown("---")
        st.markdown("### Business Case")
        
        try:
            content = load_business_case(st.session_state.viewing_bc)
            st.markdown(content)
            
            if st.button("Close", key="close_bc_view"):
                del st.session_state.viewing_bc
                st.rerun()
        except Exception as e:
            st.error(f"Error loading business case: {str(e)}")


def main():
    """Main app entry point."""
    st.set_page_config(
        page_title="AE Copilot - ROI & Enrichment",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown(MODERN_UI_CSS, unsafe_allow_html=True)
    
    # Load custom JavaScript and CSS
    load_custom_assets()
    
    # Header with modern styling
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("""
        <div style="
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-bottom: 16px;
        ">💼</div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <h1 style="margin-bottom: 4px;">AE Copilot</h1>
        <p style="color: #6b7280; font-size: 14px; margin: 0;">ROI Calculator • Gong Integration • CRM Enrichment</p>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sidebar for settings - Modern, clean
    with st.sidebar:
        st.markdown("""
        <div style="
            padding: 16px 0;
            border-bottom: 1px solid #e5e7eb;
            margin-bottom: 24px;
        ">
            <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #374151; text-transform: uppercase; letter-spacing: 0.05em;">
                ⚙️ Settings
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        gong_mock = st.checkbox(
            "Gong Mock Mode",
            value=os.getenv("GONG_MOCK_MODE", "false").lower() == "true",
            help="Use mock data instead of Gong API"
        )
        if gong_mock:
            os.environ["GONG_MOCK_MODE"] = "true"
        else:
            os.environ["GONG_MOCK_MODE"] = "false"
        
        crm_mock = st.checkbox(
            "CRM Mock Mode",
            value=os.getenv("CRM_MOCK_MODE", "false").lower() == "true",
            help="Use mock data instead of CRM API"
        )
        if crm_mock:
            os.environ["CRM_MOCK_MODE"] = "true"
        else:
            os.environ["CRM_MOCK_MODE"] = "false"
        
        st.markdown("""
        <div style="
            padding: 16px 0;
            border-bottom: 1px solid #e5e7eb;
            margin: 24px 0;
        ">
            <h3 style="margin: 0; font-size: 14px; font-weight: 600; color: #374151; text-transform: uppercase; letter-spacing: 0.05em;">
                🔑 API Keys
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        gong_key = st.text_input(
            "Gong Access Key",
            type="password",
            value=os.getenv("GONG_ACCESS_KEY", ""),
            help="Gong API access key"
        )
        if gong_key:
            os.environ["GONG_ACCESS_KEY"] = gong_key
        
        gong_secret = st.text_input(
            "Gong Access Secret",
            type="password",
            value=os.getenv("GONG_ACCESS_SECRET", ""),
            help="Gong API access secret"
        )
        if gong_secret:
            os.environ["GONG_ACCESS_SECRET"] = gong_secret
        
        hubspot_token = st.text_input(
            "HubSpot Private App Token",
            type="password",
            value=os.getenv("HUBSPOT_PRIVATE_APP_TOKEN", ""),
            help="HubSpot private app access token"
        )
        if hubspot_token:
            os.environ["HUBSPOT_PRIVATE_APP_TOKEN"] = hubspot_token
        
        st.markdown("""
        <div style="
            padding: 16px 0;
            border-top: 1px solid #e5e7eb;
            margin-top: 24px;
        "></div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Clear All Data", use_container_width=True, type="secondary"):
            st.session_state.roi_inputs = None
            st.session_state.roi_outputs = None
            st.session_state.gong_signals = None
            st.session_state.crm_context = None
            st.session_state.account_name = None
            if "gong_transcript" in st.session_state:
                del st.session_state.gong_transcript
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 ROI Calculator", "📞 Gong", "🏢 CRM", "📤 Export",
        "💾 Saved ROI Calculators", "📄 Saved Business Cases"
    ])
    
    with tab1:
        render_roi_calculator()
    
    with tab2:
        render_gong_integration()
    
    with tab3:
        render_crm_integration()
    
    with tab4:
        render_export()
    
    with tab5:
        render_saved_roi_calculators()
    
    with tab6:
        render_saved_business_cases()


if __name__ == "__main__":
    main()
