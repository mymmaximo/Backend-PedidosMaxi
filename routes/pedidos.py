import os
import hmac
import hashlib
import secrets
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.pedidos import Pedidos_Respuesta, Pedidos_Crear, Pedidos_Detalles, Pedidos_CDDP, Pedidos_DDP
from db.models.detalles_pedido import Detalles_Pedido_Crear, Detalles_Pedido_Respuesta
from db.models.clientes import Clientes
from services.direcciones import get_direccion
from services import pedidos as crud
from services import detalles_pedidos as servi
from sec import verificar_token
from fastapi.security import OAuth2PasswordBearer
from sec import obtener_usuario_actual
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="cliente/login")
PADDLE_SECRETO = os.getenv("PADDLE_SECRETO")
PADDLE_WEBHOOK_SECRETO = os.getenv("PADDLE_WEBHOOK_SECRETO", "")

@router.get(
    "/pedido/", 
    response_model= list[Pedidos_Respuesta], 
    tags=["Sección de Pedidos"]
)
def read_pedido(
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual), 
    id_pedido: Optional[int] = None,
    id_cliente_pedido: Optional[int] = None,
    id_direccion_pedido: Optional[int] = None,
    metodo_pago_pedido: Optional[str] = None
    ):
    db_pedido = crud.get_pedido(
        db, 
        id_pedido=id_pedido,
        id_cliente_pedido=id_cliente_pedido,
        id_direccion_pedido=id_direccion_pedido,
        metodo_pago_pedido=metodo_pago_pedido
    )
    if not db_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido no encontrado"
        )
    true_cliente = usuario_logeado.get("id_cliente") == db_pedido[0].id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 6])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    return db_pedido

@router.get(
    "/pedidos/producto/{id_producto}",
    response_model= list[Pedidos_Detalles],
    tags=["Sección de Pedidos"]
)
def read_producto_pedido(
    id_producto: int,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    db_pedidos = crud.get_pedidoxproducto(
        db,
        id_producto
    )
    if db_pedidos is False: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producto no encontrado"
        )
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 6])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    return db_pedidos

@router.get(
    "/pedidos/cliente/{id_cliente}",
    response_model= list[Pedidos_DDP],
    tags=["Sección de Pedidos"]
)
def read_pedido_cliente(
    id_cliente: int,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual),
    busqueda_pedido: Optional[str] = None,
    orden: Optional[int] = None,
    filtromp: Optional[str] = None,
):
    true_cliente = usuario_logeado.get("id_cliente") == id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    db_pedidos = crud.get_pedidoxcliente(
        db,
        id_cliente=id_cliente,
        busqueda_pedido=busqueda_pedido,
        orden=orden,
        filtromp=filtromp,
    )
    return db_pedidos

@router.get(
    "/pedidos/{id_pedido}",
    response_model= list[Pedidos_CDDP],
    tags=["Sección de Pedidos"]
)
def read_pedido_producto(
    id_pedido: int,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    db_pedidos = crud.get_pedidoxid_pedido(
        db,
        id_pedido
    )
    if db_pedidos is False: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido no encontrado"
        )
    true_cliente = usuario_logeado.get("id_cliente") == db_pedidos.id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 6])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    return db_pedidos

@router.get(
    "/pedidos/", 
    response_model=list[Pedidos_Respuesta], 
    tags=["Sección de Pedidos"]
)
def read_pedidos_old(
    limit: int = 100, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 6])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    db_pedidos = crud.get_pedidos(
        db, 
        limit=limit
    )
    return db_pedidos 

@router.get(
    "/pedidos/all/",
    response_model= list[Pedidos_CDDP],
    tags=["Sección de Pedidos"]
)
def read_pedidos(
    limit: int = 20,
    skip: int = 0, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual),
    busqueda_pedido: Optional[str] = None,
    orden: Optional[int] = None,
    filtromp: Optional[str] = None,
    filtroest: Optional[int] = None,
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 6])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    db_pedidos = crud.get_all_pedidos(
        db, 
        busqueda_pedido=busqueda_pedido,
        orden=orden,
        filtromp=filtromp,
        filtroest=filtroest,
        limit=limit,
        skip=skip
    )
    return db_pedidos 

