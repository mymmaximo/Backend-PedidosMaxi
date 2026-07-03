from typing import Optional
from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.historial_precios import historial_wproductos
from services import historial_precios as crud
from datetime import datetime
from sec import obtener_usuario_actual
router = APIRouter()

@router.get(
    "/historial/", 
    response_model= list[historial_wproductos], 
    tags=["Sección de Historial Precios"]
)
def read_historial(
    db:Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual),
    busqueda_historial: Optional[str] = None,
    orden: Optional[int] = None,
    fecha_upgrade_max: Optional[datetime] = None,
    fecha_upgrade_min: Optional[datetime] = None,
    precio_nuevo_min: Optional[int] = None,
    precio_nuevo_max: Optional[int] = None,
    precio_viejo_min: Optional[int] = None,
    precio_viejo_max: Optional[int] = None,
    bool_activo: Optional[bool] = None,
    filtrocat: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
):
    true_rol = usuario_logeado.get("id_rol") in [1, 2, 4]
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    db_historial = crud.get_historial(
        db, 
        busqueda_historial=busqueda_historial,
        orden=orden,
        fecha_upgrade_max=fecha_upgrade_max,
        fecha_upgrade_min=fecha_upgrade_min,
        precio_nuevo_min=precio_nuevo_min,
        precio_nuevo_max=precio_nuevo_max,
        precio_viejo_min=precio_viejo_min,
        precio_viejo_max=precio_viejo_max,
        bool_activo=bool_activo,
        filtrocat=filtrocat,
        limit=limit,
        skip=skip
    )
    return db_historial