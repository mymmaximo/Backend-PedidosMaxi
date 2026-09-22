import os
import time
import resend
from typing import Optional
from sqlalchemy import text
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from db.models.clientes import Clientes
from db.models.favoritos import Favoritos
from db.models.registro_precios import RegistroPrecios, RegistroPreciosCrear, RegistroPreciosEdit
from services.productos import clean_cache as clean_productos_cache
from db.models.productos import Productos
cache_promos = None
tiempo_cache_promos = 0
tiempo_expiracion = 300

def clean_registros_cache():
    global cache_promos
    cache_promos = None
    clean_productos_cache()

def get_registros_precios(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ):
    global cache_promos, tiempo_cache_promos
    tiempo_actual = time.time()
    if cache_promos is not None and (tiempo_actual - tiempo_cache_promos) < tiempo_expiracion:
        print("cargando promociones desde cache")
        lista_completa = cache_promos
    else:
        print("cargando promociones desde base")
        lista_completa = db.query(RegistroPrecios).order_by(RegistroPrecios.created_at.desc()).all()
        cache_promos = lista_completa
        tiempo_cache_promos = tiempo_actual
    return lista_completa[skip : skip + limit]

def get_historial_registros_precios(
    db:Session,
    busqueda_promocion: Optional[str] = None,
    orden: Optional[int] = None,
    fecha_inicio_max: Optional[datetime] = None,
    fecha_inicio_min: Optional[datetime] = None,
    fecha_fin_max: Optional[datetime] = None,
    fecha_fin_min: Optional[datetime] = None,
    precio_nuevo_min: Optional[int] = None,
    precio_nuevo_max: Optional[int] = None,
    precio_anterior_min: Optional[int] = None,
    precio_anterior_max: Optional[int] = None,
    porcentaje_descuento_min: Optional[int] = None,
    porcentaje_descuento_max: Optional[int] = None,
    es_promocion: Optional[bool] = None,
    promo_activa: Optional[bool] = None,
    bool_activo: Optional[bool] = None,
    filtrocat: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
):
    if orden == 1:
        query = text("SELECT * from get_all_promociones () order by nombre asc")
    elif orden == 2:
        query = text("SELECT * from get_all_promociones () order by nombre desc")
    elif orden == 3:
        query = text("SELECT * from get_all_promociones () order by fecha_inicio asc")
    elif orden == 4:
        query = text("SELECT * from get_all_promociones () order by fecha_inicio desc")
    elif orden == 5:
        query = text("SELECT * from get_all_promociones () order by fecha_fin asc")
    elif orden == 6:
        query = text("SELECT * from get_all_promociones () order by fecha_fin desc")
    elif orden == 7:
        query = text("SELECT * from get_all_promociones () order by precio_nuevo asc")
    elif orden == 8:
        query = text("SELECT * from get_all_promociones () order by precio_nuevo desc")
    elif orden == 9:
        query = text("SELECT * from get_all_promociones () order by precio_anterior asc")
    elif orden == 10:
        query = text("SELECT * from get_all_promociones () order by precio_anterior desc")
    elif orden == 11:
        query = text("SELECT * from get_all_promociones () order by porcentaje_descuento asc")
    elif orden == 12:
        query = text("SELECT * from get_all_promociones () order by porcentaje_descuento desc")
    elif orden == 13:
        query = text("SELECT * from get_all_promociones () order by categoria asc")
    elif orden == 14:
        query = text("SELECT * from get_all_promociones () order by categoria desc")
    else:
        query = text("SELECT * from get_all_promociones () order by created_at desc")
    db_promocion = db.execute(query).mappings().all()
    if not db_promocion:
        return []
    db_precios = {}
    for i in db_promocion:
        id_promocion = i["id"]
        if id_promocion not in db_precios:
            db_precios[id_promocion] = {
                "id": id_promocion,
                "id_producto": i["id_producto"],
                "motivo": i["motivo"],
                "precio_nuevo": i["precio_nuevo"],
                "precio_anterior": i["precio_anterior"],
                "porcentaje_descuento": i["porcentaje_descuento"],
                "fecha_inicio": i["fecha_inicio"],
                "fecha_fin": i["fecha_fin"],
                "es_promocion": i.get("es_promocion", i.get("en_promocion", False)),
                "activa": i["activa"],
                "nombre": i["nombre"],
                "created_at": i["created_at"],
                "categoria": i["categoria"],
                "codigo_barra": i["codigo_barra"],
                "activo": i["activo"]
            }
    lista_promociones = list(db_precios.values())
    if busqueda_promocion is not None:
        busqueda = busqueda_promocion.lower() 
        lista_filtrada = []
        for promocion in lista_promociones:
            nombre = promocion["nombre"].lower() if promocion["nombre"] else ""
            codigo_barra = promocion["codigo_barra"].lower() if promocion["codigo_barra"] else ""
            motivo = promocion["motivo"].lower() if promocion["motivo"] else ""
            if (busqueda in nombre or busqueda in codigo_barra or busqueda in motivo):
                lista_filtrada.append(promocion)
        lista_promociones = lista_filtrada
    if bool_activo is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion["activo"] == bool_activo:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if es_promocion is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion["es_promocion"] == es_promocion:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if promo_activa is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion["activa"] == promo_activa:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if filtrocat is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion["categoria"] == filtrocat:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if precio_nuevo_max is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion.get("precio_nuevo") is not None and promocion["precio_nuevo"] <= precio_nuevo_max:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
        
    if precio_nuevo_min is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion.get("precio_nuevo") is not None and promocion["precio_nuevo"] >= precio_nuevo_min:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
        
    if precio_anterior_max is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion.get("precio_anterior") is not None and promocion["precio_anterior"] <= precio_anterior_max:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
        
    if precio_anterior_min is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion.get("precio_anterior") is not None and promocion["precio_anterior"] >= precio_anterior_min:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if fecha_inicio_max is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion["fecha_inicio"] <= fecha_inicio_max:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if fecha_inicio_min is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion["fecha_inicio"] >= fecha_inicio_min:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if fecha_fin_max is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion["fecha_fin"] <= fecha_fin_max:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if fecha_fin_min is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion["fecha_fin"] >= fecha_fin_min:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if porcentaje_descuento_max is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion.get("porcentaje_descuento") is not None and promocion["porcentaje_descuento"] <= porcentaje_descuento_max:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    if porcentaje_descuento_min is not None:
        lista_temporal = []
        for promocion in lista_promociones:
            if promocion.get("porcentaje_descuento") is not None and promocion["porcentaje_descuento"] >= porcentaje_descuento_min:
                lista_temporal.append(promocion)
        lista_promociones = lista_temporal
    return lista_promociones[skip : skip + limit]

