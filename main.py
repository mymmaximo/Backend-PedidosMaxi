from fastapi import FastAPI
from db.database import Base, engine
from db.models import clientes as mod_clientes
from db.models import productos as mod_productos
from db.models import pedidos as mod_pedidos
from db.models import detalles_pedido as mod_detalles_pedido
from db.models import direcciones as mod_direcciones
from routes import clientes as route_clientes
from routes import productos as route_productos
from routes import pedidos as route_pedidos
from routes import detalles_pedido as route_detalles_pedido
from routes import direcciones as route_direcciones
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(route_clientes.router)
app.include_router(route_productos.router)
app.include_router(route_pedidos.router)
app.include_router(route_detalles_pedido.router)
app.include_router(route_direcciones.router)


@app.get("/", tags=["Seccion 0"])
def root():
    return {"mensaje": "La Wea anda JOya"}
