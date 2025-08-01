from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    id: str
    title: str
    assigned_to: str
    depends_on: List[str]
    duration_days: int
    status: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
