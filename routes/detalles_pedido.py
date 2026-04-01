from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.detalles_pedido import Detalles_Pedido_Respuesta, Detalles_Pedido_Crear
from services.productos import get_producto
from services.pedidos import get_pedido
from services import detalles_pedidos as crud
router = APIRouter()



@router.get(
        "/detalle_pedido/", 
        response_model= list[Detalles_Pedido_Respuesta], 
        tags=["Sección de Detalles de Pedidos"]
)
def read_detalle_pedido(
        db: Session = Depends(get_db), 
        id_detalle_pedido: Optional[int] = None,
        id_producto_detalle_pedido: Optional[int] = None,
        id_pedido_detalle_pedido: Optional[int] = None
    ):
    db_detalle_pedido = crud.get_detalle_pedido(
        db, 
        id_detalle_pedido=id_detalle_pedido,
        id_producto_detalle_pedido=id_producto_detalle_pedido,
        id_pedido_detalle_pedido=id_pedido_detalle_pedido
    )
    if not db_detalle_pedido:
        raise HTTPException(
            status_code=404, 
            detail="Detalle de Pedido no encontrado"
        )
    return db_detalle_pedido

@router.get(
        "/detalles_pedido/", 
        response_model=list[Detalles_Pedido_Respuesta], 
        tags=["Sección de Detalles de Pedidos"]
)
def read_detalles_pedido(
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    detalles_pedido = crud.get_detalles_pedido(
        db,
        limit=limit
    )
    return detalles_pedido

@router.post(
        "/detalles_pedidos/", 
        response_model=Detalles_Pedido_Respuesta, 
        tags=["Sección de Detalles de Pedidos"]
)
def create_detalle_pedido(
    detalle_pedido: Detalles_Pedido_Crear, 
    db: Session = Depends(get_db)
):
    db_detalle_pedido = get_pedido(
        db, 
        id_pedido=detalle_pedido.id_pedido
    )
    if not db_detalle_pedido:
        raise HTTPException(
            status_code=404, 
            detail="Pedido no encontrado"
        )
    db_producto = get_producto(
        db, 
        id_producto=detalle_pedido.id_producto
    )
    if not db_producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )
    return crud.create_detalle_pedido(
        db=db,
        detalle_pedido=detalle_pedido
    )

@router.put(
        "/detalles_pedido/id/{id_detalle_pedido}", 
        response_model=Detalles_Pedido_Respuesta, 
        tags=["Sección de Detalles de Pedidos"]
)
def update_detalle_pedido(
    id_detalle_pedido: int, 
    detalle_pedido: Detalles_Pedido_Crear,
    db: Session = Depends(get_db)
):
    db_pedido = get_pedido(
        db, 
        id_pedido=detalle_pedido.id_pedido
    )
    if not db_pedido:
        raise HTTPException(
            status_code=404, 
            detail="Pedido no encontrado"
        )
    db_producto = get_producto(
        db, 
        id_producto=detalle_pedido.id_producto
    )
    if not db_producto:
        raise HTTPException(
            status_code=404, 
            detail="Producto no encontrado"
        )
    db_detalle_actualizado = crud.update_detalle_pedido(
        db, 
        id_detalle_pedido=id_detalle_pedido, 
        detalle_pedido=detalle_pedido
    )
    if not db_detalle_actualizado:
        raise HTTPException(
            status_code=404, 
            detail="Detalle de Pedido no encontrado"
        )
    return db_detalle_actualizado

@router.delete(
        "/detalles_pedido/id/{id_detalle_pedido}", 
        tags=["Sección de Detalles de Pedidos"]
)
def delete_detalle_pedido(
    id_detalle_pedido: int, 
    db: Session = Depends(get_db)
):
    success = crud.delete_detalle_pedido(
        db, 
        id_detalle_pedido=id_detalle_pedido
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Detalle de Pedido no encontrado"
        )
    return {"detail": "Detalle de Pedido eliminado"}
