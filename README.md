# Email Summary API

**AI-powered email summaries** FastAPI + Ollama (Mistral) + Gmail API

## ⚡ Quick Start

1. **Prep Credentials**

   - Get `client_secret.json` from [Google Cloud Console](https://console.cloud.google.com/ "null") → Save to `/env`

2. **Install**

   ```bash
   uv init .              # Initialize the project using uv
   uv venv                # Create a virtual environment
   uv install .           # Install project dependencies
   ollama pull mistral    # Get AI model

   ```

3. **Run**

   ```bash
   fastapi dev main.py
   ```

   Docs: http://localhost:8000/docs

   ![Screenshot from 2025-03-20 22-35-48](https://github.com/user-attachments/assets/69e3bdac-9550-4893-87ab-5c70b9442e89)


## 🔐 Security

- Tokens stored in `/env` (gitignored)

- Read-only Gmail access

- Local AI processing (no data leaves your machine)

## 💻 Basic Usage

**Get summaries**

```bash
curl http://localhost:8000/emails/summarized?max_results=3
```

**Output**

```json
[
  {
    "sender": "boss@company.com",
    "subject": "Team Meeting",
    "date": "2024-03-15T12:00:00",
    "summary": "Team meeting moved to Friday..."
  },
  {
    "sender": "colleague@company.com",
    "subject": "Project Update",
    "date": "2024-03-14T10:30:00",
    "summary": "Project is on track, next steps are..."
  },
  {
    "sender": "client@company.com",
    "subject": "Invoice Due",
    "date": "2024-03-13T16:00:00",
    "summary": "Invoice #1234 is due on 2024-03-20"
  }
]
```

## ❗ Troubleshoot

| **Issue**    | **Fix**                                  |
| ------------ | ---------------------------------------- |
| Auth errors  | Delete `/env/token.json`                 |
| No summaries | Check Ollama is running (`ollama serve`) |
