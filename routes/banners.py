from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models.banners import Banners_Respuesta, Banners_Crear, Banners_Edit
from services import banners as crud
router = APIRouter()

@router.get(
        "/banners/", 
        response_model=list[Banners_Respuesta], 
        tags=["Sección de Banners"]
)
def read_banners(
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    banners = crud.get_banners(
        db, 
        limit=limit
    )
    return banners

@router.post(
        "/banners/", 
        response_model=Banners_Respuesta, 
        tags=["Sección de Banners"]
)
def create_banners(
    banner: Banners_Crear, 
    db: Session = Depends(get_db)
):
    return crud.create_banner(
        db=db, 
        banner=banner
    )

@router.put(
        "/banners/id/{id_banner}", 
        response_model=Banners_Respuesta, 
        tags=["Sección de Banners"]
)
def update_banners(
    id_banner: int, 
    banner: Banners_Edit, 
    db: Session = Depends(get_db)
):
    db_banner = crud.update_banner(
        db, 
        id_banner=id_banner, 
        banner=banner
    )
    if db_banner is None:
        raise HTTPException(
            status_code=404, 
            detail="Banners no encontrado"
        )
    return db_banner

@router.delete(
        "/banners/id/{id_banner}", 
        tags=["Sección de Banners"]
)
def delete_banners(
    id_banner: int, 
    db: Session = Depends(get_db)
):
    success = crud.delete_banner(
        db, 
        id_banner=id_banner
    )
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Banner no encontrado"
        )
    return {"detail": "Banner eliminado"}