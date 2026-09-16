from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from db.database import get_db
from db.models.promociones import Promociones, PromocionCrear, PromocionEdit, PromocionRespuesta, Promocion_wproductos
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

@router.get(
    "/promociones/historial/", 
    response_model=list[Promocion_wproductos], 
    tags=["Sección de Promociones"]
)
def read_promociones_historial(
    db:Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual),
    busqueda_promocion: Optional[str] = None,
    orden: Optional[int] = None,
    fecha_inicio_max: Optional[datetime] = None,
    fecha_inicio_min: Optional[datetime] = None,
    fecha_fin_max: Optional[datetime] = None,
    fecha_fin_min: Optional[datetime] = None,
    precio_oferta_min: Optional[int] = None,
    precio_oferta_max: Optional[int] = None,
    precio_default_min: Optional[int] = None,
    precio_default_max: Optional[int] = None,
    porcentaje_descuento_min: Optional[int] = None,
    porcentaje_descuento_max: Optional[int] = None,
    bool_activo: Optional[bool] = None,
    filtrocat: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 2, 3])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    return crud.get_historial_promocion(
        db, 
        busqueda_promocion=busqueda_promocion,
        orden=orden,
        fecha_inicio_max=fecha_inicio_max,
        fecha_inicio_min=fecha_inicio_min,
        fecha_fin_max=fecha_fin_max,
        fecha_fin_min=fecha_fin_min,
        precio_oferta_min=precio_oferta_min,
        precio_oferta_max=precio_oferta_max,
        precio_default_min=precio_default_min,
        precio_default_max=precio_default_max,
        porcentaje_descuento_max=porcentaje_descuento_max,
        porcentaje_descuento_min=porcentaje_descuento_min,
        bool_activo=bool_activo,
        filtrocat=filtrocat,
        limit=limit,
        skip=skip
    )

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
    true_rol = any(rol in roles for rol in [1, 2])
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

@router.get(
    "/promociones/limpiar-vencidas", 
    tags=["Sección de Promociones"]
)
def limpiar_vencidas(
    db: Session = Depends(get_db)
):
    db.query(Promociones).filter(Promociones.fecha_fin < func.now()).delete()
    db.commit()
    crud.clean_promos_cache()
    return {"mensaje": "Promocion Vencida"}