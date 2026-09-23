from sec import limiter
from routes import paddle
from fastapi import FastAPI
from db.database import Base, engine
from routes import banners as route_banners
from routes import pedidos as route_pedidos
from slowapi.errors import RateLimitExceeded
from routes import clientes as route_clientes
from routes import usuarios as route_usuarios
from routes import productos as route_productos
from routes import favoritos as route_favoritos
from slowapi import _rate_limit_exceeded_handler
from fastapi.middleware.cors import CORSMiddleware
from routes import direcciones as route_direcciones
from routes import detalles_pedido as route_detalles_pedido
from routes import registro_precios as route_registro_precios


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded, 
    _rate_limit_exceeded_handler
)

links = [
    "http://localhost:5173/",
    "https://pedidos-maxi.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://10.250.4.18:5173"
    # "link proximo"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=links,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(paddle.router)
app.include_router(route_clientes.router)
app.include_router(route_banners.router)
app.include_router(route_usuarios.router)
app.include_router(route_productos.router)
app.include_router(route_pedidos.router)
app.include_router(route_detalles_pedido.router)
app.include_router(route_favoritos.router)
app.include_router(route_direcciones.router)
app.include_router(route_registro_precios.router)

@app.get("/", tags=["Seccion 0"])
def root():
    return {"mensaje": "La Wea anda JOya"}
