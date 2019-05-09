import redis
import argparse
from collections import defaultdict
import json
# Install dependencies hiredis, redis
import math
import json
import numpy as np
from scipy import spatial
"""

This script generates the file that will be used by the tsne-visualization script. This current script has been written specifically for the viz script that requires the input. It takes the transE embeddings file, the entity2id.txt file as the mapping file and writes a csv of qnode,label,[vector embedding] for each mentioned qnode in the 'embed_film.txt' 

"""
 
parser = argparse.ArgumentParser()
parser.add_argument("-b","--binaryfile")
parser.add_argument("-n","--nodemap")

args = parser.parse_args()

# Load the nodemap for the mapping
nodemap = dict()
nodemaprev = dict()
emb = list()
# Load the entity to id file here
with open(args.nodemap, 'r') as filereader:
    for line in filereader:
        key,val = line.strip().split('\t')
        nodemap[key] = val
        nodemaprev[val] = key

print("Loaded nodemap")
# Load entity to vec file here
with open(args.binaryfile, 'r') as filereader:
    for line in filereader:
        vals = list(line.strip().split())
        emb.append(vals)
embeddings = np.array(emb).reshape(len(emb), 100)

print("Loaded embeddings")
out_file = open('tsne_input_transh','w')
with open('embed_film.txt','r') as fin:
    i=0
    for line in fin:
        i+=1
        # Expects each line to be like --> Q12312,Some label
        info = str(line)
        qid,lbl = info.strip().split(',')
        l = line.split(',')[0]
        id = nodemap.get(qid)
        # Fetches id from the mapping file (mapping file generally mapping of qnodeid to row number in the embedding)
        print("Got id {}".format(id))
        if not id:
            continue
        em = embeddings[i]
        print(em.shape)
       	embed = np.array(em).tolist()
        out_file.write("{}::{}::{}\n".format(qid,lbl,str(json.dumps(embed))))
    print("Completed prcoessing")
    out_file.close()
    exit(0)
