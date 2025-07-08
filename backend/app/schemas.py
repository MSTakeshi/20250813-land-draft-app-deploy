from pydantic import BaseModel, Field
from typing import Optional, List


class VoterCreate(BaseModel):
    name: str
    choice1: int = Field(..., ge=1, le=32)
    choice2: int = Field(..., ge=1, le=32)
    choice3: int = Field(..., ge=1, le=32)


class VoterResponse(BaseModel):
    name: str
    choice1: int
    choice2: int
    choice3: int
    assigned_land: Optional[int] = None


class DraftResult(BaseModel):
    round1: List[VoterResponse]
    round2: List[VoterResponse]
    round3: List[VoterResponse]
    round4: List[VoterResponse]
