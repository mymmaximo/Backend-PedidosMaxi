from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from db.database import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Usuarios(Base):
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
    id_rol = Column(
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

class Token(BaseModel):
    access_token: Optional[str]
    token_type: Optional[str]
    id_cliente: Optional[int] = None
    id_usuario: Optional[int] = None
    id_rol: Optional[str] = None

class Usuarios_Base(BaseModel):
    nombre: str
    email: EmailStr

class Usuarios_Act(Usuarios_Base):
    id_rol: str
    contrasena: str

class Usuarios_Crear(Usuarios_Base):
    dni: str
    id_rol: str
    contrasena: str

class Usuarios_Direccion(BaseModel):
    id_cliente: int
    nombre: str
    email: EmailStr
    dni: str
    calle: str
    id_rol: str
    activo: bool
    model_config = {"from_attributes": True}

class Usuarios_Direcciones(Usuarios_Base):
    id: int
    dni: str
    id_rol: str
    activo: bool
    created_at: datetime

class Usuarios_Edit(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    id_rol: Optional[str] = None
    contrasena: Optional[str] = None

class Usuarios_Login(BaseModel):
    email: EmailStr
    contrasena: str

class Usuarios_Pedidos(BaseModel):
    nombre: str

class Usuarios_Respuesta(Usuarios_Base):
    id: int
    dni: str
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}