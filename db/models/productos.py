from typing import Optional
from db.database import Base
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean

class Productos(Base):

    # Nombre en Base de Datos
    __tablename__ = "productos"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    nombre = Column(
        String(50)
    )
    precio = Column(
        Numeric(10, 2)
    )
    stock = Column(
        Integer
    )
    categoria = Column(
        String(100), 
        index=True
    )
    codigo_barra = Column(
        String(20), 
        unique=True, 
        index=True
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )
    activo = Column(
        Boolean,
        default=True
    )

# Clase/Modelo de Respuesta. {Crear Imagen en Servicio}
class ArchivoCrear(BaseModel):
    id_producto: int
    s3_key: str
    nombre_original: Optional[str] = None
    tipo_contenido: Optional[str] = None
    tamanio: Optional[int] = None

# Clase/Modelo de Respuesta. {Conexión a Productos_Imagenes}
class Imagenes(BaseModel):
    id_imagen: int
    s3_key: str
    tipo_contenido: str
    tamanio: int

# Clase/Modelo de Respuesta. {Clase Base}
class Productos_Base(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria: str
    es_promocion: Optional[bool] = None
    precio_nuevo: Optional[float] = None
    precio_anterior: Optional[float] = None
    motivo: Optional[str] = None
    porcentaje_descuento: Optional[int] = None

# Clase/Modelo de Respuesta. {Leer Categorias en Rutas}
class Productos_Categoria(BaseModel):
    categoria: str

# Clase/Modelo de Respuesta. {Crear en Servicios}
class Productos_Crear(Productos_Base):
    pass

# Clase/Modelo de Respuesta. {Conexión a Detalles de Pedido}
class Productos_Detalles(Productos_Base):
    id_producto: int
    codigo_barra: str

# Clase/Modelo de Respuesta. {Conexión a Detalles de Pedido}
class Productos_Detalles_Clientes(Productos_Base):
    id_producto: int

# Clase/Modelo de Respuesta. {Actualizar en Servicio}
class Productos_Edit(BaseModel):
    nombre: Optional[str]
    precio: Optional[float]
    stock: Optional[int]
    categoria: Optional[str]
    codigo_barra: Optional[str]

# Clase/Modelo de Respuesta. {LeerTodos en Servicios y LeerTodos en Favoritos}
class Productos_Imagenes(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int
    categoria: str
    codigo_barra: str
    created_at: datetime
    updated_at: Optional[datetime]
    activo: bool
    es_promocion: Optional[bool] = None
    precio_nuevo: Optional[float] = None
    precio_anterior: Optional[float] = None
    motivo: Optional[str] = None
    porcentaje_descuento: Optional[int] = None
    imagenes: list[Imagenes]
    model_config = {"from_attributes": True}

# Clase/Modelo de Respuesta. {Actualizar/Crear/Leer(Old) en Rutas}
class Productos_Respuesta(Productos_Base):
    id: int
    codigo_barra: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    activo: bool
    model_config = {"from_attributes": True}
