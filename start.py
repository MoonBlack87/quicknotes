#!/usr/bin/env python3
"""
start.py — Quick Notes launcher
Handles venv creation, dependency install, DB setup, and server start.
"""
import os
import sys
import shutil
import subprocess
import webbrowser
from pathlib import Path
from time import sleep

ROOT = Path(__file__).parent
BACKEND = ROOT / "backend"
VENV = ROOT / "venv"
FRONTEND = ROOT / "frontend"
STATIC = BACKEND / "app" / "static"
PORT = 8765
URL = f"http://localhost:{PORT}"

# ── Python version check ──────────────────────────────────────────────────────

if sys.version_info < (3, 10):
    print(f"✗ Python 3.10+ required (you have {sys.version})")
    sys.exit(1)

# ── Venv ──────────────────────────────────────────────────────────────────────

PYTHON = (
    VENV / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
)

if not VENV.exists():
    print("→ Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)

# ── Dependencies ──────────────────────────────────────────────────────────────

print("→ Checking dependencies...")
subprocess.run(
    [str(PYTHON), "-m", "pip", "install", "-r", str(BACKEND / "requirements.txt"),
     "--quiet", "--disable-pip-version-check", "--upgrade"],
    check=True,
)

# ── Copy frontend → static (serve from FastAPI) ───────────────────────────────

STATIC.mkdir(parents=True, exist_ok=True)
shutil.copy2(FRONTEND / "index.html", STATIC / "index.html")

# ── Start server ──────────────────────────────────────────────────────────────

print(f"→ Starting Quick Notes on {URL}")
print("  Press Ctrl+C to stop\n")

env = os.environ.copy()
env["PYTHONPATH"] = str(BACKEND)

server = subprocess.Popen(
    [
        str(PYTHON), "-m", "uvicorn",
        "app.main:app",
        "--host", "127.0.0.1",
        "--port", str(PORT),
    ],
    cwd=str(BACKEND),
    env=env,
)

sleep(1.2)
webbrowser.open(URL)

try:
    server.wait()
except KeyboardInterrupt:
    print("\n→ Stopping server...")
    server.terminate()
