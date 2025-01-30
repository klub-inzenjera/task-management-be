from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ORM model
class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model
class Task(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/tasks", response_model=List[Task], status_code=200)
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskDB).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=Task, status_code=200)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task, db: Session = Depends(get_db)):
    existing_task = db.query(TaskDB).filter(TaskDB.id == task.id).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Task ID already exists")

    new_task = TaskDB(id=task.id, name=task.name, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=Task, status_code=200)
def update_task(task_id: int, updated_task: Task, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.name = updated_task.name
    task.description = updated_task.description
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

#Epics

