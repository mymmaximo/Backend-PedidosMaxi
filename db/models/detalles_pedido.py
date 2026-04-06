from sqlalchemy import ForeignKey, Column, Integer, Numeric
from sqlalchemy.orm import relationship
from db.database import Base
from pydantic import BaseModel
from db.models.productos import Productos_Detalles
from typing import Optional


class Detalles_Pedido(Base):
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

    pedidos = relationship(
        "Pedidos", 
        foreign_keys = [id_pedido], 
        backref = "detalles_pedidos"
    )
    productos = relationship(
        "Productos", 
        foreign_keys = [id_producto],
        backref = "detalles_pedidos"
    )

class Detalles_Pedido_Base(BaseModel):
    id_pedido: Optional[int]
    cantidad: int
    id_producto: int

class Detalles_Pedido_Crear(Detalles_Pedido_Base):
    pass

class Detalles_Pedido_Respuesta(Detalles_Pedido_Base):
    id: int
    precio_unitario: float
    model_config = {"from_attributes": True}

class Detalles_Pedido_wProductos(BaseModel):
    id_detalle_pedido: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    producto : Productos_Detalles
