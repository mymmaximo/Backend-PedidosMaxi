import random
import string
from typing import Optional
from sqlalchemy import case, or_, text
from sqlalchemy.orm import Session
from db.models.archivos import Archivos
from db.models.productos import Productos, Productos_Crear, Productos_Edit, ArchivoCrear


def get_producto(
        db: Session,
        busqueda_producto: Optional[str] = None,
        precio_producto_min: Optional[int] = None,
        precio_producto_max: Optional[int] = None,
        filtrocat: Optional[str] = None,
        bool_activo: Optional[bool] = None,
        limit: int = 21,
        skip: int = 0
    ):
    query = text("SELECT * from get_all_productos ()")
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
    lista_productos = list(db_productos.values())
    if busqueda_producto is not None:
        busqueda = busqueda_producto.lower() 
        lista_filtrada = []
        for producto in lista_productos:
            nombre = producto["nombre"].lower() if producto["nombre"] else ""
            categoria = producto["categoria"].lower() if producto["categoria"] else ""
            codigo_barra = producto["codigo_barra"].lower() if producto["codigo_barra"] else ""
            if (busqueda in nombre or busqueda in categoria or busqueda in codigo_barra):
                lista_filtrada.append(producto)
        lista_productos = lista_filtrada
    if bool_activo is not None:
        lista_temporal = []
        for producto in lista_productos:
            if producto["activo"] == bool_activo:
                lista_temporal.append(producto)
        lista_productos = lista_temporal
    if precio_producto_min is not None:
        lista_temporal = []
        for producto in lista_productos:
            if producto["precio"] >= precio_producto_min:
                lista_temporal.append(producto)
        lista_productos = lista_temporal
    if precio_producto_max is not None:
        lista_temporal = []
        for producto in lista_productos:
            if producto["precio"] <= precio_producto_max:
                lista_temporal.append(producto)
        lista_productos = lista_temporal
    if filtrocat is not None:
        lista_temporal = []
        for producto in lista_productos:
            if producto["categoria"] == filtrocat:
                lista_temporal.append(producto)
        lista_productos = lista_temporal
    return lista_productos[skip : skip + limit]

def get_categoria(
        db: Session
    ):
    return db.query(Productos.categoria).distinct().all()

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
    return db_producto

def create_archivo(
        db: Session, 
        archivo: ArchivoCrear
    ):
    db_archivo = Archivos(**archivo.dict())
    db.add(db_archivo)
    db.commit()
    db.refresh(db_archivo)
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
    return True