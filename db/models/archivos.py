from db.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Integer, DateTime, String

class Archivos(Base):
    
    # Nombre en Base de Datos
    __tablename__ = "archivos"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    id_producto = Column(
        Integer, 
        ForeignKey("productos.id"), 
        index=True
    )
    s3_key = Column(
        String(255), 
        unique=True, 
        index=True
    )
    nombre_original = Column(
        String(255)
    )
    tipo_contenido = Column(
        String(50)
    )
    tamanio = Column(
        Integer
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    # Accseos a Productos (ID)
    productos = relationship(
        "Productos", 
        foreign_keys = [id_producto],
        backref = "archivos"
    )
    