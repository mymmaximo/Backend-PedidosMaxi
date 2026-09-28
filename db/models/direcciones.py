from db.database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean

class Direcciones(Base):
    
    # Nombre en Base de Datos
    __tablename__ = "direcciones"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    calle = Column(
        String(100)
    )
    numero = Column(
        Integer
    )
    barrio = Column(
        String(50)
    )
    ciudad = Column(
        String(50)
    )
    provincia = Column(
        String(50)
    )
    activo = Column(
        Boolean,
        default=True
    )

# Clase/Modelo de Respuesta. {Clase Base}
class Direcciones_Base(BaseModel):
    ciudad: str
    calle: str
    numero: int

# Clase/Modelo de Respuesta. {Conexión a Clientes}
class Direcciones_Clientes(BaseModel):
    id_direccion: int
    ciudad: str
    calle: str
    barrio: str
    numero: int
    provincia: str

# Clase/Modelo de Respuesta. {Actualizar/Crear en Servicios}
class Direcciones_Crear(Direcciones_Base):
    barrio: str
    provincia: str

# Clase/Modelo de Respuesta. {Leer Ciudad en Rutas}
class Direcciones_ciudades(BaseModel):
    ciudad: str

# Clase/Modelo de Respuesta. {Conexión a Pedidos}
class Direcciones_Pedidos(BaseModel):
    ciudad: str
    calle: str
    numero: int
    provincia: str

# Clase/Modelo de Respuesta. {Leer Provincia en Rutas}
class Direcciones_provincias(BaseModel):
    provincia: str

# Clase/Modelo de Respuesta. {Actualizar/Crear/LeerTodos en Rutas}
class Direcciones_Respuesta(Direcciones_Base):
    id: int
    barrio: str
    provincia: str
    model_config = {"from_attributes": True}