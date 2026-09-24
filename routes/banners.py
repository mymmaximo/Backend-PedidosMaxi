from typing import Optional
from db.database import get_db
from sqlalchemy.orm import Session
from services import banners as crud
from sec import obtener_usuario_actual
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.banners import Banners_Respuesta, Banners_Crear, Banners_Edit
router = APIRouter()

# Codigo. {Ver Banners}
@router.get(
    "/banners/",
    response_model=list[Banners_Respuesta],
    tags=["Sección de Banners"]
)
def read_banners(
    limit: int = 100,
    bool_activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    # Service. {Ver Banners}
    banners = crud.get_banners(
        db,
        limit=limit,
        bool_activo = bool_activo
    )
    return banners

# Codigo. {Nuevo Banner}
@router.post(
    "/banners/",
    response_model=Banners_Respuesta,
    tags=["Sección de Banners"]
)
def create_banners(
    banner: Banners_Crear,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar esto."
        )
    # Codigo. {Nuevo Banner}
    return crud.create_banner(
        db=db, 
        banner=banner
    )

# Codigo. {Actualizar Banner}
@router.put(
    "/banners/id/{id_banner}", 
    response_model=Banners_Respuesta, 
    tags=["Sección de Banners"]
)
def update_banners(
    id_banner: int,
    banner: Banners_Edit,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar esto."
        )
    # Service. {Actualizar Banner}
    db_banner = crud.update_banner(
        db, 
        id_banner=id_banner, 
        banner=banner
    )
    if db_banner is None:
        raise HTTPException(
            status_code=status.HTTP_404_not_FOUND, 
            detail="Banners no encontrado"
        )
    return db_banner

# Codigo. {Desactivar Banner}
@router.put(
    "/banners/estado/id/{id_banner}", 
    tags=["Sección de Banners"]
)
def deact_banner(
    id_banner: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permisos para modificar esto."
        )
    # Service. {Desactivar Banner}
    success = crud.deact_banner(
        db, 
        id_banner=id_banner
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_not_FOUND, 
            detail="Banner no encontrado"
        )
    return {"detail": "Banner desactivado"}

# Codigo. {Borrar Banner}
@router.delete(
    "/banners/id/{id_banner}", 
    tags=["Sección de Banners"]
)
def hard_delete_banner(
    id_banner: int,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permisos para modificar esto."
        )
    # Service. {Borrar Banner}
    success = crud.hard_delete_banner(
        db,
        id_banner=id_banner
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_not_FOUND,
            detail="Banner no encontrado"
        )
    return {"detail": "Banner eliminado"}