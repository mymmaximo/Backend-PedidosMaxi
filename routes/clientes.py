from typing import Optional
from db.database import get_db
from sqlalchemy.orm import Session
from services import clientes as crud
from sec import crear_pase, obtener_usuario_actual, crear_huella, limiter
from fastapi import HTTPException, APIRouter, Response, Request, status, Depends
from db.models.clientes import Clientes_Respuesta, Clientes_Crear, Clientes_Login, Clientes_Direcciones, Clientes_id_Direccion, Clientes_Edit
router = APIRouter()

# Codigo. {Leer 1 Cliente}
@router.get(
    "/cliente/", 
    response_model= list[Clientes_Direcciones], 
    tags=["Sección de Clientes"]
)
def read_cliente(
    limit: int = 20,
    skip: int = 0, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual),

    id_cliente: Optional[int] = None,
    orden: Optional[int] = None,
    busqueda_cliente: Optional[str] = None,
    
    filtroprovincia: Optional[str] = None,
    filtrociudad: Optional[str] = None,
    bool_activo: Optional[bool] = None,
    bool_direccion: Optional[bool] = None
):
    # Verificacion. {Administrador, Gestor de Pedidos General}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 7])
    true_cliente = usuario_logeado.get("id_cliente")
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los privilegios necesarios para hacer esto."
        )
    if true_cliente and not true_rol:
        id_cliente=true_cliente
        busqueda_cliente = None
        orden = None
        bool_direccion = None
        bool_activo = None
        filtrociudad = None
        filtroprovincia = None
        limit = 1000
    # Service. {Leer  Cliente}
    db_cliente = crud.get_cliente(
        db,
        busqueda_cliente=busqueda_cliente,
        id_cliente=id_cliente,
        orden=orden,
        bool_direccion=bool_direccion,
        bool_activo=bool_activo,
        filtrociudad=filtrociudad,
        filtroprovincia=filtroprovincia,
        limit=limit,
        skip=skip
    )
    return db_cliente

# Codigo. {Conseguir Direccion de Cliente}
@router.get(
    "/cliente/{id_cliente}/direcciones/", 
    response_model= list[Clientes_id_Direccion], 
    tags=["Sección de Clientes"]
)
def get_cliente_idireccion(
    id_cliente: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Pedidos General}
    true_cliente = usuario_logeado.get("id_cliente") == id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 7])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar este perfil."
        )
    # Service. {Conseguir Direccion de Cliente}
    cliente = crud.get_cliente_id_direccion(
        db,
        id_cliente
    )
    return cliente

# Codigo. {Leer Todos los Clientes con sus Direcciones}
@router.get(
    "/clientes/", 
    response_model=list[Clientes_Direcciones], 
    tags=["Sección de Clientes"]
)
def read_clientes(
    db: Session = Depends(get_db), 
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Pedidos General}
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 7])
    if not (true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar este perfil."
        )
    # Service. {Leer Todos los Clientes con sus Direcciones}
    clientes = crud.get_cliente_direccion(
        db
    )
    return clientes

# Codigo. {Iniciar Sesion como Cliente}
@router.post(
    "/cliente/login/",
    tags=["Seccion de Clientes"]
)
@limiter.limit("5/minute")
def login_cliente(
    pase: Clientes_Login, 
    response: Response,
    request: Request,
    db: Session = Depends(get_db)
):
    # Service. {Iniciar Sesion como Cliente}
    cliente, id_cliente = crud.login_clientes(
        db,
        pase
    )
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="E-Mail o Contraseña Invalido"
        )
    payload_data = {
        "id_cliente": id_cliente,
        "es_cliente": True,
        "huella": crear_huella(request)
    }
    token_seguro = crear_pase(
        datos=payload_data
    )
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
        "id_cliente": id_cliente
    }
    
# Codigo. {Registrar Cliente}
@router.post(
    "/clientes/", 
    response_model=Clientes_Respuesta, 
    tags=["Sección de Clientes"]
)
def create_cliente(
    cliente: Clientes_Crear, 
    db: Session = Depends(get_db)
):
    # Service. {Verificar Mail Repetido}
    db_cliente_email = crud.get_mail(
        db, 
        email_cliente=cliente.email
    )
    if db_cliente_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email ya registrado"
        )
    # Service. {Registrar Cliente}
    db_cliente_dni = crud.get_dni(
        db, 
        dni_cliente=cliente.dni
    )
    if db_cliente_dni:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="DNI ya registrado"
        )
    return crud.create_cliente(
        db=db, 
        cliente=cliente
    )

# Codigo. {Actualizar Datos del Cliente}
@router.put(
    "/clientes/id/{id_cliente}", 
    response_model=Clientes_Respuesta, 
    tags=["Sección de Clientes"]
)
def update_cliente(
    id_cliente: int, 
    cliente: Clientes_Edit, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Pedidos General}
    true_cliente = usuario_logeado.get("id_cliente") == id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 7])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar este perfil."
        )
    # Service. {Verificar Mail Repetido}
    if cliente.email is not None:
        db_cliente_email = crud.get_mail(
            db, 
            email_cliente=cliente.email
        )
        if db_cliente_email and id_cliente != db_cliente_email[0].id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email ya registrado"
            )
    # Service. {Actualizar Datos del Cliente}
    db_cliente = crud.update_cliente(
        db, 
        id_cliente=id_cliente, 
        cliente=cliente
    )
    if db_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_not_FOUND, 
            detail="Cliente no encontrado"
        )
    return db_cliente

# Codigo. {Desactivar Cliente}
@router.delete(
    "/clientes/id/{id_cliente}", 
    tags=["Sección de Clientes"]
)
def delete_cliente(
    id_cliente: int, 
    db: Session = Depends(get_db),
    usuario_logeado: dict = Depends(obtener_usuario_actual)
):
    # Verificacion. {Administrador, Gestor de Pedidos General}
    true_cliente = usuario_logeado.get("id_cliente") == id_cliente
    roles = usuario_logeado.get("id_rol") or []
    true_rol = any(rol in roles for rol in [1, 7])
    if not (true_cliente or true_rol):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No tienes permiso para modificar este perfil."
        )
    # Verificacion. {Desactivar Cliente}
    success = crud.delete_cliente(
        db, 
        id_cliente=id_cliente
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_not_FOUND, 
            detail="Cliente no encontrado"
        )
    return {"detail": "Cliente eliminado"}
