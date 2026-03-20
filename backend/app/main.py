from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import create_db_and_tables
from .routers.notes import router as notes_router

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


# ── API routes ────────────────────────────────────────────────────────────────

app.include_router(notes_router, prefix="/api")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": settings.APP_VERSION}


# ── Serve frontend static files ───────────────────────────────────────────────

_project_root = Path(__file__).resolve().parents[2]
_frontend_dir = _project_root / "frontend"
_static_dir = Path(__file__).parent / "static"

_served_frontend_dir = None
if (_frontend_dir / "index.html").exists():
    _served_frontend_dir = _frontend_dir
elif (_static_dir / "index.html").exists():
    _served_frontend_dir = _static_dir

if _served_frontend_dir is not None:
    app.mount(
        "/", StaticFiles(directory=_served_frontend_dir, html=True), name="static"
    )
