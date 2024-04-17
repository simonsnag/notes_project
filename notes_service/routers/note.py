from uuid import UUID
from fastapi import APIRouter, Body, Depends

from logic.note import (
    create_note_logic,
    delete_note_logic,
    get_all_notes_logic,
    get_basket_logic,
    get_note_logic,
    restore_note_logic,
    update_note_logic,
)
from routers.depends.depends import get_user
from schemas.note import CreateNoteSchema, DisplayNoteSchema, UpdateNoteSchema

note_router = APIRouter()
basket_router = APIRouter()


@note_router.post("/create")
async def create_note(
    note: CreateNoteSchema = Body(...), user_id: UUID = Depends(get_user)
) -> DisplayNoteSchema:
    created_note = await create_note_logic(note, user_id)
    return DisplayNoteSchema.model_validate(created_note)


@note_router.get("/{id}", response_model=DisplayNoteSchema)
async def get_note(id: str, user_id: UUID = Depends(get_user)) -> DisplayNoteSchema:
    current_note = await get_note_logic(id, user_id)
    return DisplayNoteSchema.model_validate(current_note)


@note_router.get("/")
async def get_all_notes(user_id: UUID) -> list:
    return await get_all_notes_logic(user_id)


@note_router.delete("/{id}")
async def delete_note(id: str, user_id: UUID = Depends(get_user)) -> dict:
    return await delete_note_logic(id, user_id)


@note_router.patch("/{id}", response_model=DisplayNoteSchema)
async def update_note(
    id: str, data: UpdateNoteSchema = Body(...), user_id: UUID = Depends(get_user)
):
    updated_note = await update_note_logic(id, data, user_id)
    return DisplayNoteSchema.model_validate(updated_note.model_dump())


@basket_router.get("/")
async def get_basket(user_id: UUID = Depends(get_user)) -> list:
    return await get_basket_logic(user_id)


@basket_router.get("/{id}", response_model=DisplayNoteSchema)
async def restore_note(id: str, user_id: UUID = Depends(get_user)):
    restored_note = await restore_note_logic(id, user_id)
    return DisplayNoteSchema.model_validate(restored_note.model_dump())
