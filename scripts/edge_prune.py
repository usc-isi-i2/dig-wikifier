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
block = set()
edge_list = open('edge_list_temp.csv', 'w')
with open(args.blacklist, 'r') as fin:
    line = fin.readline()
    block = set(json.loads(line.strip()))
print("computed blacklist")
print("Size of blacklist {}".format(len(block)))
for key in data:
    if 'fw' in data[key]:
        ids = list(data[key]['fw'])
        for id in ids:
            if key not in block and id not in block:
                edge_list.write("{},{}\n".format(key[1:],id[1:]))
    if 'bk' in data[key]:
        ids = list(data[key]['bk'])
        for id in ids:
            if key not in block and id not in block:
                edge_list.write("{},{}\n".format(id[1:],key[1:]))
print("Completed")
