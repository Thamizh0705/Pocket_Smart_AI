# PocketSmart AI

FastAPI implementation of the PocketSmart AI project: budget-aware Home, Party and Jewelry planners, user authentication, session/history tracking, platform search links, optional Gemini text/image generation, and a fallback recommendation engine.

## Windows setup

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m pytest -q
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Gemini is optional. Without `GEMINI_API_KEY`, the app uses its local fallback engine, so the website and planners still work. Add the key to `.env` to enable Gemini calls.
