from db.database import Base
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint

class Favoritos(Base):

    # Nombre en Base de Datos
    __tablename__ = "favoritos"
    
    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    id_cliente = Column(
        Integer, 
        ForeignKey(
            "clientes.id", 
            ondelete="CASCADE"
        ), 
        nullable=False
    )
    id_producto = Column(
        Integer, 
        ForeignKey(
            "productos.id", 
            ondelete="CASCADE"
        ), 
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    # Tablas Ajenas
    __table_args__ = (UniqueConstraint('id_cliente', 'id_producto', name='_cliente_producto_uc'),)

# Clase/Modelo de Respuesta. {Añadir/Quitar en Rutas}
class FavoritoBase(BaseModel):
    id_producto: int
