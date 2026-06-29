from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.usuarios import Usuarios_Respuesta, Usuarios_Crear, Usuarios_Login, Token,Usuarios_Direcciones, Usuarios_Edit
from services import usuarios as crud
router = APIRouter()



@router.get(
        "/usuarios/", 
        response_model= list[Usuarios_Direcciones], 
        tags=["Sección de Usuarios"]
)
def read_usuario(
        limit: int = 20,
        skip: int = 0, 
        db: Session = Depends(get_db),
        busqueda_usuario: Optional[str] = None,
        orden: Optional[int] = None,
        bool_activo: Optional[bool] = None,
    ):
    db_usuario = crud.get_usuario(
        db,
        busqueda_usuario=busqueda_usuario,
        orden=orden,
        bool_activo=bool_activo,
        limit=limit,
        skip=skip
    )
    return db_usuario

@router.post(
        "/usuario/login/",
        response_model=Token,
        tags=["Seccion de Usuarios"]
)
def login_usuario(
    pase: Usuarios_Login, 
    db: Session = Depends(get_db)
):
    usuario, id_usuario, id_rol = crud.login_usuarios(
        db,
        pase
    )
    if not usuario:
        raise HTTPException(
            status_code=401, 
            detail="E-Mail o Contraseña Invalido"
        )
    return {
        "access_token": usuario, 
        "token_type": "bearer",
        "id_usuario": id_usuario,
        "id_rol": id_rol
        }
    
@router.post(
        "/usuarios/", 
        response_model=Usuarios_Respuesta, 
        tags=["Sección de Usuarios"]
)
def create_usuario(
    usuario: Usuarios_Crear, 
    db: Session = Depends(get_db)
):
    db_usuario_email = crud.get_mail_usuario(
        db, 
        email_usuario=usuario.email
    )
    if db_usuario_email:
        raise HTTPException(
            status_code=400, 
            detail="Email ya registrado"
        )
    db_usuario_dni = crud.get_dni_usuario(
        db, 
        dni_usuario=usuario.dni
    )
    if db_usuario_dni:
        raise HTTPException(
            status_code=400, 
            detail="DNI ya registrado"
        )
    return crud.create_usuario(
        db=db, 
        usuario=usuario
    )

@router.put(
        "/usuarios/id/{id_usuario}", 
        response_model=Usuarios_Respuesta, 
        tags=["Sección de Usuarios"]
)
def update_usuario(
    id_usuario: int, 
    usuario: Usuarios_Edit, 
    db: Session = Depends(get_db)
):
    if usuario.email is not None:
        db_usuarios_email = crud.get_mail_usuario(
            db, 
            email_usuario=usuario.email
        )
        if db_usuarios_email and id_usuario != db_usuarios_email[0].id:
            raise HTTPException(
                status_code=400, 
                detail="Email ya registrado"
            )
    db_usuario = crud.update_usuario(
        db, 
        id_usuario=id_usuario, 
        usuario=usuario
    )
    if db_usuario is None:
        raise HTTPException(
            status_code=404, 
            detail="Usuario no encontrado"
        )
    return db_usuario

@router.delete(
        "/usuarios/id/{id_usuario}", 
        tags=["Sección de Usuarios"]
)
def delete_usuario(
    id_usuario: int, 
    db: Session = Depends(get_db)
):
    success = crud.delete_usuario(
        db, 
        id_usuario=id_usuario
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Usuario no encontrado"
        )
    return {"detail": "Usuario eliminado"}
