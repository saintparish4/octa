from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import spatial
from app.schemas import spatial as spatial_schema

router = APIRouter()

@router.post("/spatial-data/")
def create_spatial_data(
    data: spatial_schema.SpatialDataCreate,
    db: Session = Depends(get_db),
):
    return spatial.create_spatial_data(db, data)

@router.get("/spatial-data/")
def get_all_spatial_data(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
):
    return spatial.get_all_spatial_data(db, skip=skip, limit=limit)

@router.get("/spatial-data/{spatial_id}")
def get_spatial_data_by_id(
    spatial_id: int,
    db: Session = Depends(get_db),
):
    return spatial.get_spatial_data_by_id(db, spatial_id)

@router.get("/spatial-data/within/")
def get_spatial_data_within_bounds(
    minx: float, miny: float, maxx: float, maxy: float,
    db: Session = Depends(get_db),
):
    return spatial.get_spatial_data_within_bounds(db, minx, miny, maxx, maxy)