import random
from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.models.pedidos import Pedidos, Pedidos_Crear
from datetime import datetime

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
                "estatus": i["estatus"],
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
                "estatus": i["estatus"],
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
        busqueda_pedido: Optional[str] = None,
        filtromp: Optional[str] = None,
        filtroest: Optional[int] = None,
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
                "estatus": i["estatus"],
                "tiempo_estimado_entrega": i["tiempo_estimado_entrega"],
                "tiempo_entrega": i["tiempo_entrega"],
                "created_at": i["created_at"],
                "updated_at": i["updated_at"],
                "total": i["total"],
                "detalle_pedido": []
            }
        subtotal_detalle = i["cantidad"] * i["precio_unitario"]
        db_pedidos[id_pedidios]["total"] += subtotal_detalle
        nuevo_detalle = {
            "id_detalle_pedido": i["id_detalles_pedido"],
            "cantidad": i["cantidad"],
            "precio_unitario": i["precio_unitario"],
            "subtotal": i["dp_subtotal"],
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
    lista_pedidos = list(db_pedidos.values())
    if busqueda_pedido is not None:
        busqueda = busqueda_pedido.lower() 
        lista_filtrada = []
        for pedido in lista_pedidos:
            nombre = pedido["cliente"][0]["nombre"].lower() if pedido["cliente"] else ""
            apellido = pedido["cliente"][0]["apellido"].lower() if pedido["cliente"] else ""
            metodo = pedido["metodo_pago"].lower() if pedido["metodo_pago"] else ""
            calle = pedido["direccion"][0]["calle"].lower() if pedido["direccion"] else ""
            ciudad = pedido["direccion"][0]["ciudad"].lower() if pedido["direccion"] else ""
            provincia = pedido["direccion"][0]["provincia"].lower() if pedido["direccion"] else ""
            encontrado_en_producto = False
            for detalle in pedido["detalle_pedido"]:
                nombre_producto = detalle["producto"]["nombre"].lower()
                if busqueda in nombre_producto:
                    encontrado_en_producto = True
                    break
            if (busqueda in nombre or busqueda in apellido or busqueda in metodo or busqueda in calle or busqueda in ciudad or busqueda in provincia or encontrado_en_producto):
                lista_filtrada.append(pedido)
        lista_pedidos = lista_filtrada
    if filtromp is not None:
        lista_temporal = []
        for pedido in lista_pedidos:
            if pedido["metodo_pago"] == filtromp:
                lista_temporal.append(pedido)
        lista_pedidos = lista_temporal
    if filtroest is not None:
        lista_temporal = []
        for pedido in lista_pedidos:
            if pedido["estatus"] == filtroest:
                lista_temporal.append(pedido)
        lista_pedidos = lista_temporal
    return lista_pedidos

def get_pedidoxcliente(
        db: Session,
        id_cliente: int,
        busqueda_pedido: Optional[str] = None,
        filtromp: Optional[str] = None,
        limit: int = 100
):
    query = text("SELECT * from obtener_clientes_pedidos(:id)")
    db_pedido = db.execute(query, {"id": id_cliente}).mappings().all()
    if not db_pedido:
        return []
    db_pedidos = {}
    for i in db_pedido:
        id_pedidios = i["id_pedido"]
        if id_pedidios not in db_pedidos:
            db_pedidos[id_pedidios] = {
                "id_pedido": id_pedidios,
                "id_cliente": i["id_cliente"],
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
                "total": i["total"],
                "created_at": i["created_at"],
                "updated_at": i["updated_at"],
                "total": i["total"],
                "estatus": i["estatus"],
                "detalle_pedido": []
            }
        nuevo_detalle = {
            "id_detalle_pedido": i["id_detalles_pedido"],
            "cantidad": i["cantidad"],
            "precio_unitario": i["precio_unitario"],
            "subtotal": i["subtotal"],
                "producto": {
                "id_producto": i["id_producto"],
                "nombre": i["nombre"],
                "precio": i["precio"],
                "stock": i["stock"],
                "categoria": i["categoria"]
            }
        }
        db_pedidos[id_pedidios]["detalle_pedido"].append(nuevo_detalle)
    lista_pedidos = list(db_pedidos.values())
    if busqueda_pedido is not None:
        busqueda = busqueda_pedido.lower() 
        lista_filtrada = []
        for pedido in lista_pedidos:
            metodo = pedido["metodo_pago"].lower() if pedido["metodo_pago"] else ""
            calle = pedido["direccion"][0]["calle"].lower() if pedido["direccion"] else ""
            ciudad = pedido["direccion"][0]["ciudad"].lower() if pedido["direccion"] else ""
            provincia = pedido["direccion"][0]["provincia"].lower() if pedido["direccion"] else ""
            encontrado_en_producto = False
            for detalle in pedido["detalle_pedido"]:
                nombre_producto = detalle["producto"]["nombre"].lower()
                if busqueda in nombre_producto:
                    encontrado_en_producto = True
                    break
            if ( busqueda in metodo or busqueda in calle or busqueda in ciudad or busqueda in provincia or encontrado_en_producto):
                lista_filtrada.append(pedido)
        lista_pedidos = lista_filtrada
    if filtromp is not None:
        lista_temporal = []
        for pedido in lista_pedidos:
            if pedido["metodo_pago"] == filtromp:
                lista_temporal.append(pedido)
        lista_pedidos = lista_temporal
    return lista_pedidos

def create_pedido(
        db: Session, 
        pedido: Pedidos_Crear
):
    datos_pedido = pedido.dict()
    datos_pedido["tiempo_estimado_entrega"] = random.randint(1, 7)
    db_pedido = Pedidos(**datos_pedido)
    db.add(db_pedido)
    db.flush()
    db.refresh(db_pedido)
    return db_pedido

def update_pedido(
        db: Session, 
        id_pedido: int, 
        pedido: Pedidos_Crear
):
    datos_pedido = pedido.dict()
    db_pedido = db.query(Pedidos).filter(Pedidos.id == id_pedido).first()
    if not db_pedido:
        return None
    if datos_pedido["estatus"] == 1:
        datos_pedido["tiempo_entrega"] = (datetime.now() - db_pedido.created_at).days
    for key, value in datos_pedido.items():
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
