from .similarity import Similarity
import json
import numpy as np
from collections import defaultdict
from scipy import spatial

class VerseSimilarity(Similarity):
    def __init__(self, nodemap, embeddingsfile):
        Similarity.__init__()
        with open(nodemap, 'r') as filereader:
            self.nodemap = json.loads(filereader.readline())
        self.embeddings = np.fromfile(embeddingsfile, np.float32).reshape(len(nodemap), 128)
        self.nodemap_rev = defaultdict()
        for k, v in nodemap.items():
            self.nodemap_rev[v] = k


    def get_score(self, node1, node2):
        idx1 = self.nodemap_rev[node1] if node1 in self.nodemap_rev else None
        idx2 = self.nodemap_rev[node2] if node2 in self.nodemap_rev else None

        if idx1 and idx2:
            vec1 = self.embeddings[idx1]
            vec2 = self.embeddings[idx2]
            return spatial.distance.cosine(vec1, vec2)
        return 0