@router.post(
    "/pedidos/", 
    response_model=Pedidos_Respuesta, 
    tags=["Sección de Pedidos"]
)
def create_pedido(
    nuevo_pedido: Pedidos_Crear,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    true_cliente = usuario_logeado.get("id_cliente") == nuevo_pedido.id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    db_pedidos = crud.create_pedido(
        db=db,
        pedido=nuevo_pedido
    )
    db.commit()
    db.refresh(db_pedidos)
    return db_pedidos

@router.post(
    "/pedidos/detalles_pedido/", 
    response_model=list[Detalles_Pedido_Respuesta], 
    tags=["Sección de Detalles de Pedidos"]
)
def create_detalles_pedido(
    detalle_pedido: list[Detalles_Pedido_Crear],
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    if not detalle_pedido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La lista de detalles no puede estar vacía"
        )
    db_pedido  = crud.get_pedido(
        db, 
        id_pedido=detalle_pedido[0].id_pedido
    )
    if not db_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido no encontrado"
        )
    pedidios = db_pedido[0]
    true_cliente = usuario_logeado.get("id_cliente") == pedidios.id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    db_detalle = servi.create_detalle_pedido(
        db=db,
        detalle_pedido=detalle_pedido
    )
    db.commit()
    return db_detalle

@router.put(
    "/pedidos/id/{id_pedido}", 
    response_model=Pedidos_Respuesta, 
    tags=["Sección de Pedidos"]
)
def update_pedido(
    id_pedido: int, 
    pedido: Pedidos_Crear, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    db_cliente = db.query(Clientes).filter(Clientes.id == pedido.id_cliente).first()
    if not db_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado"
        )
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 6])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    db_direccion = get_direccion(
        db, 
        id_direccion=pedido.id_direccion
    )
    if not db_direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Direccion no encontrada"
        )
    return crud.update_pedido(
        db, 
        id_pedido=id_pedido, 
        pedido=pedido
    )

@router.delete(
    "/pedidos/id/{id_pedido}", 
    tags=["Sección de Pedidos"]
)
def delete_pedido(
    id_pedido: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3, 6])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    success = crud.delete_pedido(
        db, 
        id_pedido=id_pedido
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido no encontrado"
        )
    return {"detail": "Pedido eliminado"}

@router.post(
    "/webhook/paddle",
    tags=["Webhooks"]
)
async def webhook_paddle(
    payload: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    firma = request.headers.get("paddle-signature")
    if not firma:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Headers no encontrado"
        )
    try:
        partes = dict(item.split("=") for item in firma.split(";"))
        ts = partes.get("ts")
        h1 = partes.get("h1")
        cuerpo_crudo = await request.body()
        payload_sfirma = f"{ts}:".encode('utf-8') + cuerpo_crudo
        firma_calculada = hmac.new(
            PADDLE_WEBHOOK_SECRETO.encode('utf-8'), 
            payload_sfirma, 
            hashlib.sha256
        ).hexdigest() 
        compa = secrets.compare_digest(h1, firma_calculada)
        if not compa:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Firma inválida"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Error validando firma: {str(e)}"
        )
    evento = payload.get("event_type")
    if evento == "transaction.completed":
        datos_transaccion = payload.get("data", {})
        id_pedido_str = datos_transaccion.get("custom_data", {}).get("id_pedido")
        if not id_pedido_str:
            return {
                "status": "ok",
                "message": "Ignorado: no tiene Id de Pedido"
            }
        id_pedido = int(id_pedido_str)
        transaccion_id = datos_transaccion.get("id")
        datos_recibo = datos_transaccion.get("receipt_data")
        if datos_recibo:
            url_recibo = datos_recibo.get("receipt_url", "")
        else:
            url_recibo = ""
        monto_pagado_paddle = None
        total_pagado_str = datos_transaccion.get("details", {}).get("totals", {}).get("total")
        if total_pagado_str:
            monto_pagado_paddle = float(total_pagado_str) / 100.0
        detalle_pago = "Paddle"
        pagos = datos_transaccion.get("payments", [])
        if pagos:
            tipo_metodo = pagos[0].get("method_details", {}).get("type", "")
            if tipo_metodo == "card":
                last4 = pagos[0].get("method_details", {}).get("card", {}).get("last4", "")
                detalle_pago = f"Tarjeta terminada en {last4}"
            else:
                detalle_pago = tipo_metodo.capitalize() 
        paycon = crud.confirmar_pago(
            db, 
            id_pedido=id_pedido,
            transaccion_id=transaccion_id,
            url_recibo=url_recibo,
            detalle_pago=detalle_pago,
            monto_pagado=monto_pagado_paddle
        )
        if paycon:
            return {"status": "ok"} 
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Pedido no encontrado"
            )
    return {"status": "ok", "message": "Evento ignorado"}