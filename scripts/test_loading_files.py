import sys, os, json
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-g","--glossary")
parser.add_argument("-d","--dictionary")
args = parser.parse_args()
print("Reading glossary .....")
glossary = set()
#with open(args.glossary, 'r') as fin:
#    for line in fin:
#        word = line.strip()
#        glossary.add(word)
#print("Glossary loaded")

print("Reading inverted map of labels and Qnodes ....")
data = defaultdict(list)
with open(args.dictionary, 'r') as fin:
    line = fin.readline()
    data = json.loads(line)
print("Label map loaded")

print("Number of keys {}".format(len(data)))
l = []
for key in data:
    if len(data[key]) > 100000:
        l.append((key,len(data[key])))
    #l+=len(data[key])
print(l)
print("total number of edges {}".format(len(l)))

