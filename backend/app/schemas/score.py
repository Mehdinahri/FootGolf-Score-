from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.score import ScoreStatus
from app.models.hole import HoleSection

class ScoreCreate(BaseModel):
    hole_id: UUID
    strokes: int = Field(..., ge=1)
    penalties: int = Field(0, ge=0)
    idempotency_key: str

class ScoreUpdate(BaseModel):
    strokes: Optional[int] = Field(None, ge=1)
    penalties: Optional[int] = Field(None, ge=0)
    idempotency_key: str

class ScoreCorrection(BaseModel):
    strokes: int = Field(..., ge=1)
    penalties: int = Field(0, ge=0)
    reason: str = Field(..., min_length=5)

class ScoreResponse(BaseModel):
    id: UUID
    game_id: UUID
    player_id: UUID
    hole_id: UUID
    strokes: int
    penalties: int
    total_score: int
    status: ScoreStatus
    
    model_config = ConfigDict(from_attributes=True)

class HoleScoreDto(BaseModel):
    id: UUID
    hole_number: int
    distance: int
    par: int
    section: HoleSection
    score: dict  # Pourrait être fortement typé, mais le frontend attend qqch de précis

class ScorecardTotals(BaseModel):
    outward: int
    return_: int = Field(alias="return")
    total: int
    relative_to_par: int

class ScorecardProgress(BaseModel):
    completed_holes: int
    current_hole: int
    total_holes: int

class ScorecardGameDto(BaseModel):
    id: UUID
    title: str
    status: str

class ScorecardCourseDto(BaseModel):
    id: UUID
    name: str
    total_par: int

class ScorecardPlayerDto(BaseModel):
    id: UUID
    first_name: str
    last_name: str

class ScorecardResponse(BaseModel):
    game: ScorecardGameDto
    course: ScorecardCourseDto
    player: ScorecardPlayerDto
    progress: ScorecardProgress
    totals: ScorecardTotals
    holes: List[HoleScoreDto]
