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


# Custom CSS for Cursor-like appearance
CURSOR_CSS = """
<style>
    /* Main theme - Dark, clean, modern */
    .stApp {
        background: #0d1117;
        color: #c9d1d9;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #161b22;
    }
    ::-webkit-scrollbar-thumb {
        background: #30363d;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #484f58;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #161b22;
        border-right: 1px solid #21262d;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background-color: #0d1117;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1f6feb;
        box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #2ea043;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3);
    }
    
    /* Secondary buttons */
    button[kind="secondary"] {
        background-color: #21262d !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: #30363d !important;
        border-color: #484f58 !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: transparent;
        padding: 1rem 0;
    }
    
    [data-testid="stChatMessage"] {
        background-color: transparent;
    }
    
    /* User message styling */
    [data-testid="stChatMessage"][aria-label*="user"] {
        background-color: #161b22;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Assistant message styling */
    [data-testid="stChatMessage"][aria-label*="assistant"] {
        background-color: transparent;
    }
    
    /* Text areas and markdown */
    .stMarkdown {
        color: #c9d1d9;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #58a6ff;
    }
    
    .stMarkdown code {
        background-color: #161b22;
        color: #79c0ff;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
    }
    
    /* Checkboxes and selectboxes */
    .stCheckbox label, .stSelectbox label {
        color: #c9d1d9;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #21262d;
        border-radius: 6px;
    }
    
    /* Divider */
    hr {
        border-color: #21262d;
        margin: 1.5rem 0;
    }
    
    /* Titles and headers */
    h1 {
        color: #58a6ff;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #58a6ff;
        font-weight: 500;
    }
    
    h3 {
        color: #c9d1d9;
        font-weight: 500;
    }
    
    /* Chat input */
    .stChatInputContainer > div {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    
    .stChatInputContainer > div:focus-within {
        border-color: #1f6feb;
        box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.1);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #1a472a;
        border: 1px solid #238636;
        color: #3fb950;
    }
    
    .stError {
        background-color: #3d1f1f;
        border: 1px solid #da3633;
        color: #f85149;
    }
    
    .stInfo {
        background-color: #1c2128;
        border: 1px solid #30363d;
        color: #79c0ff;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background-color: #1f6feb !important;
        color: white !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #388bfd !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0d1117;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 6px 6px 0 0;
        border: 1px solid #21262d;
        color: #8b949e;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0d1117;
        color: #58a6ff;
        border-bottom-color: #0d1117;
    }
    
    /* Form styling */
    .stForm {
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #161b22;
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
    st.markdown(CURSOR_CSS, unsafe_allow_html=True)
    
    # Centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🦎 MoZilla", unsafe_allow_html=True)
        st.caption("Generate comprehensive account briefs with AI")
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
    st.markdown(CURSOR_CSS, unsafe_allow_html=True)
    
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
    st.markdown(CURSOR_CSS, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
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
    st.markdown("### 🦎 MoZilla")
    st.caption("Generate comprehensive account briefs with a conversational interface")
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
        
        if parsed["company"]:
            st.session_state.brief_data["company"] = parsed["company"]
        if parsed["persona"]:
            st.session_state.brief_data["persona"] = parsed["persona"]
        if parsed["competitors"]:
            st.session_state.brief_data["competitors"] = parsed["competitors"]
        
        if not st.session_state.brief_data["company"] and len(prompt.split()) <= 3:
            st.session_state.brief_data["company"] = prompt.strip()
        
        needs_company = not st.session_state.brief_data["company"]
        needs_persona = not st.session_state.brief_data["persona"]
        
        if needs_company:
            response = "I need a company name to generate the brief. Which company would you like me to research?"
        elif needs_persona:
            response = f"Great! I'll create a brief for **{st.session_state.brief_data['company']}**.\n\n"
            response += "**Who is the target persona?** (e.g., 'Head of Engineering', 'VP Engineering', 'Developer Experience Lead', 'Platform Lead', 'Engineering Productivity', or 'CTO')"
        elif st.session_state.brief_data["competitors"] == ["Unknown"]:
            response = f"Perfect! I have:\n- **Company:** {st.session_state.brief_data['company']}\n- **Persona:** {st.session_state.brief_data['persona']}\n\n"
            response += "**Any specific competitors to consider?** (Type 'none', 'unknown', or 'skip' to proceed without competitors, or list them separated by commas)"
        else:
            response = f"Excellent! Generating account brief for:\n\n"
            response += f"- **Company:** {st.session_state.brief_data['company']}\n"
            response += f"- **Persona:** {st.session_state.brief_data['persona']}\n"
            response += f"- **Competitors:** {', '.join(st.session_state.brief_data['competitors'])}\n\n"
            response += "🔍 Researching and generating your brief... This may take a moment.\n\n"
            brief_content = generate_brief_response()
            response += brief_content
        
        if not needs_company and not needs_persona and st.session_state.brief_data["competitors"] == ["Unknown"]:
            if any(word in prompt_lower for word in ["skip", "none", "unknown", "no", "no competitors", "n/a"]):
                response = f"Got it! Generating account brief for **{st.session_state.brief_data['company']}** (Target: {st.session_state.brief_data['persona']})...\n\n"
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
        page_title="MoZilla",
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
