import redis
import argparse
from collections import defaultdict
# Install dependencies hiredis, redis
import math
import json
import numpy as np
from scipy import spatial

parser = argparse.ArgumentParser()
parser.add_argument("-x","--host")
parser.add_argument("-p","--port")
parser.add_argument("-b","--binaryfile")
parser.add_argument("-n","--nodemap")
args = parser.parse_args()

# Load the nodemap for the mapping
nodemap = dict()
with open(args.nodemap, 'r') as filereader:
    nodemap = json.loads(filereader.readline())

embeddings = np.fromfile(args.binaryfile, np.float32).reshape(len(nodemap), 128)
nodemap_rev = defaultdict()
for k,v in nodemap.items():
    nodemap_rev[v] = k

redis_client = redis.StrictRedis(
        host=args.host,
        port=int(args.port),
        decode_responses=True)
data = ["76","9696","22686","14211","2684","7747","10978","194427","612","6294","1065","724","2429253","545449","182865","36557","1329269","10998","23505","10225"]

labels = defaultdict(list)

for key in nodemap:
    l = redis_client.smembers("lbl:Q"+str(key))
    labels[key] = list(l)

final = defaultdict(list)
kdt = spatial.KDTree(embeddings)
for key in data:
    idx = nodemap.get(key)
    result = kdt.query(embeddings[idx],k=21, p=100)
    assert len(result[0]) == len(result[1]), "These should've been equal"
    res = [nodemap_rev[i] for i in result[1]]
    lb = ','.join(labels[key][:3])
    final[lb] = [{"label": '::'.join(labels[res[i]][:4]) if len(labels[res[i]]) > 4 else '::'.join(list(labels[res[i]])) , "score": result[0][i]} for i in range(1,len(res))]
print(json.dumps(final))
