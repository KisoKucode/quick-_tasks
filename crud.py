from sqlalchemy.orm import Session
from models import Tareas
from schemas import TareasCreate, TareasUpdate 

def get_tareas(db: Session, tareas_id: int):
    return db.query(Tareas).filter(Tareas.id == tareas_id).first()


def get_tareas_by_email(db: Session, email: str):
    return db.query(Tareas).filter(Tareas.title == email).first()


def get_tareas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Tareas).offset(skip).limit(limit).all()


def delete_tareas(db: Session, tareas_id: int):
    tareas = db.query(Tareas).filter(Tareas.id == tareas_id).first()
    if tareas:
        db.delete(tareas)
        db.commit()
    return tareas


def create_tareas(db: Session, tareas: TareasCreate):
    db_tareas = Tareas(title=tareas.title, description=tareas.description, completed=tareas.completed)
    db.add(db_tareas)
    db.commit()
    db.refresh(db_tareas)
    return db_tareas

def update_tareas(db: Session, tareas_id: int, tareas_update: TareasUpdate):
    db_tareas = db.query(Tareas).filter(Tareas.id == tareas_id).first()
    if db_tareas:
        for key, value in tareas_update.dict().items():
            setattr(db_tareas, key, value)
        db.commit()
        db.refresh(db_tareas)
    return db_tareas