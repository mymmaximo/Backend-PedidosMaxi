from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.productos import Productos_Respuesta, Productos_Crear
from services import productos as crud
router = APIRouter()


@router.get(
        "/producto/", 
        response_model= list[Productos_Respuesta], 
        tags=["Sección de Productos"]
)
def read_producto(
        db: Session = Depends(get_db), 
        id_producto: Optional[int] = None,
        nombre_producto: Optional[str] = None,
        precio_producto: Optional[int] = None,
        stock_producto: Optional[int] = None,
        categoria_producto: Optional[str] = None,
        codigo_barra_producto: Optional[str] = None
    ):
    db_producto = crud.get_producto(
        db, 
        id_producto=id_producto,
        nombre_producto=nombre_producto,
        precio_producto=precio_producto,
        stock_producto=stock_producto,
        categoria_producto=categoria_producto,
        codigo_barra_producto=codigo_barra_producto
    )
    if not db_producto:
        raise HTTPException(
            status_code=404, 
            detail="Producto no encontrado"
        )
    return db_producto

@router.get(
        "/productos/", 
        response_model=list[Productos_Respuesta], 
        tags=["Sección de Productos"]
)
def read_productos(
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    productos = crud.get_productos(
        db, 
        limit=limit
    )
    return productos


@router.post(
        "/productos/", 
        response_model=Productos_Respuesta, 
        tags=["Sección de Productos"]
)
def create_producto(
    producto: Productos_Crear, 
    db: Session = Depends(get_db)
):
    return crud.create_producto(
        db=db, 
        producto=producto
    )

@router.put(
        "/productos/id/{id_producto}", 
        response_model=Productos_Respuesta, 
        tags=["Sección de Productos"]
)
def update_producto(
    id_producto: int, 
    producto: Productos_Crear, 
    db: Session = Depends(get_db)
):
    db_producto = crud.update_producto(
        db, 
        id_producto=id_producto, 
        producto=producto
    )
    if db_producto is None:
        raise HTTPException(
            status_code=404, 
            detail="Producto no encontrado"
        )
    return db_producto

@router.delete(
        "/productos/id/{id_producto}", 
        tags=["Sección de Productos"]
)
def delete_producto(
    id_producto: int, 
    db: Session = Depends(get_db)
):
    success = crud.delete_producto(
        db, 
        id_producto=id_producto
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Producto no encontrado"
        )
    return {"detail": "Producto eliminado"}
