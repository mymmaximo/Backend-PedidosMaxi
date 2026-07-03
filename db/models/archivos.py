from sqlalchemy import ForeignKey, Column, Integer, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.database import Base
from pydantic import BaseModel
from typing import Optional

class Archivos(Base):
    __tablename__ = "archivos"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    id_producto = Column(
        Integer, 
        ForeignKey("productos.id"), 
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
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    productos = relationship(
        "Productos", 
        foreign_keys = [id_producto],
        backref = "archivos"
    )

class ArchivoCreate(BaseModel):
    id_producto: int
    s3_key: str
    nombre_original: Optional[str] = "imagen_vue"
    tipo_contenido: Optional[str] = "image/png"
    tamanio: Optional[int] = 0

class ArchivoResponse(ArchivoCreate):
    id: int
    id_producto: int    
    class Config:
        from_attributes = True