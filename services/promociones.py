import time
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from db.models.promociones import Promociones, PromocionCrear, PromocionEdit
from services.productos import clean_cache as clean_productos_cache
cache_promos = None
tiempo_cache_promos = 0
tiempo_expiracion = 300

def clean_promos_cache():
    global cache_promos
    cache_promos = None
    clean_productos_cache()

def get_promociones(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ):
    global cache_promos, tiempo_cache_promos
    tiempo_actual = time.time()
    if cache_promos is not None and (tiempo_actual - tiempo_cache_promos) < tiempo_expiracion:
        print("cargando promociones desde cache")
        lista_completa = cache_promos
    else:
        print("cargando promociones desde base")
        lista_completa = db.query(Promociones).order_by(Promociones.created_at.desc()).all()
        cache_promos = lista_completa
        tiempo_cache_promos = tiempo_actual
    return lista_completa[skip : skip + limit]

def get_promociones_activas(
    db: Session
):
    return db.query(Promociones).filter(
        Promociones.fecha_inicio <= func.now(),
        Promociones.fecha_fin >= func.now()
    ).all()

def create_promocion(
    db: Session, 
    promocion: PromocionCrear
):
    nueva_promo = Promociones(**promocion.model_dump())
    db.add(nueva_promo)
    db.commit()
    db.refresh(nueva_promo)    
    clean_promos_cache()
    return nueva_promo

def update_promocion(
    db: Session, 
    id_promocion: int, 
    promocion: PromocionEdit
):
    db_promo = db.query(Promociones).filter(Promociones.id == id_promocion).first()
    if db_promo:
        update_data = promocion.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_promo, key, value)
        db.commit()
        db.refresh(db_promo)
        clean_promos_cache()
    return db_promo

def delete_promocion(
    db: Session, 
    id_promocion: int
):
    db_promo = db.query(Promociones).filter(Promociones.id == id_promocion).first()
    if db_promo is None:
        return False
    db.delete(db_promo)
    db.commit()
    clean_promos_cache()
    return True