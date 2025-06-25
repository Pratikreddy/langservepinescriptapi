from fastapi import Header
from typing import Optional
from core.config import settings

class User:
    def __init__(self, uuid: str):
        self.uuid = uuid

async def get_current_user(x_user_uuid: Optional[str] = Header(None)) -> User:
    """Get user UUID from header or use test UUID"""
    uuid = x_user_uuid or settings.TEST_UUID
    return User(uuid=uuid)