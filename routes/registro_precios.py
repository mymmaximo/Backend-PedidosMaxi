from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from db.database import get_db
from backend_pedidos.db.models.registro_precios import RegistroPrecios, RegistroPreciosCrear, RegistroPreciosEdit, RegistroPreciosRespuesta, RegistroPrecios_wproductos
from services import registro_precios as crud
from sec import obtener_usuario_actual

router = APIRouter()

@router.get(
    "/registro_precios/", 
    response_model=list[RegistroPreciosRespuesta], 
    tags=["Sección de Registro de Precios"]
)
def read_registro_precios(
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
            detail="No tienes permiso para ver todos los registros de precios."
        )
    return crud.get_registros_precios(
        db=db, 
        skip=skip, 
        limit=limit
    )

@router.get(
    "/registro_precios/activas/", 
    response_model=list[RegistroPreciosRespuesta], 
    tags=["Sección de Registro de Precios"]
)
def read_registro_precios_activas(
    db: Session = Depends(get_db)
):
    return crud.get_registros_precios_activas(db=db)

@router.get(
    "/registro_precios/historial/", 
    response_model=list[RegistroPrecios_wproductos], 
    tags=["Sección de Registro de Precios"]
)
def read_registro_precios_historial(
    db:Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual),
    busqueda_promocion: Optional[str] = None,
    orden: Optional[int] = None,
    fecha_inicio_max: Optional[datetime] = None,
    fecha_inicio_min: Optional[datetime] = None,
    fecha_fin_max: Optional[datetime] = None,
    fecha_fin_min: Optional[datetime] = None,
    precio_nuevo_min: Optional[int] = None,
    precio_nuevo_max: Optional[int] = None,
    precio_anterior_min: Optional[int] = None,
    precio_anterior_max: Optional[int] = None,
    porcentaje_descuento_min: Optional[int] = None,
    porcentaje_descuento_max: Optional[int] = None,
    es_promocion: Optional[bool] = None,
    promo_activa: Optional[bool] = None,
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
    return crud.get_historial_registros_precios(
        db, 
        busqueda_promocion=busqueda_promocion,
        orden=orden,
        fecha_inicio_max=fecha_inicio_max,
        fecha_inicio_min=fecha_inicio_min,
        fecha_fin_max=fecha_fin_max,
        fecha_fin_min=fecha_fin_min,
        precio_nuevo_min=precio_nuevo_min,
        precio_nuevo_max=precio_nuevo_max,
        precio_anterior_min=precio_anterior_min,
        precio_anterior_max=precio_anterior_max,
        porcentaje_descuento_max=porcentaje_descuento_max,
        porcentaje_descuento_min=porcentaje_descuento_min,
        es_promocion=es_promocion,
        promo_activa=promo_activa,
        bool_activo=bool_activo,
        filtrocat=filtrocat,
        limit=limit,
        skip=skip
    )

@router.post(
    "/registro_precios/", 
    response_model=RegistroPreciosRespuesta, 
    tags=["Sección de Registro de Precios"]
)
def create_promocion(
    promocion: RegistroPreciosCrear, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 2, 3])
    if not true_rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para crear registros de precios."
        )
    return crud.create_registros_precios(
        db=db, 
        promocion=promocion
    )

@router.put(
    "/registro_precios/id/{id_promocion}", 
    response_model=RegistroPreciosRespuesta, 
    tags=["Sección de Registro de Precios"]
)
def update_promocion(
    id_promocion: int, 
    promocion: RegistroPreciosEdit, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 2])
    if not true_rol:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar registros de precios."
        )
    db_promo = crud.update_registros_precios(
        db=db, 
        id_promocion=id_promocion, 
        promocion=promocion
    )
    if db_promo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Registros de Precios no encontrados"
        )
    return db_promo

@router.delete(
    "/registro_precios/id/{id_promocion}", 
    tags=["Sección de Registro de Precios"]
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
            detail="No tienes permiso para eliminar registros de precios."
        )
    success = crud.delete_promocion(
        db=db,
        id_promocion=id_promocion
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Registros de Precios no encontrados"
        )
    return {"detail": "Promoción eliminada con éxito"}

@router.get(
    "/registro_precios/limpiar-vencidas", 
    tags=["Sección de Registro de Precios"]
)
def limpiar_vencidas(
    db: Session = Depends(get_db)
):
    db.query(RegistroPrecios).filter(
        RegistroPrecios.fecha_fin < func.now(),
        RegistroPrecios.activa == True
    ).update({"activa": False})
    db.commit()
    crud.clean_registros_cache()
    return {"mensaje": "Promociones vencidas desactivadas correctamente (Soft Delete aplicado)"}