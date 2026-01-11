# AE Copilot - ROI Calculator & Enrichment Tool

A Streamlit app focused on structured enrichment and ROI calculation for Account Executives at Cursor. This tool helps AEs prepare for calls by calculating ROI, extracting signals from Gong transcripts, and enriching account data from CRM systems.

## Features

### 1. ROI Calculator
- **Deterministic calculations** - No LLM required
- Inputs: Team size, fully loaded cost, hours saved, adoption rate, weeks per year, Cursor cost
- Outputs: Annual hours saved, annual cost saved, net annual value, payback period

### 2. Gong Integration
- Fetch call transcripts by call ID or URL
- Extract structured signals with evidence:
  - Team size (engineering)
  - Current tooling
  - Hours saved per engineer per week (only if explicitly stated)
  - Pain points
  - Initiatives
  - Buying stage
- Apply extracted signals to ROI calculator

### 3. CRM Enrichment (HubSpot)
- Fetch account context by name or domain
- Pull account information: name, domain, industry, employee count, region
- Retrieve key contacts: name, title, email
- Get opportunity data: stage, amount, close date
- View last activity notes

### 4. Export/Handoff to Narrative
- Export "Narrative Pack" as JSON and Markdown
- Contains all ROI inputs/outputs, Gong signals, and CRM context
- Ready for consumption by narrative generation tools
- Files saved to `outputs/<account>_context.json` and `outputs/<account>_context.md`

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables (optional):**
```bash
# Gong API (or use mock mode)
export GONG_BASE_URL="https://api.gong.io"
export GONG_ACCESS_KEY="your-access-key"
export GONG_ACCESS_SECRET="your-access-secret"

# HubSpot CRM (or use mock mode)
export HUBSPOT_PRIVATE_APP_TOKEN="your-private-app-token"

# Mock modes (for testing without API access)
export GONG_MOCK_MODE="true"
export CRM_MOCK_MODE="true"
```

## Usage

### Run the Streamlit app:
```bash
streamlit run ae_copilot_app.py
```

Then open your browser to `http://localhost:8501`

### Workflow:

1. **Calculate ROI:**
   - Fill in ROI inputs (team size, costs, hours saved, etc.)
   - Click "Calculate ROI" to see results

2. **Enrich with Gong:**
   - Enter a Gong call ID or URL
   - Click "Fetch Transcript"
   - Review extracted signals
   - Optionally click "Apply Signals to ROI Calculator" to auto-fill ROI inputs

3. **Enrich with CRM:**
   - Enter account name or domain
   - Click "Fetch CRM Context"
   - Review account and contact information

4. **Export Narrative Pack:**
   - Enter account name
   - Click "Export Narrative Pack"
   - Download JSON and Markdown files for use in narrative generation tools

## Mock Mode

For testing without API access, enable mock mode in the sidebar:
- **Gong Mock Mode**: Uses sample transcript from `data/sample_transcript.json`
- **CRM Mock Mode**: Uses sample CRM data from `data/sample_crm.json`

## Project Structure

```
src/
  schemas.py          # Pydantic models for all data structures
  roi_calculator.py   # ROI calculation logic
  gong_client.py      # Gong API client and signal extraction
  crm_client.py       # CRM client (HubSpot, with interface for Salesforce)
  export.py           # Narrative pack export functionality

data/
  sample_transcript.json  # Mock Gong transcript
  sample_crm.json         # Mock CRM data

ae_copilot_app.py    # Main Streamlit app
```

## Design Decisions

- **No narrative generation**: This app focuses on structured data only. Narrative generation happens in separate tools that consume the exported "Narrative Pack".
- **Modular architecture**: Each component (ROI, Gong, CRM, Export) is independent and can be extended.
- **Mock mode**: Allows testing and demos without API credentials.
- **Evidence-based extraction**: Gong signals include evidence quotes with timestamps - never invent numbers.
- **HubSpot first**: Implemented HubSpot for MVP, but designed with abstract `CRMClient` interface for easy Salesforce addition.

## Future Enhancements

- Salesforce CRM integration
- Enhanced signal extraction using LLM (optional)
- Batch processing for multiple accounts
- Integration with narrative generation tools
