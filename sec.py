import os
import hashlib
from jose import jwt
from slowapi import Limiter
from db.database import get_db
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from db.models.usuarios import Usuarios as ModeloUsuario
from fastapi import HTTPException, Request, status, Depends

load_dotenv()

ARMA_SECRETA = os.getenv("ARMA_SECRETA")
ALGORITMO = os.getenv("ALGORITMO")

# Codigo. {Contexto Encriptado}
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Codigo. {Conseguir IP del Cliente}
def obtener_ip_real(
    request: Request
) -> str:
    ip_cliente = request.headers.get(
        "x-forwarded-for", 
        request.headers.get(
            "x-real-ip", 
            request.client.host if request.client else "127.0.0.1"
        )
    )
    if "," in ip_cliente:
        ip_cliente = ip_cliente.split(",")[0].strip()
    return ip_cliente
limiter = Limiter(key_func=obtener_ip_real)

# Codigo. {Crear Firma Digital}
def crear_huella(
        request: Request
) -> str:
    navegador = request.headers.get(
        "user-agent", 
        "Desconocido"
    )
    ip_cliente = request.headers.get(
        "x-forwarded-for", 
        request.headers.get(
            "x-real-ip", 
            request.client.host if request.client else "IP_Desconocida"
        )
    )
    if "," in ip_cliente:
        ip_cliente = ip_cliente.split(",")[0].strip()
    idioma = request.headers.get(
        "accept-language", 
        "Desconocido"
    )
    huella_cruda = f"{ip_cliente}|{navegador}|{idioma}" 
    return hashlib.sha256(huella_cruda.encode('utf-8')).hexdigest()[:16]

# Codigo. {Crear Pase Digital}
def crear_pase(
        datos: dict,
        request: Request = None
):
    encripto = datos.copy()
    if request:
        encripto.update({
            "huella": crear_huella(request)
        })
    expira = datetime.now(timezone.utc) + timedelta(hours=2)
    encripto.update({
        "exp": expira
    })
    final_token = jwt.encode(
        encripto, 
        ARMA_SECRETA, 
        algorithm=ALGORITMO
    )
    return final_token

# Codigo. {Leer Contraseña Desencriptada}
def get_contrasena_criptid(
        contrasena_plana: str
    ):
    contrasena_segura = contrasena_plana[:72]
    contrasena_hash = pwd_context.hash(
        contrasena_segura
    )
    return (
        contrasena_hash
    )

# Codigo. {Leer Usuario con Sesion Iniciada}
def obtener_usuario_actual(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("token_seguro")
    sesion_activa = request.cookies.get("sesion_activa")
    if not token:
        if sesion_activa == "true":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="SESION_EXPIRADA"
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se encontró el token de sesión legítimo."
        )
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="SESION_EXPIRADA"
        )
    huella_actual = crear_huella(request)
    huella_guardada = payload.get("huella")
    if huella_guardada and huella_guardada != huella_actual:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El Acceso es inválido o ha expirado."
        )
    if payload.get("id_usuario"):        
        usuario_db = db.query(ModeloUsuario).filter(ModeloUsuario.id == payload.get("id_usuario")).first()
        if not usuario_db:
            raise HTTPException (
                status_code=403,
                detail="No se encontró el usuario."
            )
        if hasattr(usuario_db, 'activo') and not usuario_db.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario desactivado."
            )
    return payload

# Codigo. {Verificar Contraseña}
def verifica_sena(
        contrasena_plana: str,
        contrasena_hash: str
):
    verificado = pwd_context.verify(
        contrasena_plana,
        contrasena_hash
    )
    return verificado

# Codigo. {Verificar de Token}
def verificar_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            ARMA_SECRETA,
            algorithms=[ALGORITMO]
        )
        return payload
    except Exception as e:
        print("\n" + "="*30)
        print("🚨 FALLO AL VERIFICAR TOKEN 🚨")
        print(f"Motivo del error: {e}")
        print(f"Token recibido: {token[:20]}... (cortado)")
        print(f"Arma Secreta cargada: {ARMA_SECRETA}")
        print(f"Algoritmo cargado: {ALGORITMO}")
        print("="*30 + "\n")
        return None