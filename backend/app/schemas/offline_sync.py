from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class SyncScorePayload(BaseModel):
    hole_id: UUID
    strokes: int = Field(..., ge=1)
    penalties: int = Field(0, ge=0)
    idempotency_key: str

class SyncRequest(BaseModel):
    game_id: UUID
    scores: List[SyncScorePayload]

class SyncResponseItem(BaseModel):
    idempotency_key: str
    status: str
    error: Optional[str] = None

class SyncResponse(BaseModel):
    results: List[SyncResponseItem]
