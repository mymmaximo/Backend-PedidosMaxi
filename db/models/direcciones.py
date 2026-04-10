from sqlalchemy import ForeignKey, Column, Integer, String
from db.database import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship

class Direcciones(Base):
    __tablename__ = "direcciones"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    calle = Column(
        String(100)
    )
    numero = Column(
        Integer
    )
    barrio = Column(
        String(50)
    )
    ciudad = Column(
        String(50)
    )
    provincia = Column(
        String(50)
    )
  
    
class Direcciones_Base(BaseModel):
    ciudad: str
    calle: str
    numero: int

class Direcciones_Crear(Direcciones_Base):
    barrio: str
    provincia: str

class Direcciones_Respuesta(Direcciones_Base):
    id: int
    barrio: str
    provincia: str
    model_config = {"from_attributes": True}

class Direcciones_Pedidos(BaseModel):
    ciudad: str
    calle: str
    numero: int
    provincia: str

class Direcciones_Clientes(BaseModel):
    id_direccion: int
    ciudad: str
    calle: str
    barrio: str
    numero: int
    provincia: str