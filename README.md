# AE Copilot 💼

A modern Streamlit application for Account Executives at Cursor. Calculate ROI, enrich data from Gong transcripts, integrate with CRM systems, and generate business cases - all in one beautiful, Superhuman-inspired interface.

## ✨ Features

### 🧮 ROI Calculator
- **Deterministic calculations** - No LLM required
- Calculate developer productivity ROI for Cursor
- Inputs: Team size, costs, hours saved, adoption rate
- Outputs: Annual savings, net value, payback period

### 📞 Gong Integration
- Fetch call transcripts by ID or URL
- Extract structured signals with evidence:
  - Team size, current tooling, pain points
  - Hours saved (only if explicitly stated)
  - Buying stage, initiatives
- Apply extracted values to ROI calculator

### 🏢 CRM Enrichment (HubSpot)
- Fetch account context by name or domain
- Pull account information, contacts, opportunities
- View last activity notes
- Modular design - easy to add Salesforce

### 📄 Business Case Generator
- Auto-generates one-pager business cases
- Includes detailed ROI analysis in appendix
- Versioned storage grouped by company
- Ready for stakeholder review

### 💾 Storage & Versioning
- Save ROI calculators with versioning
- Auto-generate business case drafts
- Group by company name
- View and manage all versions

### 📤 Export/Handoff
- Export "Narrative Pack" as JSON + Markdown
- Contains all ROI data, Gong signals, CRM context
- Ready for consumption by narrative generation tools

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/MohamedNSoliman/ae-copilot.git
cd ae-copilot

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run ae_copilot_app.py
```

### Environment Variables (Optional)

```bash
# Gong API
export GONG_BASE_URL="https://api.gong.io"
export GONG_ACCESS_KEY="your-access-key"
export GONG_ACCESS_SECRET="your-access-secret"

# HubSpot CRM
export HUBSPOT_PRIVATE_APP_TOKEN="your-private-app-token"

# Mock modes (for testing without API access)
export GONG_MOCK_MODE="true"
export CRM_MOCK_MODE="true"
```

## 🎨 UI Features

- **Superhuman/Grammarly/ChatGPT-inspired design**
- **Keyboard shortcuts** - Press `Cmd+K` (or `Ctrl+K`) for command palette
- **Smooth animations** and transitions
- **Modern, clean interface** with gradient accents
- **Responsive layout** optimized for productivity

## 📁 Project Structure

```
ae-copilot/
├── ae_copilot_app.py          # Main Streamlit app
├── src/
│   ├── schemas.py              # Pydantic data models
│   ├── roi_calculator.py       # ROI calculation logic
│   ├── gong_client.py          # Gong API client
│   ├── crm_client.py           # CRM client (HubSpot)
│   ├── business_case.py        # Business case generator
│   ├── export.py               # Narrative pack export
│   └── storage.py              # Versioned storage
├── data/
│   ├── sample_transcript.json  # Mock Gong transcript
│   └── sample_crm.json         # Mock CRM data
├── outputs/
│   ├── roi_calculators/        # Saved ROI calculators
│   └── business_cases/         # Saved business cases
├── scripts/
│   ├── setup_github.sh         # GitHub setup automation
│   └── push_to_github.sh       # Automated push script
└── static/
    ├── js/
    │   └── enhancements.js     # JavaScript enhancements
    └── css/
        └── custom.css           # Additional CSS
```

## 🔄 GitHub Automation

### Initial Setup
```bash
chmod +x scripts/*.sh
./scripts/setup_github.sh
```

### Push Changes
```bash
./scripts/push_to_github.sh "Your commit message"
```

See [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed instructions.

## 🌐 Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Set main file: `ae_copilot_app.py`
5. Add secrets for API keys (optional)

## 📚 Documentation

- [README_AE_COPILOT.md](README_AE_COPILOT.md) - Detailed feature documentation
- [GITHUB_SETUP.md](GITHUB_SETUP.md) - GitHub setup and automation guide
- [LANGUAGES_GUIDE.md](LANGUAGES_GUIDE.md) - Languages to learn for enhancement

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** - Web framework
- **Pydantic** - Data validation
- **SQLite** - Local storage (via storage module)
- **JavaScript/CSS** - UI enhancements

## 🔐 Security

- API keys stored in environment variables
- `.gitignore` excludes secrets and sensitive data
- Sample data files are safe to commit
- Never commit `.env` files or API keys

## 📝 License

This project is private and proprietary.

## 👤 Author

Mohamed N. Soliman

## 🙏 Acknowledgments

- Inspired by Superhuman, Grammarly, and ChatGPT UI/UX
- Built with Streamlit
- Designed for Account Executives at Cursor

---

**Made with 💜 for AEs who want to move fast and close deals**
