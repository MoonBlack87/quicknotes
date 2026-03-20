from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

MAX_NOTE_CONTENT_LENGTH = 1000


class NoteCreate(BaseModel):
    title: str
    content: str = ""
    pinned: bool = False

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("content")
    @classmethod
    def content_within_limit(cls, v: str) -> str:
        if len(v) > MAX_NOTE_CONTENT_LENGTH:
            raise ValueError(
                f"Content cannot exceed {MAX_NOTE_CONTENT_LENGTH} characters"
            )
        return v


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    pinned: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v

    @field_validator("content")
    @classmethod
    def content_within_limit(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > MAX_NOTE_CONTENT_LENGTH:
            raise ValueError(
                f"Content cannot exceed {MAX_NOTE_CONTENT_LENGTH} characters"
            )
        return v


class NoteRead(BaseModel):
    id: str
    title: str
    content: str
    pinned: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
