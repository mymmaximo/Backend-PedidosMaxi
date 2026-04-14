from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.models.clientes import Clientes, Clientes_Crear, Clientes_Login, Clientes_Direccion
from sec import get_contrasena_criptid, verifica_sena, crear_pase, verificar_token

def get_cliente(
        db: Session, 
        id_cliente: Optional[int] = None,
        nombre_cliente: Optional[str] = None,
        apellido_cliente: Optional[str] = None,
        dni_cliente: Optional[str] = None,
        email_cliente: Optional[str] = None
    ):
    resultado = db.query(Clientes)
    if id_cliente is not None:
        resultado = resultado.filter(
            Clientes.id == id_cliente 
        )
    if nombre_cliente is not None:
        resultado = resultado.filter(
            Clientes.nombre == nombre_cliente
        )
    if apellido_cliente is not None:
        resultado = resultado.filter(
            Clientes.apellido == apellido_cliente
        )
    if email_cliente is not None:
        resultado = resultado.filter(
            Clientes.email == email_cliente
        )
    if dni_cliente is not None:
        resultado = resultado.filter(
            Clientes.dni == dni_cliente 
        )
    return resultado.all()

def get_clientes(
        db: Session, 
        limit: int = 100
    ):
    return db.query(Clientes).limit(limit).all()

def login_clientes(
        db: Session,
        pase: Clientes_Login
):
    cliente_db = db.query(Clientes).filter(
        Clientes.usuario == pase.usuario
        ).first()
    if not cliente_db:
        return False, False, False
    contrasena_valida = verifica_sena(
        pase.contrasena, 
        cliente_db.contrasena
    )
    if not contrasena_valida:
        return False, False, False
    token = crear_pase({"sub": str(cliente_db.id)})
    return token, cliente_db.id, cliente_db.id_rol

def get_cliente_id_direccion(
    db:Session,
    id_cliente: int
):
    query = text("SELECT * from get_only_clientes ()")
    db_cliente = db.execute(query).mappings().all()
    direcciones_list = []
    for i in db_cliente:
        if id_cliente == i["id_cliente"]:
            direcciones_list.append ({
                "id_direccion": i["id_direccion"],
                "calle": i["calle"],
                "numero": i["numero"],
                "barrio": i["barrio"],
                "ciudad": i["ciudad"],
                "provincia": i["provincia"]
            })
    return direcciones_list
    

def get_cliente_direccion(
    db: Session
):
    query = text("SELECT * from get_all_clientes ()")
    db_cliente = db.execute(query).mappings().all()
    cliente_list = {}
    for i in db_cliente:
        id_cliente = i["id_cliente"]
        if id_cliente not in cliente_list:
            cliente_list[id_cliente] = {
                "id": id_cliente,
                "nombre": i["nombre"],
                "email": i["email"],
                "dni": i["dni"],
                "apellido": i["apellido"],
                "usuario": i["usuario"],
                "id_rol": i["id_rol"],
                "direcciones": [] 
            }
        id_direcciones = []
        if i["id_direccion"] is not None:
            for e in cliente_list[id_cliente]["direcciones"]:
                id_direcciones.append(e["id_direccion"])
            if i["id_direccion"] not in id_direcciones:
                nueva_direccion = {
                    "id_direccion": i["id_direccion"],
                    "calle": i["calle"],
                    "numero": i["numero"],
                    "barrio": i["barrio"],
                    "ciudad": i["ciudad"],
                    "provincia": i["provincia"],
                }
                cliente_list[id_cliente]["direcciones"].append(nueva_direccion)
    return list(cliente_list.values())

def create_cliente(
        db: Session, 
        cliente: Clientes_Crear
    ):
    datos_cliente = cliente.dict()
    contrasena_plana = datos_cliente.pop("contrasena")
    contrasena_hash = get_contrasena_criptid(contrasena_plana)
    datos_cliente["contrasena"] = contrasena_hash
    db_cliente = Clientes(**datos_cliente)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(
        db: Session, 
        id_cliente: int, 
        cliente: Clientes_Crear
    ):
    db_cliente = db.query(Clientes).filter(Clientes.id == id_cliente).first()
    if not db_cliente:
        return None
    for key, value in cliente.dict().items():
        if key == "contrasena":
            contrasena_hash = get_contrasena_criptid(cliente.contrasena)
            value = contrasena_hash
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(
        db: Session, 
        id_cliente: int
    ):
    db_cliente = db.query(Clientes).filter(Clientes.id == id_cliente).first()
    if db_cliente is None:
        return False
    db.delete(db_cliente)
    db.commit()
    return True
