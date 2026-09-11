from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.favoritos import FavoritoCrear
from db.models.productos import Productos_Imagenes
from services import favoritos as crud_favoritos
from sec import obtener_usuario_actual

router = APIRouter()

@router.post(
    "/favoritos/toggle", 
    tags=["Favoritos"]
)
def toggle_favorito_route(
    id_cliente: int,
    fav: FavoritoCrear,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    true_cliente = usuario_logeado.get("id_cliente") == id_cliente
    if not (true_cliente):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar este perfil."
        )
    return crud_favoritos.toggle_favorito(
        db=db, 
        id_cliente=id_cliente, 
        id_producto=fav.id_producto
    )

@router.get(
        "/favoritos/cliente/{id_cliente}", 
        tags=["Favoritos"]
    )
def obtener_favoritos(
    id_cliente: int,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    if usuario_logeado.get("id_cliente") != id_cliente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No puedes ver los favoritos de otro cliente"
        )
    return crud_favoritos.get_favoritos_cliente(db=db, id_cliente=id_cliente)

@router.get(
    "/favoritos/lista/{id_cliente}", 
    response_model=list[Productos_Imagenes], 
    tags=["Favoritos"]
)
def read_favoritos_completos(
    id_cliente: int,
    busqueda_producto: Optional[str] = None,
    orden: Optional[int] = None,
    filtrocat: Optional[str] = None,
    precio_producto_min: Optional[int] = None,
    precio_producto_max: Optional[int] = None,
    bool_activo: Optional[bool] = None,
    limit: int = 24,
    skip: int = 0, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    if usuario_logeado.get("id_cliente") != id_cliente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No puedes ver los favoritos de otro cliente"
        )
    db_favoritos = crud_favoritos.get_lista_favoritos_completa(
        db=db, 
        id_cliente=id_cliente,
        busqueda_producto=busqueda_producto,
        orden=orden,
        filtrocat=filtrocat,
        precio_producto_min=precio_producto_min,
        precio_producto_max=precio_producto_max,
        bool_activo=bool_activo,
        limit=limit,
        skip=skip
    )
    return db_favoritos