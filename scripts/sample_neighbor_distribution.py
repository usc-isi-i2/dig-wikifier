import sys, os, json
import argparse
from collections import defaultdict, OrderedDict
import matplotlib.pyplot as plt
import numpy as np

plt.switch_backend('agg')
parser = argparse.ArgumentParser()
parser.add_argument("-d","--dictionary")
args = parser.parse_args()
print("Reading neighbor map...")
data = defaultdict(list)
with open(args.dictionary, 'r') as fin:
    line = fin.readline()
    data = json.loads(line)
print("Neighbor map loaded")

print("Number of keys {}".format(len(data)))
l = 0
print("Computing distribution")
dist = defaultdict(int)
while l < 53414230:
    n = 0
    id = "Q"+str(l)
    if id in data:
        n = len(data[id])
    dist[n]+=1
    l+=1

#for key in sorted(data):
#    print("{}->{}".format(key,data[key]))
#for key in data:
#    l+=len(data[key])
#print("total number of edges {}".format(l))
print("Distribution map \n")
#print(dist)
print("Sampling complete........")
x = []
y = []
print("Sorting data ........")
#data = sorted(data)
print("Sorting done!")
for k in sorted(dist):
    x.append(k)
    y.append(dist[k])
print("Generating plot......")
plt.xlabel('Number of neighbors', fontsize=12)
plt.ylabel('Number of Qnodes with that number of neighbors', fontsize=12)
plt.loglog(x,y)

plt.savefig('fo.png')

