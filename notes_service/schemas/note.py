from datetime import datetime
from typing import Annotated
from pydantic import BeforeValidator, validator
from schemas.base import BaseSchema


PyObjectId = Annotated[str, BeforeValidator(str)]


class CreateNoteSchema(BaseSchema):
    title: str
    content: str

    @validator("title", "content")
    def check_empty_field(cls, value):
        if not value or value.isspace():
            raise ValueError("Пустая заметка не будет сохранена.")
        return value


class DisplayNoteSchema(BaseSchema):
    title: str
    content: str
    time_updated: datetime


class GetNoteSchema(BaseSchema):
    id: PyObjectId


class UpdateNoteSchema(BaseSchema):
    title: str
    content: str

    @validator("title", "content")
    def check_empty_field(cls, value):
        if not value or value.isspace():
            raise ValueError("Пустая заметка не будет сохранена.")
        return value
