from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.productos import Productos_Respuesta, Productos_Crear, Productos_Edit, ArchivoCrear, Productos_Categoria, Productos_Imagenes
from services import productos as crud
router = APIRouter()


@router.get(
        "/producto/", 
        response_model= list[Productos_Imagenes], 
        tags=["Sección de Productos"]
)
def read_producto(
        limit: int = 21,
        skip: int = 0, 
        db: Session = Depends(get_db), 
        busqueda_producto: Optional[str] = None,
        filtrocat: Optional[str] = None,
        precio_producto_min: Optional[int] = None,
        precio_producto_max: Optional[int] = None,
        bool_activo: Optional[bool] = None
    ):
    db_producto = crud.get_producto(
        db, 
        busqueda_producto=busqueda_producto,
        filtrocat=filtrocat,
        precio_producto_min=precio_producto_min,
        precio_producto_max=precio_producto_max,
        bool_activo=bool_activo,
        limit=limit,
        skip=skip
    )
    return db_producto

@router.get(
        "/producto/categorias/", 
        response_model= list[Productos_Categoria], 
        tags=["Sección de Productos"]
)
def read_categoria(
        db: Session = Depends(get_db)
    ):
    db_producto = crud.get_categoria(
        db
    )
    return db_producto

@router.get(
        "/productos/", 
        response_model=list[Productos_Respuesta], 
        tags=["Sección de Productos"]
)
def read_productos(
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    productos = crud.get_productos(
        db, 
        limit=limit
    )
    return productos

@router.post(
        "/productos/", 
        response_model=Productos_Respuesta, 
        tags=["Sección de Productos"]
)
def create_producto(
    producto: Productos_Crear, 
    db: Session = Depends(get_db)
):
    return crud.create_producto(
        db=db, 
        producto=producto
    )

@router.post(
        "/productos/archivos/", 
        response_model=ArchivoCrear, 
        tags=["Sección de Productos"]
)
def create_archivo(
    archivo: ArchivoCrear, 
    db: Session = Depends(get_db)
):
    return crud.create_archivo(
        db=db, 
        archivo=archivo
    )

@router.put(
        "/productos/id/{id_producto}", 
        response_model=Productos_Respuesta, 
        tags=["Sección de Productos"]
)
def update_producto(
    id_producto: int, 
    producto: Productos_Edit, 
    db: Session = Depends(get_db)
):
    db_producto = crud.update_producto(
        db, 
        id_producto=id_producto, 
        producto=producto
    )
    if db_producto is None:
        raise HTTPException(
            status_code=404, 
            detail="Producto no encontrado"
        )
    return db_producto

@router.delete(
        "/productos/id/{id_producto}", 
        tags=["Sección de Productos"]
)
def delete_producto(
    id_producto: int, 
    db: Session = Depends(get_db)
):
    success = crud.delete_producto(
        db, 
        id_producto=id_producto
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Producto no encontrado"
        )
    return {"detail": "Producto eliminado"}

@router.delete(
        "/productos/archivos/id/{id_archivo}", 
        tags=["Sección de Productos"]
)
def delete_archivo(
    id_archivo: int, 
    db: Session = Depends(get_db)
):
    success = crud.delete_archivo(
        db, 
        id_archivo=id_archivo
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Archivo no encontrado"
        )
    return {"detail": "Archivo eliminado"}