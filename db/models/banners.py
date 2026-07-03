from sqlalchemy import ForeignKey, Column, Integer, DateTime, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base
from pydantic import BaseModel
from typing import Optional

class Banners(Base):
    __tablename__ = "banner"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    s3_key = Column(
        String(255), 
        unique=True, 
        index=True
    )
    nombre_original = Column(
        String(255)
    )
    tipo_contenido = Column(
        String(50)
    )
    tamanio = Column(
        Integer
    )
    activo = Column(
        Boolean,
        default=True
    )
    enlace = Column(
        String(255)
    )
    orden = Column(
        Integer
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

class Banners_Base(BaseModel):
    s3_key: str
    activo: bool = True
    enlace: Optional[str] = None
    orden: Optional[int] = None

class Banners_Crear(Banners_Base):
    nombre_original: Optional[str] = None
    tipo_contenido: Optional[str] = None
    tamanio: Optional[int] = None

class Banners_Edit(BaseModel):
    enlace: Optional[str] = None
    orden: Optional[int] = None

class Banners_Respuesta(Banners_Base):
    id: int
    model_config = {"from_attributes": True}