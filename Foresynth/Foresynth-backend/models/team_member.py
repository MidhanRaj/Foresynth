from pydantic import BaseModel
from typing import List

class TeamMember(BaseModel):
    id: str
    name: str
    skills: List[str]
    available_from: str  # e.g., "2024-08-01"
    current_load: int    # e.g., number of tasks currently assigned
