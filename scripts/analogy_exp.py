import redis
import argparse
from collections import defaultdict
import json
# Install dependencies hiredis, redis
import math
import json
import numpy as np
from gensim.models import Word2Vec


""" This script takes in a word2vec trained model and can perform some analogy queries, specifically x - y + z (a.k.a the king - man + woman) type queries. Initialize a list of x,y,z as tuples in the script below. The script requires the word2vec model file, along with a redis instance to connect with which contains a label for each Qnode id."""
parser = argparse.ArgumentParser()
parser.add_argument("-b","--binaryfile")
parser.add_argument("-x","--host")
parser.add_argument("-p","--port")
parser.add_argument("-o","--output")

args = parser.parse_args()
redis_client = redis.StrictRedis(
        host=str(args.host),
        port=int(args.port),
        decode_responses=True)

# Load the nodemap for the mapping
# Load entity to vec file here
model = Word2Vec.load(args.binaryfile)
outfile = open(args.output,'w')


# Set the x,y,z triples here

queries = [
    ('Q47703','Q56094','Q42574')
]

print("Loaded embeddings")
for x in queries:
    in1,in2,in3 = x
    lb1 = redis_client.smembers('lbl:'+in1)
    lb2 = redis_client.smembers('lbl:'+in2)
    lb3 = redis_client.smembers('lbl:'+in3)
    wv1, wv2, wv3 = model.wv[in1],model.wv[in2],model.wv[in3]
    res = (wv1 - wv2) + wv3
    x = model.similar_by_vector(res,topn=20,restrict_vocab = None)
    r = {}
    for item in x:
        lb = redis_client.smembers('lbl:'+item[0])
        r[item[0]] = list(lb)
    outfile.write('Query = {} ({})  - {} ({}) + {} ({})\n'.format(in1,lb1,in2,lb2,in3,lb3))
    for k in r:
        outfile.write('{}  {}\n'.format(k, r[k]))

