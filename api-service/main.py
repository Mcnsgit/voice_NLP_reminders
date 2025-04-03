from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from fastapi.middleware.cors import CORSMiddleware
from app.routes import voice
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    description="API for voice processing in voice task manager app ",
    version="0.1.0"
)

#configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#include routers 
app.include_router(voice.router, prefix=settings.api_prefix)

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/")
async def root():
    return {"message": "Voice Task Manager API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)