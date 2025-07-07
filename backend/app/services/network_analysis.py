from typing import List, Dict, Any
from app.db.neo4j import Neo4jConnection

class NetworkAnalysisService:
    def __init__(self):
        self.neo4j = Neo4jConnection()
    
    def find_shortest_path(self, start_node: str, end_node: str) -> Dict[str, Any]:
        """Find shortest path between two nodes."""
        query = """
        MATCH (start:Node {name: $start_node}), (end:Node {name: $end_node})
        MATCH path = shortestPath((start)-[*]-(end))
        RETURN path
        """
        result = self.neo4j.query(query, {"start_node": start_node, "end_node": end_node})
        return {"path": result, "start": start_node, "end": end_node}
    
    def calculate_centrality(self, network_id: str) -> Dict[str, Any]:
        """Calculate centrality metrics for a network."""
        query = """
        MATCH (n:Node)
        RETURN n.name as node, size((n)--()) as degree
        ORDER BY degree DESC
        """
        result = self.neo4j.query(query)
        return {"centrality_scores": result, "network_id": network_id}
    
    def __del__(self):
        if hasattr(self, 'neo4j'):
            self.neo4j.close() 