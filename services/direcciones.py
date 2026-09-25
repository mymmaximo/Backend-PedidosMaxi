from typing import Optional
from sqlalchemy.orm import Session
from db.models.direcciones import Direcciones, Direcciones_Crear

# Codigo. {Leer 1 Direccion}
def get_direccion(
        db: Session, 
        id_direccion: Optional[int] = None,
        calle_direccion: Optional[str] = None,
        barrio_direccion: Optional[str] = None,
        ciudad_direccion: Optional[str] = None,
        provincia_direccion: Optional[str] = None
    ):
    resultado = db.query(Direcciones)
    # Filtro de ID Direccion
    if id_direccion is not None:
        resultado = resultado.filter(
            Direcciones.id == id_direccion 
        )
    # Filtro de Calle
    if calle_direccion is not None:
        resultado = resultado.filter(
            Direcciones.calle == calle_direccion
        )
    # Filtro de Barrio
    if barrio_direccion is not None:
        resultado = resultado.filter(
            Direcciones.barrio == barrio_direccion
        )
    # Filtro de Ciudad
    if ciudad_direccion is not None:
        resultado = resultado.filter(
            Direcciones.ciudad == ciudad_direccion
        )
    # Filtro de Provincia
    if provincia_direccion is not None:
        resultado = resultado.filter(
            Direcciones.provincia == provincia_direccion 
        )
    return resultado.all()

# Codigo. {Leer todas las Ciudades}
def get_ciudad(
        db: Session, 
    ):
    return db.query(Direcciones.ciudad).distinct().all()

# Codigo. {Leer todas las Provincias}
def get_provincia(
        db: Session, 
    ):
    return db.query(Direcciones.provincia).distinct().all()

# Codigo. {Leer todas las Direcciones}
def get_direcciones(
        db: Session, 
        limit: int = 100
    ):
    return db.query(Direcciones).filter(Direcciones.activo == True).limit(limit).all()

# Codigo. {Crear Direccion}
def create_direccion(
        db: Session, 
        direccion: Direcciones_Crear
    ):
    db_direccion = Direcciones(**direccion.dict())
    db.add(db_direccion)
    db.commit()
    db.refresh(db_direccion)
    return db_direccion

# Codigo. {Actualizar Direccion}
def update_direccion(
        db: Session, 
        id_direccion: int, 
        direccion: Direcciones_Crear
    ):
    db_direccion = db.query(Direcciones).filter(Direcciones.id == id_direccion).first()
    if not db_direccion:
        return None
    for key, value in direccion.dict().items():
        setattr(db_direccion, key, value)
    db.commit()
    db.refresh(db_direccion)
    return db_direccion

# Codigo. {Borrar Direcciones}
def delete_direccion(
        db: Session, 
        id_direccion: int
    ):
    db_direccion = db.query(Direcciones).filter(Direcciones.id == id_direccion).first()
    if db_direccion is None:
        return False
    db_direccion.activo = False
    db.commit()
    db.refresh(db_direccion)
    return True
