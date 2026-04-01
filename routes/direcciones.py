from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.direcciones import Direcciones_Respuesta, Direcciones_Crear
from services import direcciones as crud
router = APIRouter()





@router.get(
        "/direccion/", 
        response_model= list[Direcciones_Respuesta], 
        tags=["Sección de Direcciones"]
)
def read_direccion(
        db: Session = Depends(get_db), 
        id_direccion: Optional[int] = None,
        calle_direccion: Optional[str] = None,
        barrio_direccion: Optional[str] = None,
        ciudad_direccion: Optional[str] = None,
        provincia_direccion: Optional[str] = None
    ):
    db_direccion = crud.get_direccion(
        db, 
        id_direccion=id_direccion,
        calle_direccion=calle_direccion,
        barrio_direccion=barrio_direccion,
        ciudad_direccion=ciudad_direccion,
        provincia_direccion=provincia_direccion
    )
    if not db_direccion:
        raise HTTPException(
            status_code=404, 
            detail="Direccion no encontrada"
        )
    return db_direccion

@router.get(
        "/direcciones/", 
        response_model=list[Direcciones_Respuesta], 
        tags=["Sección de Direcciones"]
)
def read_direcciones(
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    direcciones = crud.get_direcciones(
        db,
        limit=limit
    )
    return direcciones

@router.post(
        "/direcciones/", 
        response_model=Direcciones_Respuesta, 
        tags=["Sección de Direcciones"]
)
def create_direccion(
    direccion: Direcciones_Crear,
    db: Session = Depends(get_db)
):
    return crud.create_direccion(
        db=db,
        direccion=direccion
    )


@router.put(
        "/direcciones/id/{id_direccion}", 
        response_model=Direcciones_Respuesta, 
        tags=["Sección de Direcciones"]
)
def update_producto(
    id_direccion: int, 
    direccion: Direcciones_Crear, 
    db: Session = Depends(get_db)
):
    db_direccion = crud.update_direccion(
        db, 
        id_direccion=id_direccion, 
        direccion=direccion
    )
    if db_direccion is None:
        raise HTTPException(
            status_code=404, 
            detail="Direccion no encontrada"
        )
    return db_direccion


@router.delete(
        "/direcciones/id/{id_direccion}", 
        tags=["Sección de Direcciones"]
)
def delete_direccion(
    id_direccion: int, 
    db: Session = Depends(get_db)
):
    success = crud.delete_direccion(
        db, 
        id_direccion=id_direccion
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Direccion no encontrada"
        )
    return {"detail": "Direccion eliminada"}