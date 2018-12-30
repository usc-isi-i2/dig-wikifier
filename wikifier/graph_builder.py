from storage.redis_manager import RedisManager
from collections import defaultdict
import networkx as nx
from networkx.readwrite import json_graph
import sys
import math

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
        G=nx.DiGraph()

        for anchor in anchors:
            # Compute transition probability from anchor text to concepts.
            edges = graph_data['graph'][anchor]
            total_score = 0
            G.add_node(anchor)
            for i, edge in enumerate(edges):
                node, score = edge
                score = len(neighbor_map[node])
                total_score+=score
                edges[i] = (node,score)
            edges = [(anchor, edge[0], 1.* edge[1]/total_score) for edge in edges]
            G.add_weighted_edges_from(edges)
            graph_data['graph'][anchor] = edges
        #graph_data['nx'] = json_graph.adjacency_data(G)

        # Augment graph with edges between concepts if it is allowed.
        for first in qnodes:
            total=0.0
            for second in qnodes:
                if first != second:
                    sr_score = 1
                    n1 = neighbor_map[first]
                    n2 = neighbor_map[second]
                    inter_val = len(set(n1).intersection(set(n2)))
                    min_val = min(len(n1), len(n2))
                    #sim_score = ( math.log(max(len(n1), len(n2)),10) - (inter_val if inter_val <=0 else math.log(inter_val))) / ( 43000000 - (min_val if min_val <=0 else math.log(min_val)))
                    sim_score = ( math.log(max(len(n1), len(n2)),10) - (inter_val if inter_val <=0 else math.log(inter_val,10))) / ( math.log(53000000,10) - (min_val if min_val <=0 else math.log(min_val,10)))                    
                    sr_score = sr_score - sim_score
                    total+=sr_score
                    if sr_score > 0:
                        G.add_weighted_edges_from([(first,second,sr_score)])

            for second in qnodes:
                if second in G[first]:
                    G[first][second]['weight']/=total
        
        graph_data['nx'] = json_graph.adjacency_data(G)

    def process(self, tokens):
        graph_data = self.build_graph(tokens)
        self.compute_edge_scores(graph_data)

        return graph_data
