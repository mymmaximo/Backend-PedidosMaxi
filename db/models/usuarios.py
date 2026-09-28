from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from db.database import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Usuarios(Base):
    
    # Nombre en Base de Datos
    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True, 
        index=True
    )
    nombre = Column(
        String(50)
    )
    email = Column(
        String(100), 
        unique=True, 
        index=True
    )
    dni = Column(
        String(50), 
        unique=True, 
        index=True
    )
    contrasena = Column(
        String(255)
    )
    activo = Column(
        Boolean,
        default=True
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )

# Clase/Modelo de Respuesta. {Clase Base}
class Usuarios_Base(BaseModel):
    nombre: str
    email: EmailStr

# Clase/Modelo de Respuesta. {Crear en Servicios}
class Usuarios_Crear(Usuarios_Base):
    dni: str
    id_rol: list[int]
    contrasena: str

# Clase/Modelo de Respuesta. {Leer en Rutas}
class Usuarios_Direcciones(Usuarios_Base):
    id: int
    dni: str
    activo: bool
    id_rol: list[int]
    created_at: datetime

# Clase/Modelo de Respuesta. {Actualizar en Servicios}
class Usuarios_Edit(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    id_rol: Optional[list[int]] = None
    contrasena: Optional[str] = None

# Clase/Modelo de Respuesta. {Iniciar Sesion en Servicios}
class Usuarios_Login(BaseModel):
    email: EmailStr
    contrasena: str

# Clase/Modelo de Respuesta. {Actualizar/Crear en Rutas}
class Usuarios_Respuesta(Usuarios_Base):
    id: int
    dni: str
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
