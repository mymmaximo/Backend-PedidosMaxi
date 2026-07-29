import os
import hashlib
from fastapi import HTTPException, Request, status, Depends
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from jose import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext
from db.database import get_db 
from db.models.usuarios import Usuarios as ModeloUsuario

load_dotenv()

ARMA_SECRETA = os.getenv("ARMA_SECRETA")
ALGORITMO = os.getenv("ALGORITMO")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def crear_huella(
        request: Request
) -> str:
    ip_real = request.headers.get("X-Forwarded-For")
    if ip_real:
        ip = ip_real.split(",")[0].strip()
    else:
        ip = request.client.host if request.client else "0.0.0.0"
    navegador = request.headers.get(
        "user-agent", 
        "Desconocido"
    )
    huella_cruda = f"{ip}-{navegador}"
    return hashlib.sha256(huella_cruda.encode('utf-8')).hexdigest()[:16]

def crear_pase(
        datos: dict
):
    encripto = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=120)
    encripto.update({
        "exp": expira
    })
    final_token = jwt.encode(
        encripto, 
        ARMA_SECRETA, 
        algorithm=ALGORITMO
    )
    return final_token

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

def obtener_usuario_actual(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("token_seguro")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se encontró el token de sesión legítimo."
        )
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El Acceso es inválido o ha expirado."
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

def verifica_sena(
        contrasena_plana: str,
        contrasena_hash: str
):
    verificado = pwd_context.verify(
        contrasena_plana,
        contrasena_hash
    )
    return verificado
    
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