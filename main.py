from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Union
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

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
    epic_id = Column(Integer, ForeignKey("epics.id"), nullable=True)
    epic = relationship("EpicDB", back_populates="tasks")

class EpicDB(Base):
    __tablename__ = "epics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    tasks = relationship("TaskDB", back_populates="epic", cascade="all, delete")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model
class Task(BaseModel):
    id: int
    name: str
    description: str
    epic_id: Optional[int] = None

    class Config:
        from_attributes = True

class Epic(BaseModel):
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
def get_tasks(name: Optional[str] = None,epic_id: Union[int, None] = None, db: Session = Depends(get_db)):
    query = db.query(TaskDB)
    
    # Filtriranje po 'name' ako je prisutno
    if name:
        query = query.filter(TaskDB.name.ilike(f"%{name}%"))

    # Filtriranje po 'epic_id' ako je prisutno
    if epic_id is not None:
        query = query.filter(TaskDB.name.ilike(name))

    
    tasks = query.all()  # Ovdje se poziva sve zadatke nakon filtriranja
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

    if task.epic_id is not None:
        epic = db.query(EpicDB).filter(EpicDB.id == task.epic_id).first()
        if not epic:
            raise HTTPException(status_code=404, detail="Epic not found")

    new_task = TaskDB(id=task.id, name=task.name, description=task.description, epic_id=task.epic_id)
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
    task.epic_id = updated_task.epic_id
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

@app.get("/epics", response_model=List[Epic], status_code=200)
def get_epics(db: Session = Depends(get_db)):
    return db.query(EpicDB).all()

@app.get("/epics/{epic_id}", response_model=Epic, status_code=200)
def get_epic(epic_id: int, db: Session = Depends(get_db)):
    epic = db.query(EpicDB).filter(EpicDB.id == epic_id).first()
    if not epic:
        raise HTTPException(status_code=404, detail="Epic not found")
    return epic

@app.post("/epics", response_model=Epic, status_code=201)
def create_epic(epic: Epic, db: Session = Depends(get_db)):
    if db.query(EpicDB).filter(EpicDB.id == epic.id).first():
        raise HTTPException(status_code=400, detail="Epic ID already exists")
    new_epic = EpicDB(id=epic.id, name=epic.name, description=epic.description)
    db.add(new_epic)
    db.commit()
    db.refresh(new_epic)
    return new_epic

@app.put("/epics/{epic_id}", response_model=Epic, status_code=200)
def update_epic(epic_id: int, updated_epic: Epic, db: Session = Depends(get_db)):
    epic = db.query(EpicDB).filter(EpicDB.id == epic_id).first()
    if not epic:
        raise HTTPException(status_code=404, detail="Epic not found")
    epic.name = updated_epic.name
    epic.description = updated_epic.description
    db.commit()
    db.refresh(epic)
    return epic

@app.delete("/epics/{epic_id}", status_code=204)
def delete_epic(epic_id: int, db: Session = Depends(get_db)):
    epic = db.query(EpicDB).filter(EpicDB.id == epic_id).first()
    if not epic:
        raise HTTPException(status_code=404, detail="Epic not found")
    db.delete(epic)
    db.commit()

