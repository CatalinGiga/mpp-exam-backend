from fastapi import APIRouter, HTTPException
from models import Candidate, CandidateCreate, candidates
from typing import List
from websocket_manager import manager
import json

router = APIRouter()

@router.get("/candidates", response_model=List[Candidate])
async def get_candidates():
    return candidates

@router.post("/candidates", response_model=Candidate)
async def add_candidate(candidate: CandidateCreate):
    next_id = max([c.id for c in candidates], default=0) + 1
    new_candidate = Candidate(id=next_id, **candidate.dict())
    candidates.append(new_candidate)
    await manager.broadcast(json.dumps([c.dict() for c in candidates]))
    return new_candidate

@router.put("/candidates/{candidate_id}", response_model=Candidate)
async def update_candidate(candidate_id: int, updated: Candidate):
    for idx, c in enumerate(candidates):
        if c.id == candidate_id:
            candidates[idx] = updated
            await manager.broadcast(json.dumps([c.dict() for c in candidates]))
            return updated
    raise HTTPException(status_code=404, detail="Candidate not found.")

@router.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: int):
    for idx, c in enumerate(candidates):
        if c.id == candidate_id:
            del candidates[idx]
            await manager.broadcast(json.dumps([c.dict() for c in candidates]))
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Candidate not found.") 