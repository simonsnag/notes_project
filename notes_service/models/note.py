from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class Note(BaseModel):
    user_id: UUID
    title: str
    content: str
    is_delete: bool = False
    time_created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    time_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True


class Basket(BaseModel):
    id: str = "1234"
    deleted_notes: Optional[Dict[UUID, List[str]]] = {}
