import os
from fastapi import HTTPException, Request, status
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

ARMA_SECRETA = os.getenv("ARMA_SECRETA")
ALGORITMO = os.getenv("ALGORITMO")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def crear_pase(
        datos: dict
):
    encripto = datos.copy()
    expira = datetime.utcnow() + timedelta(minutes=120)
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
    request: Request
):
    token = request.cookies.get("token_seguro")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se encontró la cookie de sesión legítima."
        )
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El Acceso es inválido o ha expirado."
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