from storage.redis_manager import RedisManager
from collections import defaultdict
import sys

class GraphBuilder():
    def __init__(self, host, port):
        self.redisManager = RedisManager(host, port)

    def build_graph(self, tokens):
        set_a = set(tokens)
        set_b = set()
        edges = []
        data = defaultdict()
        data['graph'] = defaultdict(list)
        # Create the graph.
        for token in tokens:
            res = self.redisManager.getKey(token)
            set_b.update(res)
            for i in res:
                data['graph'][token].append((i,0.0))
        data['left'] = list(set_a)
        data['right'] =  list(set_b)
        return data

    def compute_edge_scores(self, graph_data):
        qnodes = graph_data['right']
        anchors = graph_data['left']
        neighbor_map = self.redisManager.getKeys(qnodes, prefix="all:")
        for anchor in anchors:
            # Compute transition probability from anchor text to concept
            edges = graph_data['graph'][anchor]
            total_score = 0
            for i, edge in enumerate(edges):
                node, score = edge
                score = len(neighbor_map[node])
                total_score+=score
                edges[i] = (node,score)

            edges = [(edge[0], 1.* edge[1]/total_score) for edge in edges]
            graph_data['graph'][anchor] = edges
        return neighbor_map

    def process(self, tokens):
        graph_data = self.build_graph(tokens)
        self.compute_edge_scores(graph_data)

        return graph_data