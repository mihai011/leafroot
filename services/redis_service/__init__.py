"""Redis services
"""
import redis
from redis.commands.graph.node import Node
from redis.commands.graph.edge import Edge
from logger import log
from data import get_redis_connection


class RedisService:
    """
    Redis Utils class.
    """

    def __init__(self, client):
        """Constructor for redis utils."""

        self.client = client
        self.graphs = {}
        self.nodes = {}

    @log()
    def add_graph(self, graph):
        """Add graph"""

        name = graph.name

        if name in self.graphs:
            return self.get_graph_metadata(name)

        self.graphs[graph.name] = self.client.graph(name)
        graph = self.graphs[name]
        dummy_node = Node(label="DUMMY", properties={})
        graph.add_node(dummy_node)

        return self.get_graph_metadata(name)

    @log()
    def add_node_to_graph(self, node):
        """Add node to graph."""

        graph = self.graphs[node.graph]
        n = Node(label=node.label, properties=node.properties)
        graph.add_node(n)

        return {"alias": n.alias}

    @log()
    def add_edge_to_graph(self, edge):
        """Add node to graph."""

        graph = self.graphs[edge.graph]
        source_node = graph.nodes[edge.source]
        destination_node = graph.nodes[edge.destination]
        relation = edge.relation

        e = Edge(source_node, relation, destination_node)
        graph.add_edge(e)

        return True

    @log()
    def get_graph_metadata(self, name):

        graph = self.graphs[name]
        metadata = {}
        metadata["name"] = name
        metadata["nodes"] = list(graph.nodes.keys())
        metadata["edges"] = len(graph.edges)

        return metadata

    @log()
    def graph_commit(self, graph):

        graph = self.graphs[graph.name]
        graph.commit()

        return True

    @log()
    def delete_graph(self, name):

        graph = self.graphs.pop(name)
        graph.delete()


redis_service = RedisService(next(get_redis_connection()))
