from datetime import datetime

from pydantic import BaseModel

class AnonymousBoardResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime