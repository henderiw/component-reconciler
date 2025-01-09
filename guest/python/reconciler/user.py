from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []