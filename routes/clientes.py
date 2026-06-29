from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.clientes import Clientes_Respuesta, Clientes_Crear, Clientes_Login, Token,Clientes_Direcciones, Clientes_id_Direccion, Clientes_Edit
from services import clientes as crud
router = APIRouter()



@router.get(
        "/cliente/", 
        response_model= list[Clientes_Direcciones], 
        tags=["Sección de Clientes"]
)
def read_cliente(
        limit: int = 20,
        skip: int = 0, 
        db: Session = Depends(get_db),
        busqueda_cliente: Optional[str] = None,
        orden: Optional[int] = None,
        bool_direccion: Optional[bool] = None,
        bool_activo: Optional[bool] = None,
        filtrociudad: Optional[str] = None,
        filtroprovincia: Optional[str] = None
    ):
    db_cliente = crud.get_cliente(
        db,
        busqueda_cliente=busqueda_cliente,
        orden=orden,
        bool_direccion=bool_direccion,
        bool_activo=bool_activo,
        filtrociudad=filtrociudad,
        filtroprovincia=filtroprovincia,
        limit=limit,
        skip=skip
    )
    return db_cliente

@router.get(
        "/cliente/{id_cliente}/direcciones/", 
        response_model= list[Clientes_id_Direccion], 
        tags=["Sección de Clientes"]
)
def get_cliente_idireccion(
    id_cliente: int, 
    db: Session = Depends(get_db), 
):
    cliente = crud.get_cliente_id_direccion(
        db,
        id_cliente
    )
    return cliente

@router.get(
        "/clientes/", 
        response_model=list[Clientes_Direcciones], 
        tags=["Sección de Clientes"]
)
def read_clientes(
    db: Session = Depends(get_db), 
):
    clientes = crud.get_cliente_direccion(
        db,
    )
    return clientes

@router.post(
        "/cliente/login/",
        response_model=Token,
        tags=["Seccion de Clientes"]
)
def login_cliente(
    pase: Clientes_Login, 
    db: Session = Depends(get_db)
):
    cliente, id_cliente = crud.login_clientes(
        db,
        pase
    )
    if not cliente:
        raise HTTPException(
            status_code=401, 
            detail="E-Mail o Contraseña Invalido"
        )
    return {
        "access_token": cliente, 
        "token_type": "bearer",
        "id_cliente": id_cliente,
        }
    
@router.post(
        "/clientes/", 
        response_model=Clientes_Respuesta, 
        tags=["Sección de Clientes"]
)
def create_cliente(
    cliente: Clientes_Crear, 
    db: Session = Depends(get_db)
):
    db_cliente_email = crud.get_mail(
        db, 
        email_cliente=cliente.email
    )
    if db_cliente_email:
        raise HTTPException(
            status_code=400, 
            detail="Email ya registrado"
        )
    db_cliente_dni = crud.get_dni(
        db, 
        dni_cliente=cliente.dni
    )
    if db_cliente_dni:
        raise HTTPException(
            status_code=400, 
            detail="DNI ya registrado"
        )
    return crud.create_cliente(
        db=db, 
        cliente=cliente
    )

@router.put(
        "/clientes/id/{id_cliente}", 
        response_model=Clientes_Respuesta, 
        tags=["Sección de Clientes"]
)
def update_cliente(
    id_cliente: int, 
    cliente: Clientes_Edit, 
    db: Session = Depends(get_db)
):
    if cliente.email is not None:
        db_cliente_email = crud.get_mail(
            db, 
            email_cliente=cliente.email
        )
        if db_cliente_email and id_cliente != db_cliente_email[0].id:
            raise HTTPException(
                status_code=400, 
                detail="Email ya registrado"
            )
    db_cliente = crud.update_cliente(
        db, 
        id_cliente=id_cliente, 
        cliente=cliente
    )
    if db_cliente is None:
        raise HTTPException(
            status_code=404, 
            detail="Cliente no encontrado"
        )
    return db_cliente

@router.delete(
        "/clientes/id/{id_cliente}", 
        tags=["Sección de Clientes"]
)
def delete_cliente(
    id_cliente: int, 
    db: Session = Depends(get_db)
):
    success = crud.delete_cliente(
        db, 
        id_cliente=id_cliente
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Cliente no encontrado"
        )
    return {"detail": "Cliente eliminado"}
