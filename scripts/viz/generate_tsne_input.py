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
This script again generates an input for tsne visualization. This script specifically reads VERSE embeddings (https://github.com/xgfs/verse) and extracts their embeddings into the required format for visualization. 

"""

parser = argparse.ArgumentParser()
#parser.add_argument("-x","--host")
#parser.add_argument("-p","--port")
parser.add_argument("-b","--binaryfile")
parser.add_argument("-n","--nodemap")
args = parser.parse_args()

# Load the nodemap for the mapping
nodemap = dict()
with open(args.nodemap, 'r') as filereader:
    nodemap = json.loads(filereader.readline())

embeddings = np.fromfile(args.binaryfile, np.float32).reshape(len(nodemap), 128)
print("Loaded embeddings")
nodemap_rev = defaultdict()
for k,v in nodemap.items():
    nodemap_rev[v] = k

print("Loaded data")

out_file = open('tsne_film','w')
with open('embed_film.txt','r') as fin:
    i=0
    for line in fin:
        i+=1
        info = str(line)
        qid,lbl = info.strip().split(',')
        l = line.split(',')[0]
        id = nodemap.get(l)
        print("Got id {}".format(id))
        if not id:
            print("Got id none")
            continue
        em = embeddings[id]
        print(em.shape)
       	embed = np.array(em).tolist()
        out_file.write("{}::{}::{}\n".format(qid,lbl,str(json.dumps(embed))))
        print("Iteration {}\n".format(i))
    print("Completed prcoessing")
    out_file.close()
    exit(0)
