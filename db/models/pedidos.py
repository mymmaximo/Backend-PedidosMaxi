from typing import Optional
from db.database import Base
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.models.clientes import Clientes_Pedidos
from db.models.direcciones import Direcciones_Pedidos
from sqlalchemy import ForeignKey,Column, Integer, String, DateTime, Float
from db.models.detalles_pedido import Detalles_Pedido_wProductos, Detalles_Pedido_wProductos_xClientes

class Pedidos(Base):
    
    # Nombre en Base de Datos
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
    transaccion_id = Column(
        String, 
        nullable=True
    )
    url_recibo = Column(
        String, 
        nullable=True
    )
    detalle_pago = Column(
        String, 
        nullable=True
    )
    monto_pagado = Column(
        Float, 
        nullable=True
    )

    # Accseos a Clientes (ID)
    clientes = relationship(
        "Clientes", 
        backref="pedidos"
    )
    # Accseos a Direcciones (ID)
    direcciones = relationship(
        "Direcciones", 
        backref="pedidos"
    )

# Clase/Modelo de Respuesta. {Clase Base}
class Pedidos_Base(BaseModel):
    id_cliente: int
    id_direccion: Optional[int] = 0
    metodo_pago: Optional[str] = " "
    tiempo_estimado_entrega: Optional[int] = 0
    tiempo_entrega: Optional[int] = 0
    estatus: Optional[int] = 4

# Clase/Modelo de Respuesta. {Leer1/LeerTodos en Rutas}
class Pedidos_CDDP(Pedidos_Base):
    id_pedido: int
    cliente : list[Clientes_Pedidos]
    direccion: list[Direcciones_Pedidos]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    total: float
    detalle_pedido : list[Detalles_Pedido_wProductos]

# Clase/Modelo de Respuesta. {Actualizar/Crear en Servicios}
class Pedidos_Crear(Pedidos_Base):
    pass

# Clase/Modelo de Respuesta. {Leer Pedido por Cliente}
class Pedidos_DDP(Pedidos_Base):
    id_pedido: int
    direccion: list[Direcciones_Pedidos]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    total: float
    estatus: int
    detalle_pedido : list[Detalles_Pedido_wProductos_xClientes]

# Clase/Modelo de Respuesta. {Leer Pedido por Producto}
class Pedidos_Detalles(Pedidos_Base):
    id_pedido: int
    total: float
    detalle_pedido : list[Detalles_Pedido_wProductos]

# Clase/Modelo de Respuesta. {Actualizar/Crear/Leer1/LeerTodos en Rutas}
class Pedidos_Respuesta(Pedidos_Base):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
    