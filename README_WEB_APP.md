# Account Brief Generator - Web App

A Streamlit web application for generating account briefs.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web app:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## Features

- **Easy-to-use UI** - Fill in forms, click generate
- **Real-time generation** - See results instantly
- **Download markdown** - Export briefs as `.md` files
- **LLM integration** - Optional OpenAI/Anthropic support
- **Web research** - Automatic company research

## Deploying

### Option 1: Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy!

### Option 2: Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t account-brief-generator .
docker run -p 8501:8501 account-brief-generator
```

### Option 3: Heroku/Railway/Render

These platforms support Streamlit apps. See their documentation for deployment.
