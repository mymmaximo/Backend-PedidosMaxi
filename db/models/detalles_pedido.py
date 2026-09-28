from typing import Optional
from db.database import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Integer, Numeric
from db.models.productos import Productos_Detalles, Productos_Detalles_Clientes

class Detalles_Pedido(Base):
    
        # Nombre en Base de Datos
    __tablename__ = "detalles_pedido"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    id_pedido = Column(
        Integer, 
        ForeignKey("pedidos.id"), 
        index=True
    )
    id_producto = Column(
        Integer, 
        ForeignKey("productos.id"), 
        index=True
    )
    cantidad = Column(
        Integer
    )
    precio_unitario = Column(
        Numeric(10, 2),
    )
    # Accseos a Pedidos (ID)
    pedidos = relationship(
        "Pedidos", 
        foreign_keys = [id_pedido], 
        backref = "detalles_pedidos"
    )
    # Accseos a Productos (ID)
    productos = relationship(
        "Productos", 
        foreign_keys = [id_producto],
        backref = "detalles_pedidos"
    )

# Clase/Modelo de Respuesta. {Clase Base}
class Detalles_Pedido_Base(BaseModel):
    id_pedido: Optional[int]
    cantidad: int
    id_producto: int
    precio_unitario: float

# Clase/Modelo de Respuesta. {Actualizar/Crear en Sevicios y Crear en Rutas de Pedidos}
class Detalles_Pedido_Crear(Detalles_Pedido_Base):
    pass

# Clase/Modelo de Respuesta. {Actualizar/Crear/Leer1/LeerTodos en Rutas y Crear en Rutas de Pedidos}
class Detalles_Pedido_Respuesta(Detalles_Pedido_Base):
    id: int
    precio_unitario: float
    model_config = {"from_attributes": True}

# Clase/Modelo de Respuesta. {Conexión a Pedidos}
class Detalles_Pedido_wProductos(BaseModel):
    id_detalle_pedido: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    producto : Productos_Detalles

# Clase/Modelo de Respuesta. {Conexión a Pedidos}
class Detalles_Pedido_wProductos_xClientes(BaseModel):
    id_detalle_pedido: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    producto : Productos_Detalles_Clientes
    