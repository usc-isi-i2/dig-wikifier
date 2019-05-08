import sys, os, json
import argparse
from collections import defaultdict, OrderedDict
import argparse


"""
Script that generates the 3 files required for transX embedding training on CPU using KB2E - https://github.com/thunlp/KB2E . Given a graph, it will generate the vertex, edge and property lists in the required format
"""
parser = argparse.ArgumentParser()
parser.add_argument("-d","--dictionary")
args = parser.parse_args()
print("Reading neighbor map...")
data = defaultdict(list)
with open(args.dictionary, 'r') as fin:
    line = fin.readline()
    data = json.loads(line)
print("Edge map loaded")
print("Number of keys {}".format(len(data)))

edge_list = open('train2id.txt', 'w')
nodes = open('entity2id.txt','w')
props = open('relation2id.txt','w')
allow = set(data.keys())
qid = 0
pid = 0
q = dict()
p = dict()
print("computed whitelist")
print("Size of whitelist {}".format(len(allow)))
for key in allow:
    nkey = str(key)
    sts = data[nkey]
    if nkey not in q:
        q[nkey] = qid
        qid+=1
        nodes.write("{}\t{}\n".format(nkey, q[nkey]))
    for st in sts:
        edge_ends = sts[st]
        if st not in p:
            p[st] = pid
            pid+=1
            props.write("{}\t{}\n".format(st,p[st]))
        for edge in edge_ends:
            if edge not in q:
                q[edge] = qid
                qid+=1
                nodes.write("{}\t{}\n".format(edge,q[edge]))
            edge_list.write("{}\t{}\t{}\n".format(q[nkey],q[edge],p[st])) 
        #exit(0)

