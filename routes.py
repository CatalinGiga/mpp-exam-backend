from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal
from models import CandidateDB, Candidate, CandidateCreate, UserDB, User, UserCreate, VoteDB, Vote, VoteCreate
from websocket_manager import manager
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/candidates", response_model=List[Candidate])
async def get_candidates(db: Session = Depends(get_db)):
    return db.query(CandidateDB).all()

@router.post("/candidates", response_model=Candidate)
async def add_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    db_candidate = CandidateDB(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    await manager.broadcast(json.dumps([Candidate.from_orm(c).dict() for c in db.query(CandidateDB).all()]))
    return db_candidate

@router.put("/candidates/{candidate_id}", response_model=Candidate)
async def update_candidate(candidate_id: int, updated: Candidate, db: Session = Depends(get_db)):
    db_candidate = db.query(CandidateDB).filter(CandidateDB.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    for field, value in updated.dict().items():
        setattr(db_candidate, field, value)
    db.commit()
    db.refresh(db_candidate)
    await manager.broadcast(json.dumps([Candidate.from_orm(c).dict() for c in db.query(CandidateDB).all()]))
    return db_candidate

@router.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = db.query(CandidateDB).filter(CandidateDB.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    db.delete(db_candidate)
    db.commit()
    await manager.broadcast(json.dumps([Candidate.from_orm(c).dict() for c in db.query(CandidateDB).all()]))
    return {"ok": True}

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.cnp == user.cnp).first()
    if db_user:
        return db_user
    db_user = UserDB(cnp=user.cnp, has_voted=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=User)
async def login_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.cnp == user.cnp).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found. Please register.")
    return db_user

@router.post("/vote", response_model=Vote)
async def vote(vote: VoteCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == vote.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    if db_user.has_voted:
        raise HTTPException(status_code=400, detail="User has already voted.")
    db_candidate = db.query(CandidateDB).filter(CandidateDB.id == vote.candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found.")
    db_vote = VoteDB(user_id=vote.user_id, candidate_id=vote.candidate_id)
    db.add(db_vote)
    db_user.has_voted = True
    db.commit()
    db.refresh(db_vote)
    return db_vote 