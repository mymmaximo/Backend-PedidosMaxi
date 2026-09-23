from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.models.favoritos import Favoritos

def toggle_favorito(
    db: Session, 
    id_cliente: int, 
    id_producto: int
):
    favorito_existente = db.query(Favoritos).filter(
        Favoritos.id_cliente == id_cliente,
        Favoritos.id_producto == id_producto
    ).first()    
    if favorito_existente:
        db.delete(favorito_existente)
        db.commit()
        return {
            "mensaje": "Removido de favoritos", 
            "estado_favorito": False
        }
    else:
        nuevo_favorito = Favoritos(
            id_cliente=id_cliente, 
            id_producto=id_producto
        )
        db.add(nuevo_favorito)
        db.commit()
        db.refresh(nuevo_favorito)
        return {
            "mensaje": "Agregado a favoritos", 
            "estado_favorito": True
        }

def get_favoritos_cliente(
    db: Session, 
    id_cliente: int
):
    favoritos = db.query(Favoritos.id_producto).filter(Favoritos.id_cliente == id_cliente).all()
    return [fav[0] for fav in favoritos]

def get_lista_favoritos_completa(
        db: Session, 
        id_cliente: int,
        busqueda_producto: Optional[str] = None,
        orden: Optional[int] = None,
        precio_producto_min: Optional[int] = None,
        precio_producto_max: Optional[int] = None,
        filtrocat: Optional[str] = None,
        bool_activo: Optional[bool] = None,
        limit: int = 24,
        skip: int = 0
    ):
    query = text("SELECT * FROM obtener_favoritos_cliente(:id_cliente)")
    db_favoritos = db.execute(
        query, 
        {"id_cliente": id_cliente}).mappings().all()
    if not db_favoritos:
        return []
    db_productos = {}
    for i in db_favoritos:
        id_productron = i["id"]
        if id_productron not in db_productos:
            db_productos[id_productron] = {
                "id": id_productron,
                "nombre": i["nombre"],
                "precio": i["precio"],
                "stock": i["stock"],
                "categoria": i["categoria"],
                "codigo_barra": i["codigo_barra"],
                "created_at": i["created_at"],
                "updated_at": i["updated_at"],
                "activo": i["activo"],
                "fav_created_at": i["fav_created_at"],
                "imagenes": []
            }
        if i["id_imagen"] is not None:
            imagen_echo = False
            for img_guardada in db_productos[id_productron]["imagenes"]:
                if img_guardada["id_imagen"] == i["id_imagen"]:
                    imagen_echo = True
                    break
            if imagen_echo == False:
                nueva_imagen = {
                    "id_imagen": i["id_imagen"],
                    "s3_key": i["s3_key"],
                    "tipo_contenido": i["tipo_contenido"],
                    "tamanio": i["tamanio"]
                }
                db_productos[id_productron]["imagenes"].append(nueva_imagen)
    productos_filtrados = list(db_productos.values())
    if orden == 1:
        productos_filtrados.sort(
            key=lambda x: x["nombre"].lower() if x["nombre"] else ""
        )
    elif orden == 2:
        productos_filtrados.sort(
            key=lambda x: x["nombre"].lower() if x["nombre"] else "", reverse=True
        )
    elif orden == 3:
        productos_filtrados.sort(
            key=lambda x: x["precio"] or 0, 
            reverse=True
            )
    elif orden == 4:
        productos_filtrados.sort(
            key=lambda x: x["precio"] or 0
        )
    elif orden == 5:
        productos_filtrados.sort(
            key=lambda x: x["stock"] or 0, 
            reverse=True
        )
    elif orden == 6:
        productos_filtrados.sort(
            key=lambda x: x["stock"] or 0
        )
    elif orden == 7:
        productos_filtrados.sort(
            key=lambda x: x["fav_created_at"] or ""
            )
    elif orden == 8:
        productos_filtrados.sort(
            key=lambda x: x["fav_created_at"] or "", 
            reverse=True
        )
    else:
        productos_filtrados.sort(
            key=lambda x: x["fav_created_at"] or "", 
            reverse=True
        )
    if busqueda_producto is not None:
        busqueda = busqueda_producto.lower() 
        lista_filtrada = []
        for producto in productos_filtrados:
            nombre = producto["nombre"].lower() if producto["nombre"] else ""
            categoria = producto["categoria"].lower() if producto["categoria"] else ""
            codigo_barra = producto["codigo_barra"].lower() if producto["codigo_barra"] else ""
            if (busqueda in nombre or busqueda in categoria or busqueda in codigo_barra):
                lista_filtrada.append(producto)
        productos_filtrados = lista_filtrada
    if bool_activo is not None:
        lista_temporal = []
        for producto in productos_filtrados:
            if producto["activo"] == bool_activo:
                lista_temporal.append(producto)
        productos_filtrados = lista_temporal
    if precio_producto_min is not None:
        lista_temporal = []
        for producto in productos_filtrados:
            if producto["precio"] >= precio_producto_min:
                lista_temporal.append(producto)
        productos_filtrados = lista_temporal
    if precio_producto_max is not None:
        lista_temporal = []
        for producto in productos_filtrados:
            if producto["precio"] <= precio_producto_max:
                lista_temporal.append(producto)
        productos_filtrados = lista_temporal
    if filtrocat is not None:
        lista_temporal = []
        for producto in productos_filtrados:
            if producto["categoria"] == filtrocat:
                lista_temporal.append(producto)
        productos_filtrados = lista_temporal
    return productos_filtrados[skip : skip + limit]