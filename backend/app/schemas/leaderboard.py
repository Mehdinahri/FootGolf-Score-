from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class LeaderboardRow(BaseModel):
    player_id: UUID
    first_name: str
    last_name: str
    position: int
    total_score: int
    relative_to_par: int
    holes_completed: int
    is_dnf: bool = False

class LeaderboardResponse(BaseModel):
    game_id: UUID
    status: str
    rows: List[LeaderboardRow]
    
    model_config = ConfigDict(from_attributes=True)
