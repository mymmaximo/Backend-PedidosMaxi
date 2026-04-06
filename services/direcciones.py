from typing import Optional
from sqlalchemy.orm import Session
from db.models.direcciones import Direcciones, Direcciones_Crear

def get_direccion(
        db: Session, 
        id_direccion: Optional[int] = None,
        calle_direccion: Optional[str] = None,
        barrio_direccion: Optional[str] = None,
        ciudad_direccion: Optional[str] = None,
        provincia_direccion: Optional[str] = None
    ):
    resultado = db.query(Direcciones)
    if id_direccion is not None:
        resultado = resultado.filter(
            Direcciones.id == id_direccion 
        )
    if calle_direccion is not None:
        resultado = resultado.filter(
            Direcciones.calle == calle_direccion
        )
    if barrio_direccion is not None:
        resultado = resultado.filter(
            Direcciones.barrio == barrio_direccion
        )
    if ciudad_direccion is not None:
        resultado = resultado.filter(
            Direcciones.ciudad == ciudad_direccion
        )
    if provincia_direccion is not None:
        resultado = resultado.filter(
            Direcciones.provincia == provincia_direccion 
        )
    return resultado.all()

def get_direcciones(
        db: Session, 
        limit: int = 100
    ):
    return db.query(Direcciones).limit(limit).all()

def create_direccion(
        db: Session, 
        direccion: Direcciones_Crear
    ):
    db_direccion = Direcciones(**direccion.dict())
    db.add(db_direccion)
    db.commit()
    db.refresh(db_direccion)
    return db_direccion

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

def delete_direccion(
        db: Session, 
        id_direccion: int
    ):
    db_direccion = db.query(Direcciones).filter(Direcciones.id == id_direccion).first()
    if db_direccion is None:
        return False
    db.delete(db_direccion)
    db.commit()
    return True
