from datetime import datetime, timezone
from uuid import UUID
from fastapi import HTTPException
from crud.note import (
    create_note_crud,
    delete_note_crud,
    get_all_notes_crud,
    get_basket_crud,
    get_note_crud,
    restore_from_basket_crud,
    update_note_crud,
)
from models.note import Note
from schemas.note import CreateNoteSchema, UpdateNoteSchema
from utils import check_is_not_deleted, check_user


async def create_note_logic(payload: CreateNoteSchema, user_id: UUID) -> Note:
    note = Note(
        user_id=user_id,
        title=payload.title,
        content=payload.content,
        is_delete=False,
    )
    new_note = await create_note_crud(note)
    if not new_note.acknowledged:
        raise HTTPException(status_code=500, detail="Не удалось создать заметку.")

    created_note = await get_note_crud(new_note.inserted_id)
    if not created_note:
        raise HTTPException(status_code=404, detail="Созданная заметка не найдена.")

    return created_note


async def get_note_logic(id: str, user_id: UUID) -> Note:
    current_note = await get_note_crud(id)
    if not current_note:
        raise HTTPException(status_code=404, detail="Такой заметки не существует.")

    if check_user(current_note, user_id) and check_is_not_deleted(current_note):
        return current_note
    else:
        raise HTTPException(status_code=401, detail="Нет доступа к этой заметке.")


async def delete_note_logic(id: str, user_id: UUID) -> dict:
    current_note = await get_note_crud(id)
    if not current_note:
        raise HTTPException(status_code=404, detail="Такой заметки не существует.")
    if check_is_not_deleted(current_note) and check_user(current_note, user_id):
        await delete_note_crud(current_note, id)
        return {"Response": "Заметка перемещена в корзину."}
    else:
        raise HTTPException(
            status_code=400, detail="Невозможно удалить не существующую заметку."
        )


async def update_note_logic(id: str, note: UpdateNoteSchema, user_id: UUID) -> Note:
    current_note = await get_note_crud(id)
    if not current_note:
        raise HTTPException(status_code=404, detail="Такой заметки не существует.")
    if (
        check_user(current_note, user_id) is False
        or check_is_not_deleted(current_note) is False
    ):
        raise HTTPException(
            status_code=401, detail="Заметка удалена, либо отсутствует доступ."
        )

    data = {key: value for key, value in note.dict().items() if value is not None}
    data["time_updated"] = datetime.now(timezone.utc)
    update_result = await update_note_crud(id, data)

    if not update_result.acknowledged:
        raise HTTPException(status_code=404, detail="Заметка не найдена.")

    return await get_note_crud(id)


async def restore_note_logic(id: str, user_id: UUID) -> Note:
    current_note = await restore_from_basket_crud(id, user_id)

    return current_note


async def get_basket_logic(user_id: UUID) -> list:
    basket_for_user = await get_basket_crud(user_id)
    return basket_for_user


async def get_all_notes_logic(user_id: UUID) -> list:
    return await get_all_notes_crud(user_id)
