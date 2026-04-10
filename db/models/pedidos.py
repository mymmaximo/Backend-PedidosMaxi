from sqlalchemy import ForeignKey,Column, Integer, String, DateTime
from db.models.clientes import Clientes_Pedidos
from db.models.direcciones import Direcciones_Pedidos
from db.models.detalles_pedido import Detalles_Pedido_wProductos
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Pedidos(Base):
    __tablename__ = "pedidos"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    id_cliente = Column(
        Integer, 
        ForeignKey("clientes.id"), 
        index=True
    )
    id_direccion = Column(
        Integer, 
        ForeignKey("direcciones.id"), 
        index=True
    )
    metodo_pago = Column(
        String(50)
    )
    tiempo_entrega = Column(
        Integer
    )
    tiempo_estimado_entrega = Column(
        Integer
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now()
    )
    estatus = Column(
        Integer,
        index=True
    )


    clientes = relationship(
        "Clientes", 
        backref="pedidos"
    )
    direcciones = relationship(
        "Direcciones", 
        backref="pedidos"
    )

class Pedidos_Base(BaseModel):
    id_cliente: int
    id_direccion: Optional[int] = 0
    metodo_pago: Optional[str] = " "
    tiempo_estimado_entrega: Optional[int] = 0
    tiempo_entrega: Optional[int] = 0
    estatus: Optional[int] = 3

class Pedidos_Crear(Pedidos_Base):
    pass

class Pedidos_Respuesta(Pedidos_Base):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class Pedidos_Detalles(Pedidos_Base):
    id_pedido: int
    total: float
    detalle_pedido : list[Detalles_Pedido_wProductos]

class Pedidos_Detalles_Productos(BaseModel):
    id_pedido: int
    id_cliente: int
    id_direccion: int
    metodo_pago: str
    estatus: int
    tiempo_estimado_entrega: int
    tiempo_entrega: int
    id_detalles_pedido: int
    cantidad: int
    precio_unitario: float
    id_producto: int
    nombre: str
    precio: float
    stock: int
    categoria: str
    codigo_barra: str
    model_config = {"from_attributes": True}

class Pedidos_CDDP(Pedidos_Base):
    id_pedido: int
    cliente : list[Clientes_Pedidos]
    direccion: list[Direcciones_Pedidos]
    total: float
    detalle_pedido : list[Detalles_Pedido_wProductos]

class Pedidos_Clientes_Direcciones_Detalles_Productos(BaseModel):
    id_pedido: int
    id_cliente: int
    nombre_cliente: str
    apellido_cliente: str
    id_direccion: int
    calle: str
    numero: int
    ciudad: str
    provincia: str
    metodo_pago: str
    estatus: int
    tiempo_estimado_entrega: int
    tiempo_entrega: int
    id_detalles_pedido: int
    cantidad: int
    precio_unitario: float
    id_producto: int
    nombre: str
    precio: float
    stock: int
    categoria: str
    codigo_barra: str
    model_config = {"from_attributes": True}