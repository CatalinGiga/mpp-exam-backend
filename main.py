from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as candidate_router
from websocket_manager import ws_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidate_router)
app.include_router(ws_router)

@app.get("/")
def read_root():
    return {"message": "MPP Exam FastAPI backend is running!"} 