# AGENTS.md

## ⚙️ Agent Setup Instructions (Codex, etc.)

This project uses Django, vite, and other dependencies that may need to be installed before running any given test, script, or the frontend or backend application.

---

### 🧱 Testing


Assuming Linux/macOS...

To test backend:

```bash
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt -r requirements.dev.txt && python manage.py runserver & && pytest
```

To test frontend:

```bash
cd frontend && npm install && npm run test
```