def get_registros_precios_activas(
    db: Session
):
    return db.query(RegistroPrecios).filter(
        RegistroPrecios.fecha_inicio <= func.now(),
        RegistroPrecios.fecha_fin >= func.now(),
        RegistroPrecios.activa == True,
        RegistroPrecios.es_promocion == True
    ).all()

def create_registros_precios(
    db: Session, 
    promocion: RegistroPreciosCrear
):
    db_producto = db.query(Productos).filter(Productos.id == promocion.id_producto).first()
    if not db_producto:
        return None
    precio_base = float(db_producto.precio)
    precio_nuevo = promocion.precio_nuevo
    porcentaje = promocion.porcentaje_descuento
    if porcentaje is not None and precio_nuevo is None:
        precio_nuevo = precio_base - (precio_base * (porcentaje / 100.0))
    elif precio_nuevo is not None and porcentaje is None:
        porcentaje = int(round(((precio_base - precio_nuevo) / precio_base) * 100))
    nueva_promo = RegistroPrecios(
        id_producto=promocion.id_producto,
        motivo=promocion.motivo,
        precio_nuevo=precio_nuevo,
        precio_anterior=precio_base,
        porcentaje_descuento=porcentaje,
        fecha_inicio=promocion.fecha_inicio,
        fecha_fin=promocion.fecha_fin,
        es_promocion=True,
        activa=True
    )
    db.add(nueva_promo)
    db.commit()
    db.refresh(nueva_promo)
    resend.api_key = os.getenv("RESEND_API_KEY")
    print(f"--- LOG RESEND: API KEY configurada: {bool(resend.api_key)} ---")
    clientes_favoritos = (
        db.query(Clientes)
        .join(Favoritos, Clientes.id == Favoritos.id_cliente)
        .filter(Favoritos.id_producto == promocion.id_producto)
        .all()
    )
    print(f"--- LOG RESEND: Se encontraron {len(clientes_favoritos)} clientes para notificar ---")
    for cliente in clientes_favoritos:
        html_correo = f"""
            <div style="font-family: sans-serif; 
            max-width: 600px; margin: auto; padding: 20px; 
            border: 1px solid #e5e7eb; border-radius: 12px;"
            >
                    <h2 style="color: #166534; text-align: center;">
                    🔥 ¡Tu favorito bajó de precio!
                    </h2>
                    <p style="color: #374151; font-size: 16px;">
                    Hola 
                    <b>
                    {cliente.nombre}
                    </b>,
                    </p>
                    <p style="color: #374151; font-size: 16px;">
                    El producto 
                    <b>
                    {db_producto.nombre}
                    </b> 
                    que tienes en tu lista de deseos acaba de entrar en promoción.
                    </p>
                <div style="background-color: #f0fdf4; 
                padding: 15px; border-radius: 8px; 
                text-align: center; margin: 20px 0;"
                >
                    <p style="color: #6b7280; text-decoration: line-through; margin: 0;">
                    Precio anterior: ${precio_base:,.2f}
                    </p>
                    <p style="color: #dc2626; font-size: 24px; font-weight: 900; margin: 5px 0;">
                    ${precio_nuevo:,.2f}
                    </p>
                    <span style="background-color: #22c55e; color: white; 
                    padding: 4px 8px; border-radius: 4px; 
                    font-weight: bold; font-size: 14px;"
                    >
                    {porcentaje}% OFF
                    </span>
                </div>
                <p style="color: #374151; text-align: center;">
                <i>
                Motivo: {promocion.motivo or 'Oferta especial'}
                </i>
                </p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://pedidos-maxi.vercel.app/" 
                    style="background-color: #166534; color: white; 
                    padding: 12px 24px; text-decoration: none; 
                    border-radius: 8px; font-weight: bold; display: inline-block;"
                    >
                    ¡Aprovechar Oferta!
                    </a>
                </div>
            </div>
        """
        try:
            print(f"--- LOG RESEND: Intentando enviar a {cliente.email} ---")
            respuesta_resend = resend.Emails.send({
                "from": "onboarding@resend.dev", 
                "to": cliente.email,
                "subject": f"¡Oferta del {porcentaje}% en {db_producto.nombre}!",
                "html": html_correo
            })
            print(f"--- LOG RESEND: Correo enviado exitosamente! Respuesta: {respuesta_resend} ---")
        except Exception as e:
            print(f"--- ❌ ERROR CRÍTICO RESEND a {cliente.email}: {str(e)} ---")
    clean_registros_cache()
    return nueva_promo

