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

    def compute_edge_scores(self):
        pass


    def process(self, tokens):
        graph_data = self.build_graph(tokens)
        return graph_data