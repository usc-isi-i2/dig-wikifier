from storage.redis_manager import RedisManager
from collections import defaultdict
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
        setOfQnodes = graph_data['right']
        neighbor_map = self.redisManager.getKeys(setOfQnodes, prefix="all:")
        graph_data['neighbor_map'] = neighbor_map
        return

    def process(self, tokens):
        graph_data = self.build_graph(tokens)
        self.compute_edge_scores(graph_data)
        return graph_data
