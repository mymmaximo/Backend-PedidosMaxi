from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from db.database import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from db.models.direcciones import Direcciones_Clientes


class Clientes(Base):
    __tablename__ = "clientes"

    id = Column(
        Integer,
        primary_key=True, 
        index=True
    )
    usuario = Column(
        String(50)
    )
    contrasena = Column(
        String(255)
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
    apellido = Column(
        String(50)
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )
    id_rol = Column(
        Integer
    )
    activo = Column(
        Boolean,
        default=True
    )


class Clientes_Base(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    usuario: str

class Clientes_Crear(Clientes_Base):
    dni: str
    contrasena: str

class Clientes_Respuesta(Clientes_Base):
    id: int
    dni: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    direcciones: list[Direcciones_Clientes] = []
    model_config = {"from_attributes": True}

class Clientes_Pedidos(BaseModel):
    nombre: str
    apellido: str

class Clientes_Direcciones(Clientes_Base):
    id: int
    dni: str
    direcciones: list[Direcciones_Clientes]

class Clientes_Direccion(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    email: EmailStr
    dni: str
    calle: str
    id_rol: int
    id_direccion: int
    numero: int
    barrio: str
    ciudad: str
    provincia: str
    model_config = {"from_attributes": True}

class Clientes_id_Direccion(BaseModel):
    id_direccion: int
    calle: str
    numero: int
    barrio: str
    ciudad: str
    provincia: str
    model_config = {"from_attributes": True}

class Clientes_Login(BaseModel):
    usuario: str
    contrasena: str

class Token(BaseModel):
    access_token: str
    token_type: str
    id_cliente: int
    id_rol: int = 3