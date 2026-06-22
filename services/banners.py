from sqlalchemy.orm import Session
from db.models.banners import Banners, Banners_Crear, Banners_Respuesta, Banners_Edit

def get_banners(
        db: Session, 
        limit: int = 100,
        bool_activo: bool = None
    ):
    db_banner = db.query(Banners)
    if bool_activo is not None:
        db_banner = db_banner.filter(Banners.activo == bool_activo)
    return db_banner.order_by(Banners.orden).limit(limit).all()

def create_banner(
        db: Session, 
        banner: Banners_Crear
    ):
    db_banner = Banners(**banner.dict())
    db.add(db_banner)
    db.commit()
    db.refresh(db_banner)
    return db_banner

def update_banner(
        db: Session,
        id_banner: int,
        banner: Banners_Edit
    ):
    db_banner = db.query(Banners).filter(Banners.id == id_banner).first()
    if not db_banner:
        return None
    banner_act = banner.dict(exclude_unset=True)
    for key, value in banner_act.items():
        setattr(db_banner, key, value)
    db.commit()
    db.refresh(db_banner)
    return db_banner

def deact_banner(
        db: Session, 
        id_banner: int
    ):
    db_banner = db.query(Banners).filter(Banners.id == id_banner).first()
    if db_banner is None:
        return False
    db_banner.activo = not db_banner.activo
    if db_banner.activo == False:
        db_banner.enlace = ""
        db_banner.orden = None
    db.commit()
    db.refresh(db_banner)
    return True

def hard_delete_banner(
        db: Session, 
        id_banner: int
    ):
    db_banner = db.query(Banners).filter(Banners.id == id_banner).first()
    if db_banner:
        db.delete(db_banner)
        db.commit()
    return db_banner