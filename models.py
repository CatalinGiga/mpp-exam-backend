from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class CandidateDB(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=False)
    image = Column(String, nullable=False)
    description = Column(String, nullable=False)
    votes = relationship("VoteDB", back_populates="candidate")

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    cnp = Column(String, unique=True, nullable=False, index=True)
    has_voted = Column(Boolean, default=False)
    votes = relationship("VoteDB", back_populates="user")

class VoteDB(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    user = relationship("UserDB", back_populates="votes")
    candidate = relationship("CandidateDB", back_populates="votes")

# Pydantic models (for request/response)
class CandidateBase(BaseModel):
    name: str
    party: str
    image: str
    description: str

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    cnp: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    has_voted: bool
    class Config:
        from_attributes = True

class VoteBase(BaseModel):
    user_id: int
    candidate_id: int

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    id: int
    class Config:
        from_attributes = True 