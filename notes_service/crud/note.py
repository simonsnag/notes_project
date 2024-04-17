from uuid import UUID
from bson import ObjectId
from fastapi import HTTPException
import pymongo
from db.mongo_db import note_collection, basket_collection
from models.note import Note
from pymongo.results import InsertOneResult

from schemas.note import DisplayNoteSchema


async def create_note_crud(note: Note) -> InsertOneResult:
    await note_collection.create_index([("user_id", pymongo.ASCENDING)])
    return await note_collection.insert_one(note.model_dump())


async def get_note_crud(id: str) -> Note:
    try:
        current_note = await note_collection.find_one({"_id": ObjectId(id)})
    except Exception:
        raise HTTPException(
            status_code=401, detail="Заметки не существует, отсутствует доступ."
        )
    if current_note is None:
        return None
    return Note.model_validate(current_note)


async def delete_note_crud(note: Note, id: str):
    note.is_delete = True
    await basket_collection.create_index([(f"{note.user_id}", pymongo.ASCENDING)])
    result = await basket_collection.insert_one(note.model_dump())
    await note_collection.delete_one({"_id": ObjectId(id)})
    return result


async def update_note_crud(id: str, data: dict) -> InsertOneResult:
    result = await note_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    return result


async def get_all_notes_crud(user_id: UUID) -> list:
    notes = []
    async for note in note_collection.find({"user_id": user_id}):
        notes.append(DisplayNoteSchema.model_validate(note))

    return notes


async def get_basket_crud(user_id: UUID) -> list:
    notes_in_basket = []
    async for note in basket_collection.find({"user_id": user_id}):
        notes_in_basket.append(DisplayNoteSchema.model_validate(note))
    return notes_in_basket


async def restore_from_basket_crud(id: str, user_id: UUID) -> Note:
    current_note = await basket_collection.find_one(
        {"_id": ObjectId(id), "user_id": user_id}
    )
    current_note["is_delete"] = False
    await note_collection.insert_one(current_note)
    await basket_collection.delete_one({"_id": ObjectId(id), "user_id": user_id})
    return Note.model_validate(current_note)
