from pydantic import BaseModel, Field, ConfigDict

#escribir/actualizar
class TareasBase(BaseModel):
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)


class TareasCreate(TareasBase):
    description: str = Field(..., min_length=1, example="Comprar leche")

# Esquema para actualizar una tarea. 
class TareasUpdate(TareasBase):
    description: str | None = Field(default=None, min_length=1, example="Comprar leche y pan")
    completed: bool | None = Field(default=None)

# Este es el modelo que se retornará al cliente.
class Tareas(TareasBase):
    id: int = Field(..., example=1)

    # Pydantic v2 usa model_config en lugar de la clase Config
    model_config = ConfigDict(from_attributes=True)
    