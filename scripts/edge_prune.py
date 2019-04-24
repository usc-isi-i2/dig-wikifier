import sys, os, json
import argparse
from collections import defaultdict, OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument("-d","--dictionary")
parser.add_argument("-b","--blacklist")
args = parser.parse_args()
print("Reading neighbor map...")
data = defaultdict(list)
with open(args.dictionary, 'r') as fin:
    line = fin.readline()
    data = json.loads(line)
print("Neighbor map loaded")
print("Number of keys {}".format(len(data)))
allow = set(data.keys())
out_file = open('edge_list_film.csv','w')
for key in allow:
    if key not in data:
        continue
    sts = data[key]
    for st in sts:
        edges = sts[st]
        for e in edges:
            out_file.write("{}\t{}\n".format(key,e))

"""
allow = set()
for filename in os.listdir(args.blacklist):
    with open(args.blacklist+'/'+filename) as fin:
        for line in fin:
            x = line.strip().split('/')
            if len(x) > 1:
                allow.add(x[-1])

print("whitelist has {} entities for film graph".format(len(allow)))
final_graph = dict()
for key in allow:
    if key not in data:
        continue
    sts = data[key]
    final = dict()
    for st in sts:
        edges = sts[st]
        # filter edges here
        edges = [x for x in edges if x in allow]
        if edges:
            final[st] = edges
    final_graph[key] = final

with open('film_graph.json','w') as fout:
    fout.write(json.dumps(final_graph))
print("Done")
"""
"""
edge_list = open('train2id.txt', 'w')
nodes = open('entity2id.txt','w')
props = open('relation2id.txt','w')
allow = set(data.keys())
qid = 0
pid = 0
q = dict()
p = dict()
print("computed blacklist")
print("Size of blacklist {}".format(len(allow)))
#props = set({'P31','P279'})
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
"""
print("Completed")
