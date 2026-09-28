from typing import Optional
from db.database import Base
from datetime import datetime
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from db.models.direcciones import Direcciones_Clientes
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class Clientes(Base):
    
    # Nombre en Base de Datos
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

# Clase/Modelo de Respuesta. {Clase Base}
class Clientes_Base(BaseModel):
    nombre: str
    email: EmailStr

# Clase/Modelo de Respuesta. {Crear en Servicios}
class Clientes_Crear(Clientes_Base):
    dni: str
    contrasena: str

# Clase/Modelo de Respuesta. {Leer 1 o Todos en Rutas}
class Clientes_Direcciones(Clientes_Base):
    id: int
    dni: str
    activo: bool
    created_at: datetime
    direcciones: list[Direcciones_Clientes]

# Clase/Modelo de Respuesta. {Actualizar en Servicios}
class Clientes_Edit(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    contrasena: Optional[str] = None

# Clase/Modelo de Respuesta. {Leer Direccion en Rutas}
class Clientes_id_Direccion(BaseModel):
    id_direccion: int
    calle: str
    numero: int
    barrio: str
    ciudad: str
    provincia: str
    model_config = {"from_attributes": True}

# Clase/Modelo de Respuesta. {Iniciar Sesion en Servicios}
class Clientes_Login(BaseModel):
    email: EmailStr
    contrasena: str

# Clase/Modelo de Respuesta. {Conexión a Pedidos}
class Clientes_Pedidos(BaseModel):
    nombre: str

# Clase/Modelo de Respuesta. {Actualizar/Crear en Rutas}
class Clientes_Respuesta(Clientes_Base):
    id: int
    dni: str
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    direcciones: list[Direcciones_Clientes] = []
    model_config = {"from_attributes": True}
    