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

class Clientes_Base(BaseModel):
    nombre: str
    email: EmailStr

class Clientes_Crear(Clientes_Base):
    dni: str
    contrasena: str

class Clientes_Act(Clientes_Base):
    contrasena: str

class Clientes_Respuesta(Clientes_Base):
    id: int
    dni: str
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    direcciones: list[Direcciones_Clientes] = []
    model_config = {"from_attributes": True}

class Clientes_Pedidos(BaseModel):
    nombre: str

class Clientes_Direcciones(Clientes_Base):
    id: int
    dni: str
    activo: bool
    created_at: datetime
    direcciones: list[Direcciones_Clientes]

class Clientes_Direccion(BaseModel):
    id_cliente: int
    nombre: str
    email: EmailStr
    dni: str
    calle: str
    activo: bool
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
    email: EmailStr
    contrasena: str

class Token(BaseModel):
    access_token: Optional[str]
    token_type: Optional[str]
    id_cliente: Optional[int] = None
    id_usuario: Optional[int] = None
    id_rol: Optional[int] = None

class Clientes_Edit(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = None