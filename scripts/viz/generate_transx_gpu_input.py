import sys, os, json
import argparse
from collections import defaultdict
"""
This script is used to generate a standard form of input for the transX embeddings for the GPU training, it takes in the graph in the dictionary format and then generates the 3 files required to run the transX training.
 
"""
parser = argparse.ArgumentParser()
parser.add_argument("-d","--edgemap")
args = parser.parse_args()

print("Begin processing ... ")
data = defaultdict(list)
train = open('train.txt', 'w')
e2id = open('entity2id.txt','w')
p2id = open('relation2id.txt','w')
eid = 0
pid = 0
entities = dict()
relations = dict()
with open(args.edgemap, 'r') as fin:
    for line in fin:
        p,r,q = line.strip().split('\t')
        #train.write('{}\t{}\t{}\n'.format(p,q,r))
        if p not in entities.keys():
            e2id.write('{}\t{}\n'.format(p,eid))
            entities[p] = eid
            eid+=1
        if r not in relations.keys():
            p2id.write('{}\t{}\n'.format(r,pid))
            relations[r] = pid
            pid+=1
        if q not in entities.keys():
            e2id.write('{}\t{}\n'.format(q,eid))
            entities[q] = eid
            eid+=1
        train.write('{}\t{}\t{}\n'.format(entities[p], entities[q], relations[r]))
print("Done")                        
