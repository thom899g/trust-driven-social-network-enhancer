import networkx as nx
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class SocialGraphAnalyzer:
    def __init__(self, graph_data: Dict[str, Any]) -> None:
        """Initialize the Social Graph Analyzer with network data."""
        self.graph_data = graph_data
        self.graph = self._build_graph()
        
    def _build_graph(self) -> nx.Graph:
        """Construct a NetworkX graph from provided data.
        
        Returns:
            A NetworkX graph representing the social network.
            
        Raises:
            ValueError: If the graph data is invalid or empty.
        """
        try:
            if not self.graph_data:
                raise ValueError("Graph data cannot be empty.")
            graph = nx.from_dict_of_lists(self.graph_data)
            logger.info("Successfully built the social graph.")
            return graph
        except Exception as e:
            logger.error(f"Failed to build graph: {str(e)}")
            raise

    def compute_centrality(self) -> Dict[str, float]:
        """Calculate centrality metrics for all nodes.
        
        Returns:
            A dictionary mapping node IDs to their centrality scores.
        """
        try:
            if not self.graph.nodes():
                logger.warning("Graph has no nodes.")
                return {}
            centrality = nx.betweenness_centrality(self.graph)
            logger.info(f"Computed centrality for {len(centrality)} nodes.")
            return centrality
        except Exception as e:
            logger.error(f"Centrality computation failed: {str(e)}")
            raise

    def identify_bottlenecks(self) -> Dict[str, float]:
        """Identify network bottlenecks using betweenness centrality.
        
        Returns:
            A dictionary of bottleneck nodes with their scores.
            
        Notes:
            Bottlenecks are identified based on high centrality values.
        """
        try:
            centralities = self.compute_centrality()
            if not centralities:
                logger.warning("No bottlenecks found.")
                return {}
            # Threshold can be adjusted based on network size
            threshold = max(centralities.values()) * 0.75
            bottlenecks = {node: score for node, score in centralities.items() 
                          if score > threshold}
            logger.info(f"Identified {len(bottlenecks)} bottleneck nodes.")
            return bottlenecks
        except Exception as e:
            logger.error(f"Bottleneck identification failed: {str(e)}")
            raise

    def detect_communities(self) -> Dict[int, list]:
        """Detect communities within the graph using modularity.
        
        Returns:
            A dictionary where keys are community IDs and values are node lists.
            
        Notes:
            Uses the modularity method for community detection.
        """
        try:
            if not self.graph.nodes():
                logger.warning("Graph has no nodes for community detection.")
                return {}
            communities = nx.community.greedy_communities(self.graph)
            community_dict = {i: list(comm) for i, comm in enumerate(communities)}
            logger.info(f"Detected {len(community_dict)} communities.")
            return community_dict
        except Exception as e:
            logger.error(f"Community detection failed: {str(e)}")
            raise

    def analyze_weak_links(self) -> Dict[str, float]:
        """Identify weak links in the network.
        
        Returns:
            A dictionary of edge IDs with their weakest link scores.
            
        Notes:
            Weak links are edges with low or no interaction data.
        """
        try:
            if not self.graph.edges():
                logger.warning("Graph has no edges to analyze.")
                return {}
            weak_links = {}
            for edge in self.graph.edges():
                # Assuming edge weights represent interaction strength
                weight = self.graph[edge[0]][edge[1]].get('weight', 0)
                if weight < 0.2:  # Threshold can be adjusted
                    weak_links[str(edge)] = weight
            logger.info(f"Found {len(weak_links)} weak links.")
            return weak_links
        except Exception as e:
            logger.error(f"Weak link analysis failed: {str(e)}")
            raise