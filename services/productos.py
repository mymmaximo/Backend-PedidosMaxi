import random
import string
import time
from typing import Optional
from sqlalchemy import case, or_, text
from sqlalchemy.orm import Session
from db.models.archivos import Archivos
from db.models.productos import Productos, Productos_Crear, Productos_Edit, ArchivoCrear

cache = None
tiempo_cache = 0
tiempo_expiracion = 300
cache_cat = None
tiempo_cache_cat = 0

def clean_cache():
    global cache,cache_cat
    cache = None
    cache_cat = None

def get_producto(
        db: Session,
        busqueda_producto: Optional[str] = None,
        orden: Optional[int] = None,
        precio_producto_min: Optional[int] = None,
        precio_producto_max: Optional[int] = None,
        filtrocat: Optional[str] = None,
        bool_activo: Optional[bool] = None,
        limit: int = 21,
        skip: int = 0
    ):
    global cache, tiempo_cache
    tiempo_actual = time.time()
    if cache is not None and (tiempo_actual - tiempo_cache) < tiempo_expiracion:
        lista_completa = cache
        print ("cargando desde cache")
    else: 
        print ("cargando desde base")
        query = text("SELECT * from get_all_productos () order by created_at desc")
        db_producto = db.execute(query).mappings().all()
        if not db_producto:
            return []
        db_productos = {}
        for i in db_producto:
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
        lista_completa = list(db_productos.values())
        cache = lista_completa
        tiempo_cache = tiempo_actual
    productos_filtrados = lista_completa.copy()
    if orden == 1:
        productos_filtrados.sort(key=lambda x: x["nombre"].lower() if x["nombre"] else "")
    elif orden == 2:
        productos_filtrados.sort(key=lambda x: x["nombre"].lower() if x["nombre"] else "", reverse=True)
    elif orden == 3:
        productos_filtrados.sort(key=lambda x: x["precio"] or 0, reverse=True)
    elif orden == 4:
        productos_filtrados.sort(key=lambda x: x["precio"] or 0)
    elif orden == 5:
        productos_filtrados.sort(key=lambda x: x["stock"] or 0, reverse=True)
    elif orden == 6:
        productos_filtrados.sort(key=lambda x: x["stock"] or 0)
    elif orden == 7:
        productos_filtrados.sort(key=lambda x: x["created_at"] or "")
    elif orden == 8:
        productos_filtrados.sort(key=lambda x: x["created_at"] or "", reverse=True)
    else:
        productos_filtrados.sort(key=lambda x: x["created_at"] or "", reverse=True)
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

def get_categoria(
        db: Session
    ):
    global cache_cat, tiempo_cache_cat
    tiempo_actual = time.time()
    if cache_cat is not None and (tiempo_actual - tiempo_cache_cat) < tiempo_expiracion:
        print ("cargando desde cat_cache")
        return cache_cat
    print("cargando desde cat_base")
    categorias_db = db.query(Productos.categoria).distinct().all()
    resultado_seguro = [{"categoria": c.categoria} for c in categorias_db]
    cache_cat = resultado_seguro
    tiempo_cache_cat = tiempo_actual
    return resultado_seguro

def get_productos(
        db: Session, 
        limit: int = 100
    ):
    return db.query(Productos).limit(limit).all()

def create_producto(
        db: Session, 
        producto: Productos_Crear
    ):
    parte1 = ''.join(random.choices(string.ascii_uppercase, k=3))
    parte2 = ''.join(random.choices(string.ascii_uppercase, k=3))
    parte3 = ''.join(random.choices(string.digits, k=4))
    codigo_azar = f"{parte1}-{parte2}-{parte3}"
    db_producto = Productos(**producto.dict())
    db_producto.codigo_barra = codigo_azar
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    clean_cache()
    return db_producto

def create_archivo(
        db: Session, 
        archivo: ArchivoCrear
    ):
    db_archivo = Archivos(**archivo.dict())
    db.add(db_archivo)
    db.commit()
    db.refresh(db_archivo)
    clean_cache()
    return db_archivo

def update_producto(
        db: Session, 
        id_producto: int, 
        producto: Productos_Edit
    ):
    db_producto = db.query(Productos).filter(Productos.id == id_producto).first()
    if not db_producto:
        return None
    producto_act = producto.dict(exclude_unset=True)
    for key, value in producto_act.items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    clean_cache()
    return db_producto

def delete_producto(
        db: Session, 
        id_producto: int
    ):
    db_producto = db.query(Productos).filter(Productos.id == id_producto).first()
    if db_producto is None:
        return False
    db_producto.activo = not db_producto.activo
    db.commit()
    db.refresh(db_producto)
    clean_cache()
    return True

def delete_archivo(
        db: Session,
        id_archivo: int
):
    db_archivo = db.query(Archivos).filter(Archivos.id == id_archivo).first()
    if db_archivo is None:
        return False
    db.delete(db_archivo)
    db.commit()
    clean_cache()
    return True