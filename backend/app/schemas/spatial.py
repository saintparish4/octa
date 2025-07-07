from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

class SpatialDataBase(BaseModel):
    name: str = Field(..., description="Name of the spatial data point")
    properties: Optional[Dict[str, Any]] = Field(default={}, description="Additional properties")

class SpatialDataCreate(SpatialDataBase):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    
    @property
    def geom(self):
        """Convert lat/lng to PostGIS geometry."""
        point = Point(self.longitude, self.latitude)
        return from_shape(point, srid=4326)

class SpatialDataResponse(SpatialDataBase):
    id: int
    coordinates: Optional[tuple[float, float]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True 