import redis
import argparse
from collections import defaultdict
import json
# Install dependencies hiredis, redis
import math
import json
import numpy as np
from gensim.models import Word2Vec
"""
This script is also for generating an input file for tsne-visualizations. This script specifically works with reading gensim models. Given a gensim model, it will generate the file that will be used by the tsne viz script to plot the visualization. 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-b","--binaryfile")

args = parser.parse_args()

# Load the nodemap for the mapping
# Load entity to vec file here
model = Word2Vec.load(args.binaryfile)


print("Loaded embeddings")
out_file = open('tsne_input_word2vec','w')
with open('embed_film.txt','r') as fin:
    i=0
    for line in fin:
#    for i in range(0,100):
        i+=1
        info = str(line)
        qid,lbl = info.strip().split(',')
        l = line.split(',')[0]
        vec = model.wv[qid]
        print("Got vector {}".format(id))
        if not vec.all():
            continue
        print(vec.shape)
        print("Got embed")
       	embed = np.array(vec).tolist()
        print("Writing")
        out_file.write("{}::{}::{}\n".format(qid,lbl,str(json.dumps(embed))))
        print("Iteration {}\n".format(i))
    print("Completed prcoessing")
    out_file.close()
    exit(0)
