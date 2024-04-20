from uuid import UUID
from models.note import Note


def check_user(note: Note, user_id: UUID) -> bool:
    return note.user_id == user_id


def check_is_not_deleted(note: Note) -> bool:
    return not note.is_delete
