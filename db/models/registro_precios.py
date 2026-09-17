from sqlalchemy import ForeignKey, Column, Integer, DateTime, String, Numeric, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RegistroPrecios(Base):
    __tablename__ = "registro_precios"

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
    motivo = Column(
        String(255)
    )
    precio_nuevo = Column(
        Numeric(10, 2)
    )
    precio_anterior = Column(
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
    es_promocion = Column(
        Boolean,
        default=True
    ) 
    activa = Column(
        Boolean, 
        default=True
    )
    productos = relationship(
        "Productos", 
        foreign_keys = [id_producto],
        backref = "registro_precios"
    )

class RegistroPreciosBase(BaseModel):
    id_producto: int
    motivo: Optional[str] = None
    precio_nuevo: Optional[float] = None
    porcentaje_descuento: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    es_promocion: Optional[bool] = True
    activa: Optional[bool] = True

class RegistroPreciosCrear(RegistroPreciosBase):
    pass

class RegistroPrecios_wproductos(BaseModel):
    id: int
    id_producto: int
    motivo: Optional[str] = None
    precio_nuevo: float
    precio_anterior: float
    porcentaje_descuento: Optional[int] = None
    fecha_inicio: datetime
    fecha_fin: datetime
    es_promocion: bool
    activa: bool
    nombre: str
    categoria: str
    codigo_barra: str
    activo: bool
    model_config = {"from_attributes": True}

class RegistroPreciosEdit(BaseModel):
    motivo: Optional[str] = None
    precio_nuevo: Optional[float] = None
    porcentaje_descuento: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    es_promocion: Optional[bool] = None
    activa: Optional[bool] = None

class RegistroPreciosRespuesta(RegistroPreciosBase):
    id: int
    precio_anterior: float
    created_at: datetime
    model_config = {"from_attributes": True}