from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime

def get_historial(
    db:Session,
    busqueda_historial: Optional[str] = None,
    fecha_upgrade_max: Optional[datetime] = None,
    fecha_upgrade_min: Optional[datetime] = None,
    precio_nuevo_min: Optional[int] = None,
    precio_nuevo_max: Optional[int] = None,
    precio_viejo_min: Optional[int] = None,
    precio_viejo_max: Optional[int] = None,
    bool_activo: Optional[bool] = None,
    filtrocat: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
):
    query = text("SELECT * from get_all_historial ()")
    db_historial = db.execute(query).mappings().all()
    if not db_historial:
        return []
    db_precios = {}
    for i in db_historial:
        id_historial = i["id"]
        if id_historial not in db_precios:
            db_precios[id_historial] = {
                "id": id_historial,
                "id_producto": i["id_producto"],
                "precio_viejo": i["precio_viejo"],
                "precio_nuevo": i["precio_nuevo"],
                "updated_at": i["updated_at"],
                "nombre": i["nombre"],
                "categoria": i["categoria"],
                "codigo_barra": i["codigo_barra"],
                "activo": i["activo"]
            }
    lista_historial = list(db_precios.values())
    if busqueda_historial is not None:
        busqueda = busqueda_historial.lower() 
        lista_filtrada = []
        for historial in lista_historial:
            nombre = historial["nombre"].lower() if historial["nombre"] else ""
            codigo_barra = historial["codigo_barra"].lower() if historial["codigo_barra"] else ""
            if (busqueda in nombre or busqueda in codigo_barra):
                lista_filtrada.append(historial)
        lista_historial = lista_filtrada
    if bool_activo is not None:
        lista_temporal = []
        for historial in lista_historial:
            if historial["activo"] == bool_activo:
                lista_temporal.append(historial)
        lista_historial = lista_temporal
    if filtrocat is not None:
        lista_temporal = []
        for historial in lista_historial:
            if historial["categoria"] == filtrocat:
                lista_temporal.append(historial)
        lista_historial = lista_temporal
    if precio_nuevo_max is not None:
        lista_temporal = []
        for historial in lista_historial:
            if historial["precio_nuevo"] <= precio_nuevo_max:
                lista_temporal.append(historial)
        lista_historial = lista_temporal
    if precio_nuevo_min is not None:
        lista_temporal = []
        for historial in lista_historial:
            if historial["precio_nuevo"] >= precio_nuevo_min:
                lista_temporal.append(historial)
        lista_historial = lista_temporal
    if precio_viejo_max is not None:
        lista_temporal = []
        for historial in lista_historial:
            if historial["precio_viejo"] <= precio_viejo_max:
                lista_temporal.append(historial)
        lista_historial = lista_temporal
    if precio_viejo_min is not None:
        lista_temporal = []
        for historial in lista_historial:
            if historial["precio_viejo"] >= precio_viejo_min:
                lista_temporal.append(historial)
        lista_historial = lista_temporal
    if fecha_upgrade_max is not None:
        lista_temporal = []
        for historial in lista_historial:
            if historial["updated_at"] <= fecha_upgrade_max:
                lista_temporal.append(historial)
        lista_historial = lista_temporal
    if fecha_upgrade_min is not None:
        lista_temporal = []
        for historial in lista_historial:
            if historial["updated_at"] >= fecha_upgrade_min:
                lista_temporal.append(historial)
        lista_historial = lista_temporal
    return lista_historial[skip : skip + limit]
