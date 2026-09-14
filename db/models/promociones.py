from sqlalchemy import ForeignKey, Column, Integer, DateTime, String, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Promociones(Base):
    __tablename__ = "promociones"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    id_producto = Column(
        Integer, 
        ForeignKey("productos.id", ondelete="CASCADE"),
        index=True
    )
    nombre_promocion = Column(
        String(255)
    )
    precio_oferta = Column(
        Numeric(10, 2)
    )
    fecha_inicio = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    fecha_fin = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    productos = relationship(
        "Productos", 
        foreign_keys = [id_producto],
        backref = "promociones"
    )

class PromocionBase(BaseModel):
    id_producto: int
    nombre_promocion: Optional[str] = None
    precio_oferta: float
    fecha_inicio: datetime
    fecha_fin: datetime

class PromocionCrear(PromocionBase):
    pass

class PromocionEdit(BaseModel):
    nombre_promocion: Optional[str] = None
    precio_oferta: Optional[float] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class PromocionRespuesta(PromocionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True