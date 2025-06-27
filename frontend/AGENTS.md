# AGENTS.md

## ⚙️ Agent Setup Instructions (Codex, etc.)

This project uses Django and other dependencies that must be installed before running tests, scripts, or the app.

---

### 🧱 Requirements

- Python 3.11+
- `pip`
- `npm`

---

### 🧪 Setup Steps

1. **Create and activate a virtual environment**

Assuming Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

3. **Run tests**

Pytest:
```bash
python manage.py runserver &
pytest
```

Jest with Vite:

```
npm run dev &
cd frontend && npm run test
```
