from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommitResponse(BaseModel):
    sha: str
    author: Optional[str] = None
    message: Optional[str] = None
    date: Optional[datetime] = None

    model_config = {"from_attributes": True}