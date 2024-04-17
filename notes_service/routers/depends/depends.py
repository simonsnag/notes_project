from uuid import UUID
from fastapi import Header


async def get_user(user_data: str = Header()) -> UUID:
    return UUID(user_data)
