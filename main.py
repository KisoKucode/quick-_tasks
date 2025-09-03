from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quick Tasks")

# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear tarea
@app.post("/tareas/", response_model=schemas.Tareas)
def create_tarea(tarea: schemas.TareasCreate, db: Session = Depends(get_db)):
    return crud.create_tarea(db=db, tarea=tarea)

# Listar todas las tareas
@app.get("/tareas/", response_model=list[schemas.Tareas])
def read_tareas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tareas(db, skip=skip, limit=limit)

# Leer tarea por ID
@app.get("/tareas/{tarea_id}", response_model=schemas.Tareas)
def read_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = crud.get_tarea(db, tarea_id=tarea_id)
    if not db_tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

# Actualizar tarea
@app.put("/tareas/{tarea_id}", response_model=schemas.Tareas)
def update_tarea(tarea_id: int, tarea: schemas.TareasUpdate, db: Session = Depends(get_db)):
    db_tarea = crud.update_tarea(db=db, tarea_id=tarea_id, tarea_update=tarea)
    if not db_tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

# Eliminar tarea
@app.delete("/tareas/{tarea_id}", response_model=schemas.Tareas)
def delete_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = crud.delete_tarea(db, tarea_id=tarea_id)
    if not db_tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

# Raíz
@app.get("/")
def read_root():
    return {"message": "Welcome to the Quick Tasks API by Daniel"}


## arranque de api uvicorn main:app --reload

