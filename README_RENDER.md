
# Discount4U Dash Simulation — Render Deployment (Global Unlock)

## Deploy on Render
1. Push this project to GitHub.
2. On Render: **New → Web Service**, connect the repo.
3. Confirm commands:
   - **Build:** `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
   - **Start:** `gunicorn --workers 1 --threads 8 -k gthread -t 120 -b 0.0.0.0:$PORT app:server`
4. Environment variables (Render → *Environment*):
   - `PYTHON_VERSION=3.11.11`
   - `INSTRUCTOR_PIN=YOUR_PIN` (optional; default `D4U2025`)

> Why 1 worker, multi-threaded? We maintain a tiny in-memory global flag for unlocking weeks across all students. Single worker ensures a single shared memory space; threads give concurrency for a class (~30 students).

## Local Development
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py            # Dev server with hot reload
# Simulate production locally
INSTRUCTOR_PIN=Secret123   gunicorn --workers 1 --threads 8 -k gthread -t 120 -b 0.0.0.0:8050 app:server
```

## Notes
- `assets/` contains CSS (auto-loaded by Dash).
- Student progress stays in the browser (localStorage). The **global unlock** applies to every student currently connected.
- For durability across restarts or multi-instance scaling, switch the global unlock to a small shared store (e.g., Postgres/Redis) and you can then scale to multiple workers.
