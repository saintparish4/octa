from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.tasks.geospatial_tasks import process_large_dataset, calculate_network_metrics, cache_spatial_data
from app.services.analysis import GeospatialAnalyzer
from celery.result import AsyncResult
from typing import Dict, Any

router = APIRouter()

@router.post("/process-dataset/")
async def start_dataset_processing(dataset_id: str) -> Dict[str, Any]:
    """Start processing a large geospatial dataset asynchronously."""
    try:
        task = process_large_dataset.delay(dataset_id)
        return {
            "task_id": task.id,
            "status": "started",
            "message": f"Dataset processing started for {dataset_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start processing: {str(e)}")

@router.post("/calculate-network-metrics/")
async def start_network_analysis(network_id: str) -> Dict[str, Any]:
    """Start network metrics calculation asynchronously."""
    try:
        task = calculate_network_metrics.delay(network_id)
        return {
            "task_id": task.id,
            "status": "started",
            "message": f"Network analysis started for {network_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")

@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get the status of a background task."""
    try:
        task_result = AsyncResult(task_id)
        
        if task_result.state == 'PENDING':
            response = {
                'task_id': task_id,
                'state': task_result.state,
                'status': 'Task is pending...'
            }
        elif task_result.state == 'PROGRESS':
            response = {
                'task_id': task_id,
                'state': task_result.state,
                'status': task_result.info.get('step', 'Processing...'),
                'progress': task_result.info.get('current', 0),
                'total': task_result.info.get('total', 100)
            }
        elif task_result.state == 'SUCCESS':
            response = {
                'task_id': task_id,
                'state': task_result.state,
                'result': task_result.result
            }
        else:
            response = {
                'task_id': task_id,
                'state': task_result.state,
                'error': str(task_result.info)
            }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get task status: {str(e)}")

@router.post("/cache-spatial-data/{spatial_id}")
async def cache_spatial_data_endpoint(spatial_id: int) -> Dict[str, Any]:
    """Cache spatial data for faster retrieval."""
    try:
        task = cache_spatial_data.delay(spatial_id)
        return {
            "task_id": task.id,
            "status": "started",
            "message": f"Caching started for spatial data ID {spatial_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start caching: {str(e)}")

@router.get("/spatial-statistics/")
async def get_spatial_statistics() -> Dict[str, Any]:
    """Get spatial data statistics."""
    analyzer = GeospatialAnalyzer()
    return analyzer.get_spatial_statistics()

@router.get("/detect-hotspots/")
async def detect_hotspots(radius_km: float = 1.0) -> Dict[str, Any]:
    """Detect spatial hotspots."""
    analyzer = GeospatialAnalyzer()
    return analyzer.detect_hotspots(radius_km) 