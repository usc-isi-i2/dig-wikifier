import redis
import argparse
from collections import defaultdict
import json
# Install dependencies hiredis, redis
import math
import json
import numpy as np
from scipy import spatial

parser = argparse.ArgumentParser()
parser.add_argument("-b","--binaryfile")

args = parser.parse_args()

emb = dict()
# Load the entity to id file here
with open(args.binaryfile, 'r') as filereader:
    for line in filereader:
        vals = line.strip().split('\t')
        key,val = vals[0], vals[1:]
        key = key.split('/')[-1]
        emb[key] = np.array(val).reshape(1,200)

print("Loaded embeddings")
out_file = open('tsne_input_biggraph','w')
with open('embed_film.txt','r') as fin:
    i=0
    for line in fin:
#    for i in range(0,100):
        i+=1
        info = str(line)
        qid,lbl = info.strip().split(',')
        #print("{} and {}\n".format(qid,lbl)) 
        #qid = str(nodemaprev[str(i)])
        #res = list(redis_client.smembers('lbl:'+qid))
        #lbl = ','.join(res[:2]) if len(res) > 0 else "NO Label"
        l = line.split(',')[0]
        if qid not in emb:
            continue
        em = emb[qid]
        print(em.shape)
        print("Got embed")
       	embed = np.array(em).tolist()
        print("Writing")
        out_file.write("{}::{}::{}\n".format(qid,lbl,str(json.dumps(embed))))
        print("Iteration {}\n".format(i))
    print("Completed prcoessing")
    out_file.close()
    exit(0)
