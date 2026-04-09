from typing import Optional
from sqlalchemy.orm import Session
from db.models.detalles_pedido import Detalles_Pedido, Detalles_Pedido_Crear
from db.models.productos import Productos

def get_detalle_pedido(
        db: Session, 
        id_detalle_pedido: Optional[int] = None,
        id_producto_detalle_pedido: Optional[int] = None,
        id_pedido_detalle_pedido: Optional[int] = None
    ):
    resultado = db.query(Detalles_Pedido)
    if id_detalle_pedido is not None:
        resultado = resultado.filter(
            Detalles_Pedido.id == id_detalle_pedido 
        )
    if id_producto_detalle_pedido is not None:
        resultado = resultado.filter(
            Detalles_Pedido.id_producto == id_producto_detalle_pedido
        )
    if id_pedido_detalle_pedido is not None:
        resultado = resultado.filter(
            Detalles_Pedido.id_pedido == id_pedido_detalle_pedido
        )
    return resultado.all()

def get_detalles_pedido(
        db: Session, 
        limit: int = 100
    ):
    return db.query(Detalles_Pedido).limit(limit).all()

def create_detalle_pedido(
        db: Session, 
        detalle_pedido: list[Detalles_Pedido_Crear]
    ):
    lista_detalles = []
    for i in detalle_pedido:
        db_producto = db.query(Productos).filter(Productos.id == i.id_producto).first()
        if db_producto is None:
            return False
        db_detalle_pedido = Detalles_Pedido(
            id_pedido=i.id_pedido,
            id_producto=i.id_producto,
            cantidad=i.cantidad,
            precio_unitario=db_producto.precio
        )
        lista_detalles.append(db_detalle_pedido)
        db.add(db_detalle_pedido)
        db.flush()
        db.refresh(db_detalle_pedido)
    return lista_detalles

def update_detalle_pedido(
        db: Session, 
        id_detalle_pedido: int, 
        detalle_pedido: Detalles_Pedido_Crear
    ):
    db_detalle_pedido = db.query(Detalles_Pedido).filter(Detalles_Pedido.id == id_detalle_pedido).first()
    if not db_detalle_pedido:
        return None
    for key, value in detalle_pedido.dict().items():
        setattr(db_detalle_pedido, key, value)
    db.commit()
    db.refresh(db_detalle_pedido)
    return db_detalle_pedido

def delete_detalle_pedido(
        db: Session, 
        id_detalle_pedido: int
    ):
    db_detalle_pedido = db.query(Detalles_Pedido).filter(Detalles_Pedido.id == id_detalle_pedido).first()
    if db_detalle_pedido is None:
        return False
    db.delete(db_detalle_pedido)
    db.commit()
    return True
