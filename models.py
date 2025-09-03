from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Tareas(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
