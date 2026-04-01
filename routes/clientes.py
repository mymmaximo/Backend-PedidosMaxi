from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.clientes import Clientes_Respuesta, Clientes_Crear, Clientes_Login, Token
from services import clientes as crud
router = APIRouter()



@router.get(
        "/cliente/", 
        response_model= list[Clientes_Respuesta], 
        tags=["Sección de Clientes"]
)
def read_cliente(
        db: Session = Depends(get_db), 
        id_cliente: Optional[int] = None,
        nombre_cliente: Optional[str] = None,
        apellido_cliente: Optional[str] = None,
        dni_cliente: Optional[str] = None,
        email_cliente: Optional[str] = None
    ):
    db_cliente = crud.get_cliente(
        db, 
        id_cliente=id_cliente,
        nombre_cliente=nombre_cliente,
        apellido_cliente=apellido_cliente,
        dni_cliente=dni_cliente,
        email_cliente=email_cliente
    )
    if not db_cliente:
        raise HTTPException(
            status_code=404, 
            detail="Cliente no encontrado"
        )
    return db_cliente

@router.get(
        "/clientes/", 
        response_model=list[Clientes_Respuesta], 
        tags=["Sección de Clientes"]
)
def read_clientes(
    db: Session = Depends(get_db), 
    limit: int = 100
):
    clientes = crud.get_clientes(
        db, 
        limit=limit
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
    cliente = crud.login_clientes(
        db,
        pase
    )
    if not cliente:
        raise HTTPException(
            status_code=401, 
            detail="Usuario o Contraseña Invalido"
        )
    return {"access_token": cliente, "token_type": "bearer"}
    
@router.post(
        "/clientes/", 
        response_model=Clientes_Respuesta, 
        tags=["Sección de Clientes"]
)
def create_cliente(
    cliente: Clientes_Crear, 
    db: Session = Depends(get_db)
):
    db_cliente_email = crud.get_cliente(
        db, 
        email_cliente=cliente.email
    )
    if db_cliente_email:
        raise HTTPException(
            status_code=400, 
            detail="Email ya registrado"
        )
    db_cliente_dni = crud.get_cliente(
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
    cliente: Clientes_Crear, 
    db: Session = Depends(get_db)
):
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
