from .similarity import Similarity
import json
import numpy as np
from collections import defaultdict
from scipy import spatial

class VerseSimilarity(Similarity):
    def __init__(self, embeddingsfile, nodemapfile):
        super(Similarity,self).__init__()
        with open(nodemapfile, 'r') as filereader:
            self.nodemap = json.loads(filereader.readline())
        self.embeddings = np.fromfile(embeddingsfile, np.float32).reshape(len(self.nodemap), 128)
    
    def get_score(self, node1, node2):
        # Remove 'Q' from the QID
        key1 = node1[1:]
        key2 = node2[1:]
        # Fetch vectors for each Qnode
        idx1 = self.nodemap[key1] if key1 in self.nodemap else None
        idx2 = self.nodemap[key2] if key2 in self.nodemap else None
        # If both exist in the index, compute the similarity
        if idx1 and idx2:
            vec1 = self.embeddings[int(idx1)]
            vec2 = self.embeddings[int(idx2)]
            return 1 - spatial.distance.cosine(vec1, vec2)
        return 0
