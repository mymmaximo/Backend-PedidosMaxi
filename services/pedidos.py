from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.models.pedidos import Pedidos, Pedidos_Crear

def get_pedido(
        db: Session, 
        id_pedido: Optional[int] = None,
        id_cliente_pedido: Optional[int] = None,
        id_direccion_pedido: Optional[int] = None,
        metodo_pago_pedido: Optional[str] = None
):
    resultado = db.query(Pedidos)
    if id_pedido is not None:
        resultado = resultado.filter(
            Pedidos.id == id_pedido 
        )
    if id_cliente_pedido is not None:
        resultado = resultado.filter(
            Pedidos.id_cliente == id_cliente_pedido
        )
    if id_direccion_pedido is not None:
        resultado = resultado.filter(
            Pedidos.id_direccion == id_direccion_pedido
        )
    if metodo_pago_pedido is not None:
        resultado = resultado.filter(
            Pedidos.metodo_pago == metodo_pago_pedido
        )
    return resultado.all()

def get_pedidoxproducto(
        db: Session,
        id_producto: int
):
    
    query = text("SELECT * from obtener_productos_pedidos(:id)")
    db_pedido = db.execute(query, {"id": id_producto}).mappings().all()
    if not db_pedido:
        return False
    db_pedidos = {}
    for i in db_pedido:
        id_pedidios = i["id_pedido"]
        if id_pedidios not in db_pedidos:
            db_pedidos[id_pedidios] = {
                "id_pedido": id_pedidios,
                "id_cliente": i["id_cliente"],
                "id_direccion": i["id_direccion"],
                "metodo_pago": i["metodo_pago"],
                "tiempo_estimado_entrega": i["tiempo_estimado_entrega"],
                "tiempo_entrega": i["tiempo_entrega"],
                "detalle_pedido": [],
                "total": 0
            }
        subtotal_detalle = i["cantidad"] * i["precio_unitario"]
        db_pedidos[id_pedidios]["total"] += subtotal_detalle
        nuevo_detalle = {
            "id_detalle_pedido": i["id_detalles_pedido"],
            "cantidad": i["cantidad"],
            "precio_unitario": i["precio_unitario"],
            "subtotal": subtotal_detalle,
                "producto": {
                "id_producto": i["id_producto"],
                "nombre": i["nombre"],
                "precio": i["precio"],
                "stock": i["stock"],
                "categoria": i["categoria"],
                "codigo_barra": i["codigo_barra"]
            }
        }
        db_pedidos[id_pedidios]["detalle_pedido"].append(nuevo_detalle)
    return list(db_pedidos.values())

def get_pedidoxid_pedido(
        db: Session,
        id_pedidos: int
):
    
    query = text("SELECT * from obtener_id_pedido_pedidos(:id)")
    db_pedido = db.execute(query, {"id": id_pedidos}).mappings().all()
    if not db_pedido:
        return False
    db_pedidos = {}
    for i in db_pedido:
        id_pedidios = i["id_pedido"]
        if id_pedidios not in db_pedidos:
            db_pedidos[id_pedidios] = {
                "id_pedido": id_pedidios,
                "id_cliente": i["id_cliente"],
                "cliente": [{
                "nombre": i["nombre_cliente"],
                "apellido": i["apellido_cliente"],
                }],
                "id_direccion": i["id_direccion"],
                "direccion": [{
                    "calle": i["calle"],
                    "numero": i["numero"],
                    "ciudad": i["ciudad"],
                    "provincia": i["provincia"],
                }],
                "metodo_pago": i["metodo_pago"],
                "tiempo_estimado_entrega": i["tiempo_estimado_entrega"],
                "tiempo_entrega": i["tiempo_entrega"],
                "detalle_pedido": [],
                "total": 0
            }
        subtotal_detalle = i["cantidad"] * i["precio_unitario"]
        db_pedidos[id_pedidios]["total"] += subtotal_detalle
        nuevo_detalle = {
            "id_detalle_pedido": i["id_detalles_pedido"],
            "cantidad": i["cantidad"],
            "precio_unitario": i["precio_unitario"],
            "subtotal": subtotal_detalle,
                "producto": {
                "id_producto": i["id_producto"],
                "nombre": i["nombre"],
                "precio": i["precio"],
                "stock": i["stock"],
                "categoria": i["categoria"],
                "codigo_barra": i["codigo_barra"]
            }
        }
        db_pedidos[id_pedidios]["detalle_pedido"].append(nuevo_detalle)
    return list(db_pedidos.values())

def get_pedidos(
        db: Session, 
        limit: int = 100
):
    return db.query(Pedidos).limit(limit).all()

def get_all_pedidos(
        db: Session, 
        limit: int = 100
):
    query = text("SELECT * from obtener_all_pedidos()")
    db_pedido = db.execute(query).mappings().all()
    if not db_pedido:
        return []
    db_pedidos = {}
    for i in db_pedido:
        id_pedidios = i["id_pedido"]
        if id_pedidios not in db_pedidos:
            db_pedidos[id_pedidios] = {
                "id_pedido": id_pedidios,
                "id_cliente": i["id_cliente"],
                "cliente": [{
                "nombre": i["nombre_cliente"],
                "apellido": i["apellido_cliente"],
                }],
                "id_direccion": i["id_direccion"],
                "direccion": [{
                    "calle": i["calle"],
                    "numero": i["numero"],
                    "ciudad": i["ciudad"],
                    "provincia": i["provincia"],
                }],
                "metodo_pago": i["metodo_pago"],
                "tiempo_estimado_entrega": i["tiempo_estimado_entrega"],
                "tiempo_entrega": i["tiempo_entrega"],
                "detalle_pedido": [],
                "total": 0
            }
        subtotal_detalle = i["cantidad"] * i["precio_unitario"]
        db_pedidos[id_pedidios]["total"] += subtotal_detalle
        nuevo_detalle = {
            "id_detalle_pedido": i["id_detalles_pedido"],
            "cantidad": i["cantidad"],
            "precio_unitario": i["precio_unitario"],
            "subtotal": subtotal_detalle,
                "producto": {
                "id_producto": i["id_producto"],
                "nombre": i["nombre"],
                "precio": i["precio"],
                "stock": i["stock"],
                "categoria": i["categoria"],
                "codigo_barra": i["codigo_barra"]
            }
        }
        db_pedidos[id_pedidios]["detalle_pedido"].append(nuevo_detalle)
    return list(db_pedidos.values())

def create_pedido(
        db: Session, 
        pedido: Pedidos_Crear
):
    db_pedido = Pedidos(**pedido.dict())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def update_pedido(
        db: Session, 
        id_pedido: int, 
        pedido: Pedidos_Crear
):
    db_pedido = db.query(Pedidos).filter(Pedidos.id == id_pedido).first()
    if not db_pedido:
        return None
    for key, value in pedido.dict().items():
        setattr(db_pedido, key, value)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def delete_pedido(
        db: Session, 
        id_pedido: int
):
    db_pedido = db.query(Pedidos).filter(Pedidos.id == id_pedido).first()
    if db_pedido is None:
        return False
    db.delete(db_pedido)
    db.commit()
    return True