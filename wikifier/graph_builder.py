import redis

class GraphBuilder():
    def __init__(self, host, port):
        #self.redis = redis.Redis(
        #            host=host,
        #            port=int(port), decode_response=True)
        self.redis = redis.StrictRedis(host, int(port), charset="utf-8", decode_responses=True)
    def build_graph(self, tokens):
        set_a = set(tokens)
        set_b = set()
        edges = []
        for token in tokens:
            res =  self.redis.smembers(token)
            set_b.update(res)
            for i in res:
                edges.append((token,i))
        data = {}
        data['left'] = list(set_a)
        data['right'] =  list(set_b)
        data['edges'] = edges
        return data
