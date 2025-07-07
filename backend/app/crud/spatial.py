from sqlalchemy.orm import Session
from app.models.spatial import SpatialData
from app.schemas.spatial import SpatialDataCreate
from typing import List, Optional

def create_spatial_data(db: Session, data: SpatialDataCreate) -> SpatialData:
    """Create a new spatial data record."""
    db_spatial = SpatialData(
        name=data.name,
        geom=data.geom,
        properties=data.properties or {}
    )
    db.add(db_spatial)
    db.commit()
    db.refresh(db_spatial)
    return db_spatial

def get_spatial_data_within_bounds(
    db: Session, 
    minx: float, 
    miny: float, 
    maxx: float, 
    maxy: float
) -> List[SpatialData]:
    """Get spatial data within specified bounds."""
    from sqlalchemy import text
    
    query = text("""
        SELECT * FROM spatial_data 
        WHERE ST_Within(geom, ST_MakeEnvelope(:minx, :miny, :maxx, :maxy, 4326))
    """)
    
    result = db.execute(query, {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy})
    return result.fetchall()

def get_spatial_data_by_id(db: Session, spatial_id: int) -> Optional[SpatialData]:
    """Get spatial data by ID."""
    return db.query(SpatialData).filter(SpatialData.id == spatial_id).first()

def get_all_spatial_data(db: Session, skip: int = 0, limit: int = 100) -> List[SpatialData]:
    """Get all spatial data with pagination."""
    return db.query(SpatialData).offset(skip).limit(limit).all() 