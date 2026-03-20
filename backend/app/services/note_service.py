from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session, select

from ..models.note import Note
from ..schemas.note import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[Note]:
        """Return all notes: pinned first, then by created_at descending."""
        statement = select(Note).order_by(
            Note.pinned.desc(),  # type: ignore[attr-defined]
            Note.created_at.desc(),
        )
        return list(self.session.exec(statement).all())

    def get_or_404(self, note_id: str) -> Note:
        note = self.session.get(Note, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note

    def create(self, data: NoteCreate) -> Note:
        note = Note(**data.model_dump())
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def update(self, note_id: str, data: NoteUpdate) -> Note:
        note = self.get_or_404(note_id)
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(note, field, value)
        note.updated_at = datetime.utcnow()
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def delete(self, note_id: str) -> None:
        note = self.get_or_404(note_id)
        self.session.delete(note)
        self.session.commit()
