from storage.redis_manager import RedisManager
from collections import defaultdict
import networkx as nx
from similarity.neighbor_similarity import NeighborSimilarity
from networkx.readwrite import json_graph
from utils import pagerank
import sys
import math
from flask import Flask, app


class GraphBuilder():
    def __init__(self, host, port, verse_similarity):
        self.redisManager = RedisManager(host, port)
        self.verse_similarity = verse_similarity

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
                data['graph'][token].append((i, 0.0))
        data['left'] = list(set_a)
        data['right'] = list(set_b)
        return data


    def compute_edge_scores(self, graph_data, jsonify=False):
        qnodes = graph_data['right']
        anchors = graph_data['left']
        del graph_data['right']
        del graph_data['left']

        #neighbor_map = self.redisManager.getKeys(qnodes, prefix="all:")
        G = nx.DiGraph()

        for anchor in anchors:
            # Compute transition probability from anchor text to concepts.
            edges = graph_data['graph'][anchor]
            total_score = 0
            G.add_node(anchor)
            for i, edge in enumerate(edges):
                node, score = edge
                score = self.redisManager.get(anchor+":"+node)
                if score:
                    score = math.log(score,2)
                total_score += score
                edges[i] = (node, score)
            edges = [(anchor, edge[0], (1. * edge[1] / total_score) if total_score else 0) for edge in edges]
            G.add_weighted_edges_from(edges)
            #graph_data['graph'][anchor] = edges
        del graph_data['graph']
        # Augment graph with edges between concepts if it is allowed.
        # neighbor_similarity = NeighborSimilarity(neighbor_map)
        for first in qnodes:
            total = 0.0
            for second in qnodes:
                sr_score = 0.0 
                if first != second:
                    sr_score = self.verse_similarity.get_score(first, second)
                    total += sr_score
                    if sr_score > 0.5:
                        G.add_weighted_edges_from([(first, second, sr_score)])

            #for second in qnodes:
            #    if second in G[first]:
            #        G[first][second]['weight'] /= total
        scores = dict()
        for node in G.nodes:
            scores[node] = 1000
        res = pagerank(G, alpha=0.1, weight='weight', nstart=scores)
        graph_data['nx'] = dict()
        pr_result = dict()

        # Setting the top node for the graph

        # Fetch all labels that are needed
        label_keys = qnodes
        labels = self.redisManager.getKeys(keys=label_keys, prefix="lbl:")
        # Set score as property in networkx graphs
        for key in res:
            if key in G.nodes:
                G.node[key]['pagerank'] = res[key]

        # Construct final result json
        for anchor in anchors:
            edges = G.edges(anchor)
            # Iterate and find the most suitable concept, use pagerank scores to choose
            max_node = None
            max_val = -1
            pr_result[anchor] = dict()
            pr_result[anchor]['candidates'] = list()
            for (u,v) in edges:
                if res[v] > max_val:
                    max_val = res[v]
                    max_node = v
                #pr_result[anchor]['candidates'].append({'qnode': v, 'score': res[v], 'labels': list(labels[v]) if v in labels.keys() else list()})
            #pr_result[anchor]['candidates'] = sorted(pr_result[anchor]['candidates'], key=lambda k: k['score'], reverse=True)
            pr_result[anchor]['result'] = {'qnode': max_node, 'score': max_val, 'labels': list(labels[max_node]) if max_node in labels.keys() else list()}
            # if max_val > 0:
            #     pr_result[anchor] = {"qnode": max_node, "score": max_val, "labels":labels}
        graph_data['pr_result'] = pr_result

        # Returning json_data to file

        if jsonify:
            node_link_data = nx.readwrite.json_graph.node_link_data(G)
        else:
            node_link_data = dict()

        return node_link_data

    def process(self, tokens):
        graph_data = self.build_graph(tokens)
        self.compute_edge_scores(graph_data, jsonify=False)

        return graph_data

    def process_nx_graph(self, tokens):
        graph_data = self.build_graph(tokens)
        node_link_data = self.compute_edge_scores(graph_data, jsonify=True)
        return node_link_data

