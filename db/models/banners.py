from typing import Optional
from db.database import Base
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, DateTime, String, Boolean

class Banners(Base):
    
    # Nombre en Base de Datos
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


# Clase/Modelo de Respuesta. {Clase Base}
class Banners_Base(BaseModel):
    s3_key: str = Field (max_length=255)
    activo: bool = True
    enlace: Optional[str]  = Field (None, max_length=255)
    orden: Optional[int] = None

# Clase/Modelo de Respuesta. {Crear en Servicios}
class Banners_Crear(Banners_Base):
    nombre_original: Optional[str] = None
    tipo_contenido: Optional[str] = None
    tamanio: Optional[int] = None

# Clase/Modelo de Respuesta. {Actualizar en Servicios}
class Banners_Edit(BaseModel):
    enlace: Optional[str] = None
    orden: Optional[int] = None

# Clase/Modelo de Respuesta. {Actualizar/Crear/Leer en Rutas}
class Banners_Respuesta(Banners_Base):
    id: int
    model_config = {"from_attributes": True}