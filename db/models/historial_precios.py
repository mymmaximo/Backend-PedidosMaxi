from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.sql import func
from db.database import Base
from pydantic import BaseModel
from datetime import datetime


class Historial_Precios(Base):
    __tablename__ = "historial_precios"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    id_producto = Column(
        Integer
    )
    precio_viejo = Column(
        Numeric(10, 2)
    )
    precio_nuevo = Column(
        Numeric(10, 2)
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )

    
class historial_wproductos(BaseModel):
    id: int
    id_producto: int
    nombre: str
    categoria: str
    codigo_barra: str
    precio_viejo: int
    precio_nuevo: int
    updated_at: datetime
    model_config = {"from_attributes": True}