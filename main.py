from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as candidate_router
from websocket_manager import ws_router
from database import engine, Base
from models import CandidateDB
from sqlalchemy.orm import Session

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

def seed_initial_candidates():
    initial_candidates = [
        {
            "name": "Eleanor Vance",
            "party": "Innovate Today",
            "image": "https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "description": "A forward-thinking leader with 15 years of experience in tech and public policy. Advocates for digital transformation and sustainable urban development."
        },
        {
            "name": "Marcus Thorne",
            "party": "People's Union",
            "image": "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "description": "A dedicated community organizer focused on social equity and healthcare reform. Believes in strengthening local communities through grassroots initiatives."
        },
        {
            "name": "Isabella Chen",
            "party": "Green Future",
            "image": "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            "description": "A climate scientist and environmental advocate committed to implementing green policies and protecting natural resources for future generations."
        }
    ]
    db = Session(bind=engine)
    if db.query(CandidateDB).count() == 0:
        for c in initial_candidates:
            db.add(CandidateDB(**c))
        db.commit()
    db.close()

seed_initial_candidates()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://mpp-exam-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidate_router)
app.include_router(ws_router)

@app.get("/")
def read_root():
    return {"message": "MPP Exam FastAPI backend is running!"} 