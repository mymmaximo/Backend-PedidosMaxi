from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.promociones import PromocionCrear, PromocionEdit, PromocionRespuesta
from services import promociones as crud
from sec import obtener_usuario_actual

router = APIRouter()

@router.get(
    "/promociones/", 
    response_model=list[PromocionRespuesta], 
    tags=["Sección de Promociones"]
)
def read_promociones(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 2])
    if not true_rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para ver todas las promociones."
        )
    return crud.get_promociones(
        db=db, 
        skip=skip, 
        limit=limit
    )

@router.get(
    "/promociones/activas/", 
    response_model=list[PromocionRespuesta], 
    tags=["Sección de Promociones"]
)
def read_promociones_activas(
    db: Session = Depends(get_db)
):
    return crud.get_promociones_activas(db=db)

@router.post(
    "/promociones/", 
    response_model=PromocionRespuesta, 
    tags=["Sección de Promociones"]
)
def create_promocion(
    promocion: PromocionCrear, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 2, 3])
    if not true_rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para crear promociones."
        )
    return crud.create_promocion(
        db=db, 
        promocion=promocion
    )

@router.put(
    "/promociones/id/{id_promocion}", 
    response_model=PromocionRespuesta, 
    tags=["Sección de Promociones"]
)
def update_promocion(
    id_promocion: int, 
    promocion: PromocionEdit, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 2, 3])
    if not true_rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar promociones."
        )
    db_promo = crud.update_promocion(
        db=db, 
        id_promocion=id_promocion, 
        promocion=promocion
    )
    if db_promo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Promoción no encontrada"
        )
    return db_promo

@router.delete(
    "/promociones/id/{id_promocion}", 
    tags=["Sección de Promociones"]
)
def delete_promocion(
    id_promocion: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 2, 3])
    if not true_rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para eliminar promociones."
        )
    success = crud.delete_promocion(
        db=db,
        id_promocion=id_promocion
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Promoción no encontrada"
        )
    return {"detail": "Promoción eliminada con éxito"}