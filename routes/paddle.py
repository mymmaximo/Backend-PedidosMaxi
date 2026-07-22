import httpx
import os
from dotenv import load_dotenv
from db.database import get_db
from sqlalchemy.orm import Session
from db.models.productos import Productos
from fastapi import APIRouter, HTTPException, Depends
from db.models.detalles_pedido import Detalles_Pedido

load_dotenv()
router = APIRouter()

PADDLE_SECRETO = os.getenv("PADDLE_SECRETO", "").strip()
PADDLE_WEBHOOK_SECRETO = os.getenv("PADDLE_WEBHOOK_SECRETO", "").strip()

@router.post("/crear-transaccion-paddle/")
def crear_transaccion(
    datos_pedido: dict,
    db: Session = Depends(get_db)
):
    id_pedido = datos_pedido.get("id_pedido")
    if not id_pedido:
        raise HTTPException(
            status_code=400, 
            detail="Falta el id_pedido"
        )
    detalles = db.query(Detalles_Pedido).filter(Detalles_Pedido.id_pedido == id_pedido).all()
    if not detalles:
        raise HTTPException(
            status_code=404, 
            detail="El pedido no tiene detalles"
        )
    items_paddle = []
    for detalle in detalles:
        productos = db.query(Productos).filter(Productos.id == detalle.id_producto).first()
        nombre_producto = productos.nombre if productos else "Producto sin Nombre"
        precio_centavos = str(int(detalle.precio_unitario * 100))
        items_paddle.append({
            "quantity": detalle.cantidad,
            "price": {
                "description": nombre_producto,
                "unit_price": {
                    "amount": precio_centavos,
                    "currency_code": "USD"
                },
                "product": {
                    "name": nombre_producto,
                    "tax_category": "standard"
                }
            }
        })
    url = "https://sandbox-api.paddle.com/transactions"
    headers = {
        "Authorization": f"Bearer {PADDLE_SECRETO}",
        "Content-Type": "application/json"
    }
    payload = {
        "items": items_paddle,
        "custom_data": {
            "id_pedido": str(id_pedido)
        }
    }
    
    response = httpx.post(
        url, 
        json=payload, 
        headers=headers
    )

    if response.status_code not in [200, 201]:
        print("--- ❌ ERROR DETALLADO DE PADDLE ---")
        print(response.text)
        raise HTTPException(status_code=400, detail=response.json())
        
    data = response.json()
    return {"transaction_id": data["data"]["id"]}