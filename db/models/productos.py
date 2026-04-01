from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from db.database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Productos(Base):
    __tablename__ = "productos"

    id = Column(
        Integer, primary_key=True, index=True)
    nombre = Column(
        String(50)
    )
    precio = Column(
        Numeric(10, 2)
    )
    stock = Column(
        Integer
    )
    categoria = Column(
        String(100), 
        index=True
    )
    codigo_barra = Column(
        String(20), 
        unique=True, 
        index=True
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )



class Productos_Base(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria: str
    
class Productos_Crear(Productos_Base):
    codigo_barra: str

class Productos_Respuesta(Productos_Base):
    id: int
    codigo_barra: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class Productos_Detalles(Productos_Base):
    id_producto: int
    codigo_barra: str
