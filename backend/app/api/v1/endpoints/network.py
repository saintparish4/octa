from fastapi import APIRouter, Depends
from app.services.network_analysis import NetworkAnalysisService

router = APIRouter()

@router.post("/network/shortest-path/")
def find_shortest_path(
    start_node: str,
    end_node: str,
    network_service: NetworkAnalysisService = Depends()
):
    return network_service.find_shortest_path(start_node, end_node)

@router.get("/network/centrality/")
def calculate_centrality(
    network_id: str,
    network_service: NetworkAnalysisService = Depends()
):
    return network_service.calculate_centrality(network_id)