import sys, os, json
import argparse
from collections import defaultdict, OrderedDict
"""
This script is used to slice out a subgraph from the larger graph of wikidata. This works using the computed edge dictionary from the wikidata ontology. Given a set of whitelist nodes, it retains all edges between those qnodes to form a subgraph from the entire wikidata graphi
Dictionary - refers to the edge map computed
Whitelist - refers to the list of nodes we want to retain in the graph
output - refers to the output file to write the json subgraph into
"""

parser = argparse.ArgumentParser()
parser.add_argument("-d","--dictionary")
parser.add_argument("-w","--whitelist")
parser.add_argument("-o","--output")

args = parser.parse_args()
print("Reading neighbor map...")
data = defaultdict(list)
with open(args.dictionary, 'r') as fin:
    line = fin.readline()
    data = json.loads(line)

print("Edge map loaded")
print("Number of keys {}".format(len(data)))
"""
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
with open(args.blacklist) as fin:
    for line in fin:
        x = line.strip().split('/')
        if len(x) > 1:
            allow.add(x[-1])

print("whitelist has {} entities for graph".format(len(allow)))
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

with open(args.output,'w') as fout:
    fout.write(json.dumps(final_graph))
print("Done")
