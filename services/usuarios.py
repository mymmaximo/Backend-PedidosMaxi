from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Request
from db.models.usuarios import Usuarios, Usuarios_Crear, Usuarios_Login, Usuarios_Edit
from sec import get_contrasena_criptid, verifica_sena, crear_pase, crear_huella


def get_usuario(
    db:Session,
    busqueda_usuario: Optional[str] = None,
    orden: Optional[int] = None,
    bool_activo: Optional[bool] = None,
    limit: int = 20,
    skip: int = 0
):
    if orden == 1:
        query = text("SELECT * from get_all_usuarios () order by nombre asc")
    elif orden == 2:
        query = text("SELECT * from get_all_usuarios () order by nombre desc")
    elif orden == 3:
        query = text("SELECT * from get_all_usuarios () order by id_rol asc")
    elif orden == 4:
        query = text("SELECT * from get_all_usuarios () order by id_rol desc")
    elif orden == 5:
        query = text("SELECT * from get_all_usuarios () order by created_at asc")
    elif orden == 6:
        query = text("SELECT * from get_all_usuarios () order by created_at desc")
    else:
        query = text("SELECT * from get_all_usuarios () order by id_rol asc")
    db_usuario = db.execute(query).mappings().all()
    if not db_usuario:
        return []
    db_usuarios = {}
    for i in db_usuario:
        id_usuarioh = i["id_usuario"]
        if id_usuarioh not in db_usuarios:
            db_usuarios[id_usuarioh] = {
                "id": id_usuarioh,
                "nombre": i["nombre"],
                "email": i["email"],
                "dni": i["dni"],
                "id_rol": i["id_rol"],
                "activo": i["activo"],
                "created_at": i["created_at"]
            }
    lista_usuarios = list(db_usuarios.values())
    if busqueda_usuario is not None:
        busqueda = busqueda_usuario.lower() 
        lista_filtrada = []
        for usuario in lista_usuarios:
            nombre = usuario["nombre"].lower() if usuario["nombre"] else ""
            email = usuario["email"].lower() if usuario["email"] else ""
            dni = usuario["dni"].lower() if usuario["dni"] else ""
            if (busqueda in nombre or busqueda in email or busqueda in dni):
                lista_filtrada.append(usuario)
        lista_usuarios = lista_filtrada
    if bool_activo is not None:
        lista_temporal = []
        for usuario in lista_usuarios:
            if usuario["activo"] == bool_activo:
                lista_temporal.append(usuario)
        lista_usuarios = lista_temporal
    return lista_usuarios[skip : skip + limit]

def get_dni_usuario(
        db: Session,
        dni_usuario: Optional[str] = None
    ):
    resultado = db.query(Usuarios)
    if dni_usuario is not None:
        resultado = resultado.filter(
            Usuarios.dni == dni_usuario
        )
    return resultado.all()

def get_mail_usuario(
        db: Session,
        email_usuario: Optional[str] = None
    ):
    resultado = db.query(Usuarios)
    if email_usuario is not None:
        resultado = resultado.filter(
            Usuarios.email == email_usuario
        )
    return resultado.all()

def get_usuarios(
        db: Session, 
        limit: int = 100
    ):
    return db.query(Usuarios).limit(limit).all()

def login_usuarios(
        db: Session,
        pase: Usuarios_Login,
        request: Request
):
    usuario_db = db.query(Usuarios).filter(
        Usuarios.email == pase.email
        ).first()
    if not usuario_db:
        return None, None, None
    contrasena_valida = verifica_sena(
        pase.contrasena, 
        usuario_db.contrasena
    )
    if not contrasena_valida:
        return None, None, None
    roles_query = db.execute(
        text("SELECT id_rol FROM usuarios_roles WHERE id_usuario = :uid"), 
        {"uid": usuario_db.id}
    ).fetchall()
    lista_roles = [r[0] for r in roles_query]
    payload_data = {
        "id_usuario": usuario_db.id,
        "id_rol": lista_roles,
        "huella": crear_huella(request)
    }
    token = crear_pase(datos=payload_data)
    return token, usuario_db.id, lista_roles

def create_usuario(
        db: Session, 
        usuario: Usuarios_Crear
    ):
    datos_usuario = usuario.dict()
    roles = datos_usuario.pop("id_rol")
    contrasena_plana = datos_usuario.pop("contrasena")
    contrasena_hash = get_contrasena_criptid(contrasena_plana)
    datos_usuario["contrasena"] = contrasena_hash
    db_usuario = Usuarios(**datos_usuario)
    db.add(db_usuario)
    db.flush()
    for rol in roles:
        db.execute(
            text("INSERT INTO usuarios_roles (id_usuario, id_rol) VALUES (:uid, :rid)"), 
            {"uid": db_usuario.id, "rid": rol}
        )
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(
        db: Session, 
        id_usuario: int, 
        usuario: Usuarios_Edit
    ):
    db_usuario = db.query(Usuarios).filter(Usuarios.id == id_usuario).first()
    if not db_usuario:
        return None
    usuarios_act = usuario.dict(exclude_unset=True)
    roles_nuevos = usuarios_act.pop("id_rol", None)
    for key, value in usuarios_act.items():
        if key == "contrasena":
            contrasena_hash = get_contrasena_criptid(usuario.contrasena)
            value = contrasena_hash
        setattr(db_usuario, key, value)
    if roles_nuevos is not None:
        db.execute(
            text("DELETE FROM usuarios_roles WHERE id_usuario = :uid"), 
            {"uid": id_usuario}
        )
        for rol in roles_nuevos:
            db.execute(
                text("INSERT INTO usuarios_roles (id_usuario, id_rol) VALUES (:uid, :rid)"), 
                {"uid": id_usuario, "rid": rol}
            )
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(
        db: Session, 
        id_usuario: int
    ):
    db_usuario = db.query(Usuarios).filter(Usuarios.id == id_usuario).first()
    if db_usuario is None:
        return False
    db_usuario.activo = not db_usuario.activo
    db.commit()
    db.refresh(db_usuario)
    return True
