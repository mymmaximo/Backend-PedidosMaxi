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
    precio_default = Column(
        Numeric(10, 2)
    )
    porcentaje_descuento = Column(
        Integer
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
    precio_oferta: Optional[float] = None
    porcentaje_descuento: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: datetime

class PromocionCrear(PromocionBase):
    pass

class Promocion_wproductos(BaseModel):
    id: int
    id_producto: int
    nombre_promocion: Optional[str] = None
    precio_oferta: float
    precio_default: float
    porcentaje_descuento: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    nombre: str
    categoria: str
    codigo_barra: str
    activo: bool
    model_config = {"from_attributes": True}

class PromocionEdit(BaseModel):
    nombre_promocion: Optional[str] = None
    precio_oferta: Optional[float] = None
    porcentaje_descuento: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None

class PromocionRespuesta(PromocionBase):
    id: int
    precio_default: float
    created_at: datetime
    model_config = {"from_attributes": True}