def update_registros_precios(
    db: Session, 
    id_promocion: int, 
    promocion: RegistroPreciosEdit
):
    db_promo = db.query(RegistroPrecios).filter(RegistroPrecios.id == id_promocion).first()
    if not db_promo:
        return None
    update_data = promocion.model_dump(exclude_unset=True)
    if 'precio_nuevo' in update_data or 'porcentaje_descuento' in update_data:
        precio_base = float(db_promo.precio_anterior) 
        nuevo_precio = update_data.get('precio_nuevo', db_promo.precio_nuevo)
        nuevo_porcentaje = update_data.get('porcentaje_descuento', db_promo.porcentaje_descuento)
        if update_data.get('porcentaje_descuento') is not None and update_data.get('precio_nuevo') is None:
            nuevo_precio = precio_base - (precio_base * (nuevo_porcentaje / 100.0))
            update_data['precio_nuevo'] = nuevo_precio
        elif update_data.get('precio_nuevo') is not None and update_data.get('porcentaje_descuento') is None:
            nuevo_porcentaje = int(round(((precio_base - nuevo_precio) / precio_base) * 100))
            update_data['porcentaje_descuento'] = nuevo_porcentaje 
    for key, value in update_data.items():
        setattr(db_promo, key, value)
    db.commit()
    db.refresh(db_promo)
    clean_registros_cache()
    return db_promo

def delete_promocion(
    db: Session, 
    id_promocion: int
):
    db_promo = db.query(RegistroPrecios).filter(RegistroPrecios.id == id_promocion).first()
    if db_promo is None:
        return False
    db_promo.activa = False
    db.commit()
    clean_registros_cache()
    return True
