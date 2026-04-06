from typing import Optional
from sqlalchemy.orm import Session
from db.models.productos import Productos, Productos_Crear


def get_producto(
        db: Session, 
        id_producto: Optional[int] = None,
        nombre_producto: Optional[str] = None,
        precio_producto: Optional[int] = None,
        stock_producto: Optional[int] = None,
        categoria_producto: Optional[str] = None,
        codigo_barra_producto: Optional[str] = None
    ):
    resultado = db.query(Productos)
    if id_producto is not None:
        resultado = resultado.filter(
            Productos.id == id_producto 
        )
    if nombre_producto is not None:
        resultado = resultado.filter(
            Productos.nombre == nombre_producto
        )
    if precio_producto is not None:
        resultado = resultado.filter(
            Productos.precio == precio_producto
        )
    if stock_producto is not None:
        resultado = resultado.filter(
            Productos.stock == stock_producto
        )
    if categoria_producto is not None:
        resultado = resultado.filter(
            Productos.categoria == categoria_producto 
        )
    if codigo_barra_producto is not None:
        resultado = resultado.filter(
            Productos.codigo_barra == codigo_barra_producto 
        )
    return resultado.all()

def get_productos(
        db: Session, 
        limit: int = 100
    ):
    return db.query(Productos).limit(limit).all()

def create_producto(
        db: Session, 
        producto: Productos_Crear
    ):
    db_producto = Productos(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def update_producto(
        db: Session, 
        id_producto: int, 
        producto: Productos_Crear
    ):
    db_producto = db.query(Productos).filter(Productos.id == id_producto).first()
    if not db_producto:
        return None
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(
        db: Session, 
        id_producto: int
    ):
    db_producto = db.query(Productos).filter(Productos.id == id_producto).first()
    if db_producto is None:
        return False
    db.delete(db_producto)
    db.commit()
    return True
