"""
Streamlit web app for Account Brief Generator - Modern Cursor-like UI.
"""

import streamlit as st
import sys
from pathlib import Path
import os
import re

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.renderer import render_account_brief
from src.database import (
    create_user, authenticate_user, save_brief,
    get_user_briefs, get_brief_content, delete_brief
)


# Custom CSS for Figma-inspired dark appearance
CURSOR_DARK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main theme - Figma-inspired dark */
    .stApp {
        background: #1a1a1a;
        color: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth transitions everywhere */
    * {
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Custom scrollbar - Figma style */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: #2d2d2d;
        border-radius: 5px;
        border: 2px solid #1a1a1a;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3d3d3d;
    }
    
    /* Sidebar styling - Figma panel style */
    .css-1d391kg {
        background-color: #1f1f1f;
        border-right: 1px solid #2d2d2d;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Input fields - Figma input style */
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #3d3d3d;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 14px;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #18a0fb;
        box-shadow: 0 0 0 2px rgba(24, 160, 251, 0.2);
        outline: none;
        background-color: #2d2d2d;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6b6b6b;
    }
    
    /* Buttons - Figma primary button style */
    .stButton > button {
        background: linear-gradient(135deg, #18a0fb 0%, #0d8ce8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 4px rgba(24, 160, 251, 0.2);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1ba8ff 0%, #0e95f5 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(24, 160, 251, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(24, 160, 251, 0.2);
    }
    
    /* Secondary buttons - Figma secondary style */
    button[kind="secondary"] {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 1px solid #3d3d3d !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: #3d3d3d !important;
        border-color: #4d4d4d !important;
        transform: translateY(-1px);
    }
    
    /* Chat messages - Figma card style */
    .stChatMessage {
        background-color: transparent;
        padding: 12px 0;
    }
    
    [data-testid="stChatMessage"] {
        background-color: transparent;
    }
    
    /* User message styling - Elevated card */
    [data-testid="stChatMessage"][aria-label*="user"] {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Assistant message styling */
    [data-testid="stChatMessage"][aria-label*="assistant"] {
        background-color: transparent;
    }
    
    /* Text areas and markdown - Figma typography */
    .stMarkdown {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #ffffff;
        font-weight: 600;
        letter-spacing: -0.02em;
        font-family: 'Inter', sans-serif;
    }
    
    .stMarkdown h1 {
        font-size: 28px;
        line-height: 1.2;
        margin-bottom: 12px;
    }
    
    .stMarkdown h2 {
        font-size: 20px;
        line-height: 1.3;
        margin-bottom: 10px;
    }
    
    .stMarkdown h3 {
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    .stMarkdown code {
        background-color: #2d2d2d;
        color: #18a0fb;
        padding: 3px 8px;
        border-radius: 6px;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
        font-size: 13px;
        border: 1px solid #3d3d3d;
    }
    
    .stMarkdown p {
        margin-bottom: 12px;
        color: #e0e0e0;
    }
    
    /* Checkboxes and selectboxes */
    .stCheckbox label, .stSelectbox label {
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
    }
    
    /* Expander styling - Figma accordion */
    .streamlit-expanderHeader {
        background-color: #2d2d2d;
        color: #ffffff;
        border: 1px solid #3d3d3d;
        border-radius: 8px;
        padding: 12px 16px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #3d3d3d;
        border-color: #4d4d4d;
    }
    
    /* Divider - Figma separator */
    hr {
        border: none;
        border-top: 1px solid #2d2d2d;
        margin: 24px 0;
    }
    
    /* Titles and headers - Figma typography */
    h1 {
        color: #ffffff;
        font-weight: 600;
        letter-spacing: -0.02em;
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        line-height: 1.2;
    }
    
    h2 {
        color: #ffffff;
        font-weight: 600;
        letter-spacing: -0.01em;
        font-family: 'Inter', sans-serif;
        font-size: 20px;
    }
    
    h3 {
        color: #ffffff;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
    }
    
    /* Chat input - Figma input style */
    .stChatInputContainer > div {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 12px;
        padding: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stChatInputContainer > div:focus-within {
        border-color: #18a0fb;
        box-shadow: 0 0 0 2px rgba(24, 160, 251, 0.2), 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Success/Error messages - Figma toast style */
    .stSuccess {
        background-color: #1a3a2a;
        border: 1px solid #2d5a3d;
        color: #4ade80;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stError {
        background-color: #3a1a1a;
        border: 1px solid #5a2d2d;
        color: #f87171;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stInfo {
        background-color: #1a2a3a;
        border: 1px solid #2d3d5a;
        color: #60a5fa;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #18a0fb 0%, #0d8ce8 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 2px 4px rgba(24, 160, 251, 0.2) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1ba8ff 0%, #0e95f5 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(24, 160, 251, 0.3) !important;
    }
    
    /* Tabs - Figma tab style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #1a1a1a;
        border-bottom: 1px solid #2d2d2d;
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        border-radius: 8px 8px 0 0;
        color: #8b8b8b;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #18a0fb;
        border-bottom: 2px solid #18a0fb;
        font-weight: 600;
    }
    
    /* Form styling - Figma card */
    .stForm {
        border: 1px solid #2d2d2d;
        border-radius: 12px;
        padding: 24px;
        background-color: #1f1f1f;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Selectbox - Figma dropdown */
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 8px;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #18a0fb;
        box-shadow: 0 0 0 2px rgba(24, 160, 251, 0.2);
    }
    
    /* Main container spacing */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Caption styling */
    .stMarkdown p.caption {
        color: #8b8b8b;
        font-size: 13px;
        margin-top: 4px;
    }
    </style>
"""

# Custom CSS for Figma-inspired light mode
CURSOR_LIGHT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main theme - Figma-inspired light */
    .stApp {
        background: #ffffff;
        color: #1a1a1a;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth transitions everywhere */
    * {
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Custom scrollbar - Figma style */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #f5f5f5;
    }
    ::-webkit-scrollbar-thumb {
        background: #d0d0d0;
        border-radius: 5px;
        border: 2px solid #ffffff;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #b0b0b0;
    }
    
    /* Sidebar styling - Figma panel style */
    .css-1d391kg {
        background-color: #fafafa;
        border-right: 1px solid #e5e5e5;
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Input fields - Figma input style */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1a1a1a;
        border: 1px solid #d0d0d0;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 14px;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #18a0fb;
        box-shadow: 0 0 0 2px rgba(24, 160, 251, 0.15);
        outline: none;
        background-color: #ffffff;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #8b8b8b;
    }
    
    /* Buttons - Figma primary button style */
    .stButton > button {
        background: linear-gradient(135deg, #18a0fb 0%, #0d8ce8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 2px 4px rgba(24, 160, 251, 0.2);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1ba8ff 0%, #0e95f5 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(24, 160, 251, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(24, 160, 251, 0.2);
    }
    
    /* Secondary buttons - Figma secondary style */
    button[kind="secondary"] {
        background-color: #f5f5f5 !important;
        color: #1a1a1a !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: #e8e8e8 !important;
        border-color: #b0b0b0 !important;
        transform: translateY(-1px);
    }
    
    /* Chat messages - Figma card style */
    .stChatMessage {
        background-color: transparent;
        padding: 12px 0;
    }
    
    [data-testid="stChatMessage"] {
        background-color: transparent;
    }
    
    /* User message styling - Elevated card */
    [data-testid="stChatMessage"][aria-label*="user"] {
        background-color: #fafafa;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Assistant message styling */
    [data-testid="stChatMessage"][aria-label*="assistant"] {
        background-color: transparent;
    }
    
    /* Text areas and markdown - Figma typography */
    .stMarkdown {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1a1a1a;
        font-weight: 600;
        letter-spacing: -0.02em;
        font-family: 'Inter', sans-serif;
    }
    
    .stMarkdown h1 {
        font-size: 28px;
        line-height: 1.2;
        margin-bottom: 12px;
    }
    
    .stMarkdown h2 {
        font-size: 20px;
        line-height: 1.3;
        margin-bottom: 10px;
    }
    
    .stMarkdown h3 {
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    .stMarkdown code {
        background-color: #f5f5f5;
        color: #18a0fb;
        padding: 3px 8px;
        border-radius: 6px;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
        font-size: 13px;
        border: 1px solid #e5e5e5;
    }
    
    .stMarkdown p {
        margin-bottom: 12px;
        color: #4a4a4a;
    }
    
    /* Checkboxes and selectboxes */
    .stCheckbox label, .stSelectbox label {
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
    }
    
    /* Expander styling - Figma accordion */
    .streamlit-expanderHeader {
        background-color: #fafafa;
        color: #1a1a1a;
        border: 1px solid #e5e5e5;
        border-radius: 8px;
        padding: 12px 16px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f5f5f5;
        border-color: #d0d0d0;
    }
    
    /* Divider - Figma separator */
    hr {
        border: none;
        border-top: 1px solid #e5e5e5;
        margin: 24px 0;
    }
    
    /* Titles and headers - Figma typography */
    h1 {
        color: #1a1a1a;
        font-weight: 600;
        letter-spacing: -0.02em;
        font-family: 'Inter', sans-serif;
        font-size: 28px;
        line-height: 1.2;
    }
    
    h2 {
        color: #1a1a1a;
        font-weight: 600;
        letter-spacing: -0.01em;
        font-family: 'Inter', sans-serif;
        font-size: 20px;
    }
    
    h3 {
        color: #1a1a1a;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
    }
    
    /* Chat input - Figma input style */
    .stChatInputContainer > div {
        background-color: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stChatInputContainer > div:focus-within {
        border-color: #18a0fb;
        box-shadow: 0 0 0 2px rgba(24, 160, 251, 0.15), 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Success/Error messages - Figma toast style */
    .stSuccess {
        background-color: #e8f5e9;
        border: 1px solid #81c784;
        color: #2e7d32;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .stError {
        background-color: #ffebee;
        border: 1px solid #ef5350;
        color: #c62828;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .stInfo {
        background-color: #e3f2fd;
        border: 1px solid #64b5f6;
        color: #1565c0;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #18a0fb 0%, #0d8ce8 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 2px 4px rgba(24, 160, 251, 0.2) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1ba8ff 0%, #0e95f5 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(24, 160, 251, 0.3) !important;
    }
    
    /* Tabs - Figma tab style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background-color: #ffffff;
        border-bottom: 1px solid #e5e5e5;
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        border-radius: 8px 8px 0 0;
        color: #8b8b8b;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #fafafa;
        color: #1a1a1a;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #18a0fb;
        border-bottom: 2px solid #18a0fb;
        font-weight: 600;
    }
    
    /* Form styling - Figma card */
    .stForm {
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 24px;
        background-color: #fafafa;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Selectbox - Figma dropdown */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 1px solid #d0d0d0;
        border-radius: 8px;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #18a0fb;
        box-shadow: 0 0 0 2px rgba(24, 160, 251, 0.15);
    }
    
    /* Main container spacing */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Caption styling */
    .stMarkdown p.caption {
        color: #8b8b8b;
        font-size: 13px;
        margin-top: 4px;
    }
</style>
"""


# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "chat"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "brief_data" not in st.session_state:
    st.session_state.brief_data = {
        "company": None,
        "persona": None,
        "competitors": ["Unknown"],
        "use_research": True,
        "use_llm": False,
        "llm_provider": "openai"
    }
if "brief_generated" not in st.session_state:
    st.session_state.brief_generated = False
if "current_brief" not in st.session_state:
    st.session_state.current_brief = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode


def format_persona_title(persona: str) -> str:
    """Format persona title consistently (Title Case)."""
    if not persona:
        return persona
    
    # Common titles that should be uppercase
    title_case_map = {
        'vp': 'VP',
        'cto': 'CTO',
        'cfo': 'CFO',
        'ceo': 'CEO',
        'cio': 'CIO'
    }
    
    # Split and format each word
    words = persona.split()
    formatted_words = []
    
    for i, word in enumerate(words):
        word_lower = word.lower()
        
        # Handle special cases
        if word_lower in title_case_map:
            formatted_words.append(title_case_map[word_lower])
        elif word_lower in ['of', 'the', 'a', 'an', 'and'] and i > 0:
            # Keep prepositions lowercase (except at start)
            formatted_words.append(word_lower)
        else:
            # Capitalize first letter, rest lowercase
            formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words)


def format_company_name(company: str) -> str:
    """Format company name consistently (Title Case)."""
    if not company:
        return company
    
    # Common company suffixes/prefixes that might need special handling
    # For now, just do proper Title Case
    words = company.split()
    formatted_words = []
    
    for word in words:
        # Capitalize first letter, rest lowercase
        formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words)


def parse_user_input(text: str) -> dict:
    """Parse user input to extract company, persona, and competitors."""
    text_lower = text.lower()
    extracted = {"company": None, "persona": None, "competitors": None}
    
    persona_patterns = [
        r"(?:head of|vp of|vice president of|director of)\s+engineering",
        r"vp engineering",
        r"developer experience lead",
        r"platform lead",
        r"engineering productivity",
        r"\bcto\b",
        r"chief technology officer"
    ]
    
    for pattern in persona_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            words = text.split()
            for i, word in enumerate(words):
                if word.lower() in match.group().lower():
                    if i + 2 < len(words):
                        extracted["persona"] = " ".join(words[i:i+3]).title()
                    elif i + 1 < len(words):
                        extracted["persona"] = " ".join(words[i:i+2]).title()
                    else:
                        extracted["persona"] = words[i].title()
                    break
            if not extracted["persona"]:
                extracted["persona"] = match.group().title()
            break
    
    competitor_keywords = ["competitor", "vs", "versus", "compared to", "against"]
    for keyword in competitor_keywords:
        if keyword in text_lower:
            idx = text_lower.find(keyword)
            after = text[idx + len(keyword):].strip()
            competitors = re.split(r'[,;]|and\s+', after)
            competitors = [c.strip() for c in competitors if c.strip() and len(c.strip()) > 2]
            if competitors:
                extracted["competitors"] = competitors
            break
    
    words = text.split()
    if words:
        skip_words = ["generate", "create", "brief", "for", "at", "the", "a", "an", "to", "about"]
        company_words = [w for w in words if w.lower() not in skip_words]
        if company_words:
            if len(company_words) >= 1:
                extracted["company"] = company_words[0]
            if len(company_words) >= 2 and not extracted["persona"]:
                extracted["company"] = " ".join(company_words[:2])
    
    return extracted


def generate_brief_response():
    """Generate the account brief and return it."""
    try:
        brief = render_account_brief(
            company=st.session_state.brief_data["company"],
            persona=st.session_state.brief_data["persona"],
            competitors=st.session_state.brief_data["competitors"],
            use_research=st.session_state.brief_data["use_research"],
            use_llm=st.session_state.brief_data["use_llm"],
            llm_provider=st.session_state.brief_data["llm_provider"]
        )
        st.session_state.brief_generated = True
        st.session_state.current_brief = brief
        return brief
    except Exception as e:
        error_msg = f"❌ Error generating brief: {str(e)}\n\nPlease try again or check your API keys if using LLM features."
        st.session_state.current_brief = None
        return error_msg


def show_login_page():
    """Show login/register page with modern design."""
    # Apply theme CSS
    css = CURSOR_DARK_CSS if st.session_state.dark_mode else CURSOR_LIGHT_CSS
    st.markdown(css, unsafe_allow_html=True)
    
    # Centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Theme toggle on login page
        col_theme1, col_theme2 = st.columns([3, 1])
        with col_theme2:
            theme_icon = "🌙" if st.session_state.dark_mode else "☀️"
            theme_label = "Dark" if st.session_state.dark_mode else "Light"
            if st.button(f"{theme_icon} {theme_label}", use_container_width=True, type="secondary", key="theme_toggle_login"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        
        st.markdown("### 🦎 MoZilla GTM Account Brief Generator", unsafe_allow_html=True)
        st.caption("Generate comprehensive account briefs with AI")
        cursor_color = "#58a6ff" if st.session_state.dark_mode else "#0969da"
        st.markdown(f'<p style="font-size: 0.85em; color: #8b949e; margin-top: 1rem;">Made with <a href="https://cursor.sh" style="color: {cursor_color}; text-decoration: none;">Cursor</a></p>', unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username", key="login_username")
                password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
                submit = st.form_submit_button("Login", use_container_width=True, type="primary")
                
                if submit:
                    if not username or not password:
                        st.error("Please enter both username and password")
                    else:
                        user_id = authenticate_user(username, password)
                        if user_id:
                            st.session_state.authenticated = True
                            st.session_state.user_id = user_id
                            st.session_state.username = username
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("Username", placeholder="Choose a username", key="reg_username")
                new_password = st.text_input("Password", type="password", placeholder="Choose a password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="reg_confirm")
                submit = st.form_submit_button("Create Account", use_container_width=True, type="primary")
                
                if submit:
                    if not new_username or not new_password:
                        st.error("Please enter both username and password")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 4:
                        st.error("Password must be at least 4 characters long")
                    else:
                        success = create_user(new_username, new_password)
                        if success:
                            st.success("Account created successfully! Please login.")
                        else:
                            st.error("Username already exists. Please choose a different username.")


def show_saved_briefs_page():
    """Show saved briefs page with modern design."""
    # Apply theme CSS
    css = CURSOR_DARK_CSS if st.session_state.dark_mode else CURSOR_LIGHT_CSS
    st.markdown(css, unsafe_allow_html=True)
    
    st.markdown("### 📚 My Saved Briefs")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back", type="secondary", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()
    
    st.markdown("---")
    
    briefs = get_user_briefs(st.session_state.user_id)
    
    if not briefs:
        st.info("💡 You haven't saved any briefs yet. Generate a brief in the chat and save it!")
        return
    
    st.markdown(f"**{len(briefs)}** saved brief(s)")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for brief in briefs:
        with st.expander(f"📄 {brief['title']} • {brief['created_at'][:10]}", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Company:** `{brief['company']}`")
                st.markdown(f"**Persona:** `{brief['persona']}`")
                st.markdown(f"**Competitors:** `{', '.join(brief['competitors'])}`")
                st.caption(f"Created: {brief['created_at']}")
            
            with col2:
                if st.button("View", key=f"view_{brief['id']}", use_container_width=True):
                    brief_content = get_brief_content(brief['id'], st.session_state.user_id)
                    if brief_content:
                        st.session_state.viewing_brief = brief_content
                        st.session_state.viewing_brief_title = brief['title']
                
                if st.button("Delete", key=f"delete_{brief['id']}", use_container_width=True, type="secondary"):
                    if delete_brief(brief['id'], st.session_state.user_id):
                        st.rerun()
    
    if "viewing_brief" in st.session_state and st.session_state.viewing_brief:
        st.markdown("---")
        st.markdown(f"### 📄 {st.session_state.viewing_brief_title}")
        st.markdown(st.session_state.viewing_brief)
        
        st.download_button(
            label="📥 Download Brief",
            data=st.session_state.viewing_brief,
            file_name=f"{st.session_state.viewing_brief_title.replace(' ', '-')}.md",
            mime="text/markdown",
            use_container_width=True
        )


def show_chat_page():
    """Show main chat interface with modern design."""
    # Apply theme CSS
    css = CURSOR_DARK_CSS if st.session_state.dark_mode else CURSOR_LIGHT_CSS
    st.markdown(css, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        
        # Theme toggle
        theme_icon = "🌙" if st.session_state.dark_mode else "☀️"
        theme_label = "Dark Mode" if st.session_state.dark_mode else "Light Mode"
        if st.button(f"{theme_icon} {theme_label}", use_container_width=True, type="secondary"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.messages = []
            st.session_state.brief_data = {
                "company": None,
                "persona": None,
                "competitors": ["Unknown"],
                "use_research": True,
                "use_llm": False,
                "llm_provider": "openai"
            }
            st.session_state.brief_generated = False
            st.session_state.current_brief = None
            st.rerun()
        
        st.markdown("---")
        
        if st.button("📚 Saved Briefs", use_container_width=True):
            st.session_state.page = "saved"
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        st.session_state.brief_data["use_research"] = st.checkbox(
            "Enable Web Research",
            value=st.session_state.brief_data["use_research"],
            help="Use web research to populate brief"
        )
        
        st.session_state.brief_data["use_llm"] = st.checkbox(
            "Enable LLM Research",
            value=st.session_state.brief_data["use_llm"],
            help="Use LLM for enhanced content"
        )
        
        if st.session_state.brief_data["use_llm"]:
            st.session_state.brief_data["llm_provider"] = st.selectbox(
                "LLM Provider",
                options=["openai", "anthropic"],
                index=0 if st.session_state.brief_data["llm_provider"] == "openai" else 1
            )
            
            if st.session_state.brief_data["llm_provider"] == "openai":
                api_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    value=os.getenv("OPENAI_API_KEY", "")
                )
                if api_key:
                    os.environ["OPENAI_API_KEY"] = api_key
            elif st.session_state.brief_data["llm_provider"] == "anthropic":
                api_key = st.text_input(
                    "Anthropic API Key",
                    type="password",
                    value=os.getenv("ANTHROPIC_API_KEY", "")
                )
                if api_key:
                    os.environ["ANTHROPIC_API_KEY"] = api_key
        
        st.markdown("---")
        
        if st.button("🗑️ New Brief", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.brief_data = {
                "company": None,
                "persona": None,
                "competitors": ["Unknown"],
                "use_research": st.session_state.brief_data["use_research"],
                "use_llm": st.session_state.brief_data["use_llm"],
                "llm_provider": st.session_state.brief_data["llm_provider"]
            }
            st.session_state.brief_generated = False
            st.session_state.current_brief = None
            st.rerun()
    
    # Main content area
    st.markdown("### 🦎 MoZilla GTM Account Brief Generator")
    st.caption("Generate comprehensive account briefs with a conversational interface")
    cursor_color = "#58a6ff" if st.session_state.dark_mode else "#0969da"
    st.markdown(f'<p style="font-size: 0.85em; color: #8b949e;">Made with <a href="https://cursor.sh" style="color: {cursor_color}; text-decoration: none;">Cursor</a></p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Welcome message
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            welcome = "👋 Hi! I can help you generate account briefs for outbound outreach.\n\n"
            welcome += "**To get started, simply tell me:**\n"
            welcome += "- A company name (e.g., 'Ramp')\n\n"
            welcome += "Or provide everything at once:\n"
            welcome += "- *'Generate brief for Ramp, targeting Head of Engineering, competitors GitHub Copilot and Windsurf'*"
            st.markdown(welcome)
    
    # Chat input
    if prompt := st.chat_input("Enter a company name or request a brief..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        parsed = parse_user_input(prompt)
        prompt_lower = prompt.lower().strip()
        
        # Update brief data from parsed input (only if we don't already have that field)
        if parsed["company"] and not st.session_state.brief_data["company"]:
            st.session_state.brief_data["company"] = format_company_name(parsed["company"])
        if parsed["persona"] and not st.session_state.brief_data["persona"]:
            st.session_state.brief_data["persona"] = format_persona_title(parsed["persona"])
        if parsed["competitors"] and st.session_state.brief_data["competitors"] == ["Unknown"]:
            # Format competitors consistently
            formatted_competitors = [format_company_name(c.strip()) for c in parsed["competitors"] if c.strip()]
            st.session_state.brief_data["competitors"] = formatted_competitors
        
        # Fallback: if we don't have company and prompt looks like a company name
        if not st.session_state.brief_data["company"] and len(prompt.split()) <= 3 and not parsed["persona"]:
            st.session_state.brief_data["company"] = format_company_name(prompt.strip())
        
        # Check what we still need
        needs_company = not st.session_state.brief_data["company"]
        needs_persona = not st.session_state.brief_data["persona"]
        needs_competitors = st.session_state.brief_data["competitors"] == ["Unknown"]
        
        # Determine response based on what we need
        if needs_company:
            response = "I need a company name to generate the brief. Which company would you like me to research?"
        elif needs_persona:
            # Handle skip words for persona (in case user wants to skip)
            if any(word in prompt_lower for word in ["skip", "none", "unknown"]):
                response = "I need a target persona to generate the brief. Please provide the role (e.g., 'Head of Engineering', 'VP Engineering', 'CTO')."
            else:
                response = f"Great! I'll create a brief for **{st.session_state.brief_data['company']}**.\n\n"
                response += "**Who is the target persona?** (e.g., 'Head of Engineering', 'VP Engineering', 'Developer Experience Lead', 'Platform Lead', 'Engineering Productivity', or 'CTO')"
        elif needs_competitors:
            # Check if user wants to skip competitors
            if any(word in prompt_lower for word in ["skip", "none", "unknown", "no", "no competitors", "n/a"]):
                # User wants to skip competitors - generate brief now
                response = f"Got it! Generating account brief for **{st.session_state.brief_data['company']}** (Target: {st.session_state.brief_data['persona']})...\n\n"
                brief_content = generate_brief_response()
                response += brief_content
            else:
                # Ask about competitors
                response = f"Perfect! I have:\n- **Company:** {st.session_state.brief_data['company']}\n- **Persona:** {st.session_state.brief_data['persona']}\n\n"
                response += "**Any specific competitors to consider?** (Type 'none', 'unknown', or 'skip' to proceed without competitors, or list them separated by commas)"
        else:
            # We have everything - generate the brief
            response = f"Excellent! Generating account brief for:\n\n"
            response += f"- **Company:** {st.session_state.brief_data['company']}\n"
            response += f"- **Persona:** {st.session_state.brief_data['persona']}\n"
            response += f"- **Competitors:** {', '.join(st.session_state.brief_data['competitors'])}\n\n"
            response += "🔍 Researching and generating your brief... This may take a moment.\n\n"
            brief_content = generate_brief_response()
            response += brief_content
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # Download and Save buttons
    if st.session_state.brief_generated and st.session_state.current_brief:
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download Brief",
                data=st.session_state.current_brief,
                file_name=f"{st.session_state.brief_data['company'].replace(' ', '-')}-account-brief.md",
                mime="text/markdown",
                use_container_width=True,
                key="download_brief"
            )
        
        with col2:
            if st.button("💾 Save Brief", use_container_width=True, type="primary"):
                try:
                    save_brief(
                        user_id=st.session_state.user_id,
                        company=st.session_state.brief_data["company"],
                        persona=st.session_state.brief_data["persona"],
                        competitors=st.session_state.brief_data["competitors"],
                        brief_content=st.session_state.current_brief
                    )
                    st.success("✅ Brief saved successfully!")
                except Exception as e:
                    st.error(f"Error saving brief: {str(e)}")


def main():
    st.set_page_config(
        page_title="MoZilla GTM Account Brief Generator",
        page_icon="🦎",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        if st.session_state.page == "saved":
            show_saved_briefs_page()
        else:
            show_chat_page()


if __name__ == "__main__":
    main()
