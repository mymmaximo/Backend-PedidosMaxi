from typing import Optional
from db.database import get_db
from sqlalchemy.orm import Session
from services import productos as crud
from sec import obtener_usuario_actual
from fastapi import APIRouter, Depends, HTTPException, status
from db.models.productos import Productos_Respuesta, Productos_Crear, Productos_Edit, ArchivoCrear, Productos_Categoria, Productos_Imagenes
router = APIRouter()

# Codigo. {Leer todos los Productos}
@router.get(
    "/producto/", 
    response_model=list[Productos_Imagenes], 
    tags=["Sección de Productos"]
)
def read_producto(
    db: Session = Depends(get_db),
    limit: int = 24,
    skip: int = 0, 

    busqueda_producto: Optional[str] = None,
    orden: Optional[int] = None,

    precio_producto_min: Optional[int] = None,
    precio_producto_max: Optional[int] = None,
    porcentaje_descuento_min: Optional[int] = None,
    filtrocat: Optional[str] = None,
    bool_activo: Optional[bool] = None,
    bool_promocion: Optional[bool] = None
):
    # Service. {Leer todos los Productos}
    db_producto = crud.get_producto(
        db, 
        limit=limit,
        skip=skip,

        busqueda_producto=busqueda_producto,
        orden=orden,

        precio_producto_min=precio_producto_min,
        precio_producto_max=precio_producto_max,
        porcentaje_descuento_min=porcentaje_descuento_min,
        filtrocat=filtrocat,
        bool_activo=bool_activo,
        bool_promocion=bool_promocion
    )
    return db_producto

# Codigo. {Leer Categorias}
@router.get(
    "/producto/categorias/", 
    response_model=list[Productos_Categoria], 
    tags=["Sección de Productos"]
)
def read_categoria(
    db: Session = Depends(get_db)
):
    # Service. {Leer Categorias}
    db_producto = crud.get_categoria(
        db
    )
    return db_producto

# Codigo. {Leer todos Productos (Version Vieja)}
@router.get(
    "/productos/", 
    response_model=list[Productos_Respuesta], 
    tags=["Sección de Productos"]
)
def read_productos(
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # Service. {Leer todos Productos (Version Vieja)}
    productos = crud.get_productos(
        db, 
        limit=limit
    )
    return productos

# Codigo. {Crear Producto}
@router.post(
    "/productos/", 
    response_model=Productos_Respuesta, 
    tags=["Sección de Productos"]
)
def create_producto(
    producto: Productos_Crear, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Crear Producto}
    return crud.create_producto(
        db=db, 
        producto=producto
    )

# Codigo. {Crear Imagen}
@router.post(
    "/productos/archivos/", 
    response_model=ArchivoCrear, 
    tags=["Sección de Productos"]
)
def create_archivo(
    archivo: ArchivoCrear, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Crear Imagen}
    return crud.create_archivo(
        db=db, 
        archivo=archivo
    )

# Codigo. {Actualizar Producto}
@router.put(
    "/productos/id/{id_producto}", 
    response_model=Productos_Respuesta, 
    tags=["Sección de Productos"]
)
def update_producto(
    id_producto: int, 
    producto: Productos_Edit, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administracion}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Actualizar Producto}
    db_producto = crud.update_producto(
        db, 
        id_producto=id_producto, 
        producto=producto
    )
    if db_producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producto no encontrado"
        )
    return db_producto

# Codigo. {Desactivar Producto}
@router.delete(
    "/productos/id/{id_producto}", 
    tags=["Sección de Productos"]
)
def delete_producto(
    id_producto: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Precios}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Desactivar Producto}
    success = crud.delete_producto(
        db, 
        id_producto=id_producto
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Producto no encontrado"
        )
    return {"detail": "Producto eliminado"}

# Codigo. {Borrar Imagen del Producto}
@router.delete(
    "/productos/archivos/id/{id_archivo}", 
    tags=["Sección de Productos"]
)
def delete_archivo(
    id_archivo: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Precios}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 3])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    # Service. {Borrar Imagen del Producto}
    success = crud.delete_archivo(
        db, 
        id_archivo=id_archivo
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Archivo no encontrado"
        )
    return {"detail": "Archivo eliminado"}