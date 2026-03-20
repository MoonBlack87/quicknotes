import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.services.note_service import NoteService
from app.schemas.note import NoteCreate, NoteUpdate


def test_create_note(session):
    service = NoteService(session)
    note = service.create(NoteCreate(title="Test Note", content="Hello world"))
    assert note.id is not None
    assert note.title == "Test Note"
    assert note.content == "Hello world"
    assert note.pinned is False


def test_create_note_empty_title_raises(session):
    service = NoteService(session)
    with pytest.raises(Exception):
        service.create(NoteCreate(title="   ", content="oops"))


def test_create_note_content_too_long_raises_validation_error():
    with pytest.raises(ValidationError):
        NoteCreate(title="Too Long", content="a" * 1001)


def test_list_notes_pinned_first(session):
    service = NoteService(session)
    service.create(NoteCreate(title="Normal Note"))
    service.create(NoteCreate(title="Pinned Note", pinned=True))
    notes = service.list()
    assert notes[0].title == "Pinned Note"
    assert notes[1].title == "Normal Note"


def test_list_notes_empty(session):
    service = NoteService(session)
    assert service.list() == []


def test_get_or_404_found(session):
    service = NoteService(session)
    created = service.create(NoteCreate(title="Find Me"))
    found = service.get_or_404(created.id)
    assert found.id == created.id


def test_get_or_404_not_found(session):
    service = NoteService(session)
    with pytest.raises(HTTPException) as exc_info:
        service.get_or_404("nonexistent-id")
    assert exc_info.value.status_code == 404


def test_update_note_title(session):
    service = NoteService(session)
    note = service.create(NoteCreate(title="Old Title"))
    updated = service.update(note.id, NoteUpdate(title="New Title"))
    assert updated.title == "New Title"
    assert updated.content == note.content  # unchanged


def test_update_note_pin(session):
    service = NoteService(session)
    note = service.create(NoteCreate(title="Pin Me"))
    assert note.pinned is False
    updated = service.update(note.id, NoteUpdate(pinned=True))
    assert updated.pinned is True


def test_update_note_content_too_long_raises_validation_error():
    with pytest.raises(ValidationError):
        NoteUpdate(content="a" * 1001)


def test_update_note_not_found(session):
    service = NoteService(session)
    with pytest.raises(HTTPException) as exc_info:
        service.update("bad-id", NoteUpdate(title="X"))
    assert exc_info.value.status_code == 404


def test_delete_note(session):
    service = NoteService(session)
    note = service.create(NoteCreate(title="Delete Me"))
    service.delete(note.id)
    assert service.list() == []


def test_delete_note_not_found(session):
    service = NoteService(session)
    with pytest.raises(HTTPException) as exc_info:
        service.delete("ghost-id")
    assert exc_info.value.status_code == 404
