# Quick Notes — Workflow Test Project

A minimal local note-taking app. Built to test the full
**Local → GitLab → GitHub → Issues → GitLab → Local** development workflow.

## What it does

- Create notes with a title and content
- Pin important notes to the top
- Delete notes
- Everything stored locally in SQLite

## Why this exists

This project is a **workflow sandbox**. Use it to practice and verify:
- Codex CLI development workflow
- GitLab branch/PR process
- CI/CD pipeline (tests on every push)
- GitHub issue sync (GitHub Issues → GitLab Issues)
- Clean public releases to GitHub

## Quick Start

```bash
python start.py
# opens http://localhost:8765
```

**Requirements:** Python 3.10+

## Project Structure

```
quicknotes/
  backend/          ← FastAPI + SQLite
  frontend/         ← Vanilla HTML/CSS/JS (no framework)
  scripts/          ← release + issue sync scripts
  start.py          ← launcher
  .gitlab-ci.yml    ← CI/CD pipeline
```

## Documentation

| Doc | Purpose |
|-----|---------|
| [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) | Full step-by-step workflow walkthrough |
| [AGENTS.md](AGENTS.md) | Codex CLI instructions |
| [CURRENT_STATE.md](CURRENT_STATE.md) | Live project state (updated each session) |

## API

```
GET    /api/notes          list all notes
POST   /api/notes          create note
PATCH  /api/notes/{id}     update (title, content, pinned)
DELETE /api/notes/{id}     delete note
GET    /api/health         health check
```
