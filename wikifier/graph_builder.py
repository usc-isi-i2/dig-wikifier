from .storage.redis_manager import RedisManager

class GraphBuilder():
    def __init__(self, host, port):
        self.redisManager = RedisManager(host, port)

    def build_graph(self, tokens):
        set_a = set(tokens)
        set_b = set()
        edges = []
        # Create the graph.
        for token in tokens:
            res = self.redisManager.getKey(token)
            set_b.update(res)
            for i in res:
                edges.append((token,i))
        data = {}
        data['left'] = list(set_a)
        data['right'] =  list(set_b)
        data['edges'] = edges
        return data

    def compute_edge_scores(self):
        pass


    def process(self, tokens):
        data = self.build_graph(tokens)
        return data