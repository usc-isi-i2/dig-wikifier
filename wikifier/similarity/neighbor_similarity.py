from .similarity import Similarity

class NeighborSimilarity(Similarity):
    def __init__(self, neighbor_map):
        super(Similarity,self).__init__()
        self.neighbor_map = neighbor_map

    def get_score(self, node1, node2):
        n1 = self.neighbor_map[node1]
        n2 = self.neighbor_map[node2]
        inter_val = len(set(n1).intersection(set(n2)))
        return inter_val
