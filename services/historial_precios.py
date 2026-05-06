from typing import Optional
from sqlalchemy import text, or_
from sqlalchemy.orm import Session
from db.models.historial_precios import historial_wproductos, Historial_Precios

def get_cliente(
        db: Session, 
        id_historial: Optional[int] = None,
        busqueda_producto: Optional[str] = None,
        limit: int = 20,
        skip: int = 0
    ):
    resultado = db.query(historial_wproductos)
    if id_historial is not None:
        resultado = resultado.filter(
            Historial_Precios.id == id_historial 
        )
    if busqueda_producto is not None:
        resultado = resultado.filter(
            or_(
                resultado.nombre.ilike(f"%{busqueda_producto}%"),
                resultado.apellido.ilike(f"%{busqueda_producto}%"),
                resultado.dni.ilike(f"%{busqueda_producto}%"),
                resultado.email.ilike(f"%{busqueda_producto}%")
            ) 
        )
    listcliente = []
    rta = resultado.offset(skip).limit(limit).all()
    for i in rta:
        direccionfori = get_cliente_id_direccion(db, i.id)
        if bool_direccion is not None:
            if bool_direccion != bool(direccionfori):
                continue
        if bool_activo is not None:
            if bool_activo != i.activo:
                continue
        clientesa = {
            "id": i.id,
            "nombre": i.nombre,
            "apellido": i.apellido,
            "email": i.email,
            "dni": i.dni,
            "usuario": i.usuario,
            "id_rol": i.id_rol,
            "created_at": i.created_at,
            "updated_at": i.updated_at,
            "direcciones": direccionfori,
            "activo": i.activo
        }
        listcliente.append(clientesa)
    return listcliente
