from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..database import get_session
from ..schemas.note import NoteCreate, NoteRead, NoteUpdate
from ..services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(session: Session = Depends(get_session)) -> list[NoteRead]:
    return NoteService(session).list()  # type: ignore[return-value]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(data: NoteCreate, session: Session = Depends(get_session)) -> NoteRead:
    return NoteService(session).create(data)  # type: ignore[return-value]


@router.patch("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: str,
    data: NoteUpdate,
    session: Session = Depends(get_session),
) -> NoteRead:
    return NoteService(session).update(note_id, data)  # type: ignore[return-value]


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: str,
    session: Session = Depends(get_session),
) -> None:
    NoteService(session).delete(note_id)
