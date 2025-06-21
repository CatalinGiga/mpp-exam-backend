from pydantic import BaseModel
from typing import List

class CandidateBase(BaseModel):
    name: str
    party: str
    image: str
    description: str

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int

# In-memory storage with initial data from the frontend
initial_candidates = [
    {
        "id": 1,
        "name": "Eleanor Vance",
        "image": "https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "party": "Innovate Today",
        "description": "A forward-thinking leader with 15 years of experience in tech and public policy. Advocates for digital transformation and sustainable urban development."
    },
    {
        "id": 2,
        "name": "Marcus Thorne",
        "image": "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "party": "People's Union",
        "description": "A dedicated community organizer focused on social equity and healthcare reform. Believes in strengthening local communities through grassroots initiatives."
    },
    {
        "id": 3,
        "name": "Isabella Chen",
        "image": "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        "party": "Green Future",
        "description": "A climate scientist and environmental advocate committed to implementing green policies and protecting natural resources for future generations."
    }
]

candidates: List[Candidate] = [Candidate(**c) for c in initial_candidates] 