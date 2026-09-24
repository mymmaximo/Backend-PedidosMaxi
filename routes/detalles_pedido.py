from typing import Optional
from db.database import get_db
from sqlalchemy.orm import Session
from sec import obtener_usuario_actual
from services.pedidos import get_pedido
from services.productos import get_producto
from services import detalles_pedidos as crud
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.detalles_pedido import Detalles_Pedido_Respuesta, Detalles_Pedido_Crear
router = APIRouter()


# Codigo. {Leer 1 Detalle de Pedido}
@router.get(
    "/detalle_pedido/", 
    response_model= list[Detalles_Pedido_Respuesta], 
    tags=["Sección de Detalles de Pedidos"]
)
def read_detalle_pedido(
    db: Session = Depends(get_db), 
    usuario_logeado: dict = Depends(obtener_usuario_actual),
    id_detalle_pedido: Optional[int] = None,
    id_producto_detalle_pedido: Optional[int] = None,
    id_pedido_detalle_pedido: Optional[int] = None
):
    # Verificacion. {Cliente, Administrador, Gestor de Precios}
    true_cliente = usuario_logeado.get("id_cliente") == db_pedido[0].id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Leer 1 Detalle de Pedido}
    db_detalle_pedido = crud.get_detalle_pedido(
        db, 
        id_detalle_pedido=id_detalle_pedido,
        id_producto_detalle_pedido=id_producto_detalle_pedido,
        id_pedido_detalle_pedido=id_pedido_detalle_pedido
    )
    if not db_detalle_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Detalle de Pedido no encontrado"
        )
    # Service. {Obtener Pedido Correspondiente al Detalle}
    db_pedido = get_pedido(
        db, 
        id_pedido=db_detalle_pedido[0].id_pedido
    )
    if not db_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido no encontrado"
        )
    return db_detalle_pedido

# Codigo. {Leer Todos los Detalles de Pedidos}
@router.get(
    "/detalles_pedido/", 
    response_model=list[Detalles_Pedido_Respuesta], 
    tags=["Sección de Detalles de Pedidos"]
)
def read_detalles_pedido(
    limit: int = 100, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Cliente, Administrador, Gestor de Precios}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Leer Todos los Detalles de Pedidos}
    detalles_pedido = crud.get_detalles_pedido(
        db,
        limit=limit
    )
    return detalles_pedido

# Codigo. {Crear Detalle de Pedido}
@router.post(
    "/detalles_pedidos/", 
    response_model=list[Detalles_Pedido_Respuesta], 
    tags=["Sección de Detalles de Pedidos"]
)
def create_detalle_pedido(
    detalle_pedido: list[Detalles_Pedido_Crear], 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Cliente}
    true_cliente = usuario_logeado.get("id_cliente") == db_pedidios.id_cliente
    if not (true_cliente):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Verificacion. {Lista de Detalles Vacia}
    if not detalle_pedido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La lista de detalles está vacía"
        )
    # Service. {Obtener Pedido para los Detalles}
    id_pedidios = detalle_pedido[0].id_pedido
    db_pedido = get_pedido(
        db, 
        id_pedido=id_pedidios
    )
    if not db_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido no encontrado"
        )
    db_pedidios = db_pedido[0] if isinstance(db_pedido, list) else db_pedido
    # Service. {Crear los Detalles de Pedidos}
    resultado = crud.create_detalle_pedido(
        db=db,
        detalle_pedido=detalle_pedido
    )
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Uno o más productos no fueron encontrados en la base de datos"
        )
    return resultado

# Codigo. {Actualizar Detalle de Pedido}
@router.put(
    "/detalles_pedido/id/{id_detalle_pedido}", 
    response_model=Detalles_Pedido_Respuesta, 
    tags=["Sección de Detalles de Pedidos"]
)
def update_detalle_pedido(
    id_detalle_pedido: int, 
    detalle_pedido: Detalles_Pedido_Crear,
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Cliente, Administrador, Gestor de Precios}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Obtener Pedido para los Detalles}
    db_pedido = get_pedido(
        db, 
        id_pedido=detalle_pedido.id_pedido
    )
    if not db_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Pedido no encontrado"
        )
    # Service. {Obtener Producto para los Detalles}
    db_producto = get_producto(
        db, 
        id_producto=detalle_pedido.id_producto
    )
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producto no encontrado"
        )
    # Service. {Actualizar Detalle de Pedido}
    db_detalle_actualizado = crud.update_detalle_pedido(
        db, 
        id_detalle_pedido=id_detalle_pedido, 
        detalle_pedido=detalle_pedido
    )
    if not db_detalle_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Detalle de Pedido no encontrado"
        )
    return db_detalle_actualizado

# Codigo. {Borrar Detalle de Pedido}
@router.delete(
    "/detalles_pedido/id/{id_detalle_pedido}", 
    tags=["Sección de Detalles de Pedidos"]
)
def delete_detalle_pedido(
    id_detalle_pedido: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Cliente, Administrador, Gestor de Precios}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Borrar Detalle de Pedido}
    success = crud.delete_detalle_pedido(
        db, 
        id_detalle_pedido=id_detalle_pedido
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Detalle de Pedido no encontrado"
        )
    return {"detail": "Detalle de Pedido eliminado"}
