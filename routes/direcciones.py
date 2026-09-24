from db.database import get_db
from sqlalchemy.orm import Session
from sec import obtener_usuario_actual
from services import direcciones as crud
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.direcciones import Direcciones_Respuesta, Direcciones_Crear, Direcciones_provincias, Direcciones_ciudades
router = APIRouter()

# Codigo. {Leer Ciudad}
@router.get(
    "/direccion/ciudad/", 
    response_model= list[Direcciones_ciudades], 
    tags=["Sección de Direcciones"]
)
def read_ciudad(
    db: Session = Depends(get_db)
):
    # Service. {Leer Ciudad}
    db_direccion = crud.get_ciudad(
        db
    )
    return db_direccion

# Codigo. {Leer Provincia}
@router.get(
    "/direccion/provincia/", 
    response_model= list[Direcciones_provincias], 
    tags=["Sección de Direcciones"]
)
def read_provincia(
    db: Session = Depends(get_db)
):
    # Service. {Leer Provincia}
    db_direccion = crud.get_provincia(
        db
    )
    return db_direccion

# Codigo. {Leer Todas las Direcciones}
@router.get(
    "/direcciones/", 
    response_model=list[Direcciones_Respuesta], 
    tags=["Sección de Direcciones"]
)
def read_direcciones(
    limit: int = 100, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Precios, Gestor de Pedidos General}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 7])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Leer Todas las Direcciones}
    direcciones = crud.get_direcciones(
        db,
        limit=limit
    )
    return direcciones

# Codigo. {Crear Direccion}
@router.post(
    "/direcciones/", 
    response_model=Direcciones_Respuesta, 
    tags=["Sección de Direcciones"]
)
def create_direccion(
    direccion: Direcciones_Crear,
    db: Session = Depends(get_db)
):
    # Codigo. {Crear Direccion}
    db_direcciones = crud.create_direccion(
        db=db,
        direccion=direccion
    )
    if db_direcciones is None:
        raise HTTPException(
            status_code=status.HTTP_404_not_FOUND, 
            detail="Direccion no encontrada"
        )
    return db_direcciones

# Codigo. {Actualizar Direccion}
@router.put(
    "/direcciones/id/{id_direccion}", 
    response_model=Direcciones_Respuesta, 
    tags=["Sección de Direcciones"]
)
def update_direccion(
    id_direccion: int, 
    direccion: Direcciones_Crear, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Precios, Gestor de Pedidos General}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 7])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Actualizar Direccion}
    db_direccion = crud.update_direccion(
        db, 
        id_direccion=id_direccion, 
        direccion=direccion
    )
    if db_direccion is None:
        raise HTTPException(
            status_code=status.HTTP_404_not_FOUND, 
            detail="Direccion no encontrada"
        )
    return db_direccion

# Codigo. {Borrar Direccion}
@router.delete(
    "/direcciones/id/{id_direccion}", 
    tags=["Sección de Direcciones"]
)
def delete_direccion(
    id_direccion: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Precios, Gestor de Pedidos General}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 7])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Borrar Direccion}
    success = crud.delete_direccion(
        db, 
        id_direccion=id_direccion
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_not_FOUND, 
            detail="Direccion no encontrada"
        )
    return {"detail": "Direccion eliminada"}