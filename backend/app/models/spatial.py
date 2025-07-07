from sqlalchemy import Column, Integer, String, DateTime, Text, func, JSON, Float
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional, Dict, Any
from datetime import datetime
from app.db.base import Base

class SpatialData(Base):
    """Spatial data model for storing geographic points with properties."""
    
    __tablename__ = "spatial_data"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    properties = Column(JSONB, nullable=True, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<SpatialData(id={self.id}, name='{self.name}')>"
    
    @property
    def coordinates(self) -> Optional[tuple[float, float]]:
        """Extract coordinates from latitude and longitude."""
        if hasattr(self, 'latitude') and hasattr(self, 'longitude'):
            return (self.latitude, self.longitude)
        return None