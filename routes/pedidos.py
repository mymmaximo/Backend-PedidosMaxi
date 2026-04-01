from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.pedidos import Pedidos_Respuesta, Pedidos_Crear, Pedidos_Detalles, Pedidos_CDDP
from services.clientes import get_cliente
from services.direcciones import get_direccion
from services import pedidos as crud
router = APIRouter()




@router.get(
        "/pedido/", 
        response_model= list[Pedidos_Respuesta], 
        tags=["Sección de Pedidos"]
)
def read_pedido(
        db: Session = Depends(get_db), 
        id_pedido: Optional[int] = None,
        id_cliente_pedido: Optional[int] = None,
        id_direccion_pedido: Optional[int] = None,
        metodo_pago_pedido: Optional[str] = None
    ):
    db_pedido = crud.get_pedido(
        db, 
        id_pedido=id_pedido,
        id_cliente_pedido=id_cliente_pedido,
        id_direccion_pedido=id_direccion_pedido,
        metodo_pago_pedido=metodo_pago_pedido
    )
    if not db_pedido:
        raise HTTPException(
            status_code=404, 
            detail="Pedido no encontrado"
        )
    return db_pedido

@router.get(
        "/pedidos/producto/{id_producto}",
        response_model= list[Pedidos_Detalles],
        tags=["Sección de Pedidos"]
)
def read_pedido_producto(
    id_producto: int,
    db: Session = Depends(get_db)
    ):
    db_pedidos = crud.get_pedidoxproducto(
        db,
        id_producto
    )
    if db_pedidos is False: 
        raise HTTPException(
            status_code=404, 
            detail="Producto no encontrado"
        )
    return db_pedidos

@router.get(
        "/pedidos/{id_pedido}",
        response_model= list[Pedidos_CDDP],
        tags=["Sección de Pedidos"]
)
def read_pedido_producto(
    id_pedidos: int,
    db: Session = Depends(get_db)
    ):
    db_pedidos = crud.get_pedidoxid_pedido(
        db,
        id_pedidos
    )
    if db_pedidos is False: 
        raise HTTPException(
            status_code=404, 
            detail="Pedido no encontrado"
        )
    return db_pedidos

@router.get(
        "/pedidos/", 
        response_model=list[Pedidos_Respuesta], 
        tags=["Sección de Pedidos"]
)
def read_pedidos(
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    pedidos = crud.get_pedidos(
        db, 
        limit=limit
    )
    return pedidos 

@router.get(
        "/pedidos/all/",
        response_model= list[Pedidos_CDDP],
        tags=["Sección de Pedidos"]
)
def read_pedidos(
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    pedidos = crud.get_all_pedidos(
        db, 
        limit=limit
    )
    return pedidos 

@router.post(
        "/pedidos/", 
        response_model=Pedidos_Respuesta, 
        tags=["Sección de Pedidos"]
)
def create_pedido(
    pedido: Pedidos_Crear, 
    db: Session = Depends(get_db)
):
    db_cliente = get_cliente(
        db, 
        id_cliente=pedido.id_cliente
    )
    if not db_cliente:
        raise HTTPException(
            status_code=404, 
            detail="Cliente no encontrado"
        )
    db_direccion = get_direccion(
        db, 
        id_direccion=pedido.id_direccion
    )
    if not db_direccion:
        raise HTTPException(
            status_code=404, 
            detail="Direccion no encontrada"
        )
    return crud.create_pedido(
        db=db, 
        pedido=pedido
    )

@router.put(
        "/pedidos/id/{id_pedido}", 
        response_model=Pedidos_Respuesta, 
        tags=["Sección de Pedidos"]
)
def update_pedido(
    id_pedido: int, 
    pedido: Pedidos_Crear, 
    db: Session = Depends(get_db)
):
    db_cliente = get_cliente(
        db, 
        id_cliente=pedido.id_cliente
    )
    if not db_cliente:
        raise HTTPException(
            status_code=404, 
            detail="Cliente no encontrado"
        )
    db_direccion = get_direccion(
        db, 
        id_direccion=pedido.id_direccion
    )
    if not db_direccion:
        raise HTTPException(
            status_code=404, 
            detail="Direccion no encontrada"
        )
    return crud.update_pedido(
        db, 
        id_pedido=id_pedido, 
        pedido=pedido
    )

@router.delete(
        "/pedidos/id/{id_pedido}", 
        tags=["Sección de Pedidos"]
)
def delete_pedido(
    id_pedido: int, 
    db: Session = Depends(get_db)
):    
    success = crud.delete_pedido(
        db, 
        id_pedido=id_pedido
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Pedido no encontrado"
        )
    return {"detail": "Pedido eliminado"}
