from typing import Optional
from sqlalchemy import text
from sqlalchemy.orm import Session
from db.models.clientes import Clientes, Clientes_Crear, Clientes_Login, Clientes_Edit
from sec import get_contrasena_criptid, verifica_sena, crear_pase


def get_cliente(
    db:Session,
    busqueda_cliente: Optional[str] = None,
    id_cliente: Optional[int] = None,
    orden: Optional[int] = None,
    bool_direccion: Optional[bool] = None,
    bool_activo: Optional[bool] = None,
    filtrociudad: Optional[str] = None,
    filtroprovincia: Optional[str] = None,
    limit: int = 20,
    skip: int = 0
):
    if orden == 1:
        query = text("SELECT * from get_all_clientes () order by nombre asc")
    elif orden == 2:
        query = text("SELECT * from get_all_clientes () order by nombre desc")
    elif orden == 3:
        query = text("SELECT * from get_all_clientes () order by created_at asc")
    elif orden == 4:
        query = text("SELECT * from get_all_clientes () order by created_at desc")
    else:
        query = text("SELECT * from get_all_clientes () order by created_at desc")
    db_cliente = db.execute(query).mappings().all()
    if not db_cliente:
        return []
    db_clientes = {}
    for i in db_cliente:
        id_clienshin = i["id_cliente"]
        if id_clienshin not in db_clientes:
            db_clientes[id_clienshin] = {
                "id": id_clienshin,
                "nombre": i["nombre"],
                "email": i["email"],
                "dni": i["dni"],
                "direcciones": [],
                "activo": i["activo"],
                "created_at": i["created_at"]
            }
        if i["id_direccion"] is not None:
            direccion_ditto = False
            for dir_guardada in db_clientes[id_clienshin]["direcciones"]:
                if dir_guardada["id_direccion"] == i["id_direccion"]:
                    direccion_ditto = True
                    break
            if direccion_ditto == False:
                nueva_direccion = {
                    "id_direccion": i["id_direccion"],
                    "calle": i["calle"],
                    "numero": i["numero"],
                    "barrio": i["barrio"],
                    "ciudad": i["ciudad"],
                    "provincia": i["provincia"]
                }
                db_clientes[id_clienshin]["direcciones"].append(nueva_direccion)
    lista_clientes = list(db_clientes.values())
    if id_cliente is not None:
        lista_temporal = []
        for cliente in lista_clientes:
            if cliente["id"] == id_cliente:
                lista_temporal.append(cliente)
        lista_clientes = lista_temporal
    if busqueda_cliente is not None:
        busqueda = busqueda_cliente.lower() 
        lista_filtrada = []
        for cliente in lista_clientes:
            nombre = cliente["nombre"].lower() if cliente["nombre"] else ""
            email = cliente["email"].lower() if cliente["email"] else ""
            dni = cliente["dni"].lower() if cliente["dni"] else ""
            encontrado_en_direccion = False
            for direccion in cliente["direcciones"]:
                calle = direccion["calle"].lower() if direccion["calle"] else ""
                barrio = direccion["barrio"].lower() if direccion["barrio"] else ""
                ciudad = direccion["ciudad"].lower() if direccion["ciudad"] else ""
                provincia = direccion["provincia"].lower() if direccion["provincia"] else ""
                if (busqueda in calle or busqueda in barrio or busqueda in ciudad or busqueda in provincia):
                    encontrado_en_direccion = True
                    break
            if (busqueda in nombre or busqueda in email or busqueda in dni or encontrado_en_direccion):
                lista_filtrada.append(cliente)
        lista_clientes = lista_filtrada
    if bool_activo is not None:
        lista_temporal = []
        for cliente in lista_clientes:
            if cliente["activo"] == bool_activo:
                lista_temporal.append(cliente)
        lista_clientes = lista_temporal
    if bool_direccion is not None:
        if bool_direccion:
            lista_temporal = []
            for cliente in lista_clientes:
                if filtrociudad is not None or filtroprovincia is not None:
                    for direcciones in cliente["direcciones"]:
                        if direcciones["ciudad"] == filtrociudad or direcciones["provincia"] == filtroprovincia:
                            lista_temporal.append(cliente)
                            break
                elif cliente["direcciones"] != []:
                    lista_temporal.append(cliente)
            lista_clientes = lista_temporal
        else:
            lista_temporal = []
            for cliente in lista_clientes:
                if cliente["direcciones"] == []:
                    lista_temporal.append(cliente)
            lista_clientes = lista_temporal
    return lista_clientes[skip : skip + limit]

def get_mail(
        db: Session,
        email_cliente: Optional[str] = None
    ):
    resultado = db.query(Clientes)
    if email_cliente is not None:
        resultado = resultado.filter(
            Clientes.email == email_cliente
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
        Clientes.email == pase.email
        ).first()
    if not cliente_db:
        return False, False
    contrasena_valida = verifica_sena(
        pase.contrasena, 
        cliente_db.contrasena
    )
    if not contrasena_valida:
        return False, False
    token = crear_pase({"sub": str(cliente_db.id)})
    return token, cliente_db.id

def get_cliente_id_direccion(
    db:Session,
    id_cliente: int
):
    query = text("SELECT * from get_only_clientes ()")
    db_cliente = db.execute(query).mappings().all()
    direcciones_list = []
    id_direcciones = []
    for i in db_cliente:
        if id_cliente == i["id_cliente"]:
            if i["id_direccion"] is not None:
                if i["id_direccion"] not in id_direcciones:
                    direcciones_list.append ({
                        "id_direccion": i["id_direccion"],
                        "calle": i["calle"],
                        "numero": i["numero"],
                        "barrio": i["barrio"],
                        "ciudad": i["ciudad"],
                        "provincia": i["provincia"]
                    })
                    id_direcciones.append(i["id_direccion"])
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
                "activo": i["activo"],
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

def get_dni(
    db: Session, 
    dni_cliente: str
):
    return db.query(Clientes).filter(Clientes.dni == dni_cliente).first()

def update_cliente(
        db: Session, 
        id_cliente: int, 
        cliente: Clientes_Edit
    ):
    db_cliente = db.query(Clientes).filter(Clientes.id == id_cliente).first()
    if not db_cliente:
        return None
    clientes_act = cliente.dict(exclude_unset=True)
    for key, value in clientes_act.items():
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
    db_cliente.activo = not db_cliente.activo
    db.commit()
    db.refresh(db_cliente)
    return True
