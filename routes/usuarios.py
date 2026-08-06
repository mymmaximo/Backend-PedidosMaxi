from typing import Optional
from fastapi import HTTPException, APIRouter, Response, Request, status, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.usuarios import Usuarios_Respuesta, Usuarios_Crear, Usuarios_Login, Token,Usuarios_Direcciones, Usuarios_Edit
from services import usuarios as crud
from sec import crear_pase, obtener_usuario_actual, crear_huella, limiter
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
    usuario_verificado: dict = Depends(obtener_usuario_actual),
    busqueda_usuario: Optional[str] = None,
    orden: Optional[int] = None,
    bool_activo: Optional[bool] = None
    ):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los privilegios necesarios para hacer esto."
        )
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
    tags=["Seccion de Usuarios"]
)
@limiter.limit("5/minute")
def login_usuario(
    pase: Usuarios_Login, 
    response: Response,
    request: Request,
    db: Session = Depends(get_db)
):
    token_string, id_usuario, id_rol = crud.login_usuarios(
        db,
        pase,
        request
    )
    if not token_string:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="E-Mail o Contraseña Invalido"
        )
    payload_data = {
        "id_usuario": id_usuario,
        "id_rol": id_rol,
        "huella": crear_huella(request)
    }
    token_seguro = crear_pase(datos=payload_data)
    response.set_cookie(
        key="token_seguro", 
        value=token_seguro, 
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7200
    )
    return {
        "access_token": token_seguro,
        "token_type": "bearer",
        "id_usuario": id_usuario,
        "id_rol": id_rol,
    }
    
@router.post(
    "/usuarios/", 
    response_model=Usuarios_Respuesta, 
    tags=["Sección de Usuarios"]
)
def create_usuario(
    usuario: Usuarios_Crear, 
    db: Session = Depends(get_db),
    usuario_verificado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los privilegios necesarios para hacer esto."
        )
    db_usuario_email = crud.get_mail_usuario(
        db, 
        email_usuario=usuario.email
    )
    if db_usuario_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email ya registrado"
        )
    db_usuario_dni = crud.get_dni_usuario(
        db, 
        dni_usuario=usuario.dni
    )
    if db_usuario_dni:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
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
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    if usuario.email is not None:
        db_usuarios_email = crud.get_mail_usuario(
            db, 
            email_usuario=usuario.email
        )
        if db_usuarios_email and id_usuario != db_usuarios_email[0].id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email ya registrado"
            )
    db_usuario = crud.update_usuario(
        db, 
        id_usuario=id_usuario, 
        usuario=usuario
    )
    if db_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    return db_usuario

@router.delete(
    "/usuarios/id/{id_usuario}", 
    tags=["Sección de Usuarios"]
)
def delete_usuario(
    id_usuario: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar esto."
        )
    success = crud.delete_usuario(
        db, 
        id_usuario=id_usuario
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario no encontrado"
        )
    return {"detail": "Usuario eliminado"}

@router.get(
    "/reload/", 
    tags=["Autenticación"]
)
def verificar_sesion (
    response: Response,
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    payload_data = usuario_logeado.copy()
    payload_data.pop("exp", None)
    nuevo_token = crear_pase(datos=payload_data)
    response.set_cookie(
        key="token_seguro",
        value=nuevo_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7200
    )
    return {
        "id_usuario": usuario_logeado.get("id_usuario"),
        "id_rol": usuario_logeado.get("id_rol"),
        "id_cliente": usuario_logeado.get("id_cliente")
    }

@router.post(
    "/logout/", 
    tags=["Autenticación"]
)
def logout_sesion(
    response: Response
):
    response.delete_cookie(
        key="token_seguro",
        httponly=True,
        secure=True,
        samesite="none"
    )
    return {
        "mensaje": "Sesion cerrada de forma segura"
    }
