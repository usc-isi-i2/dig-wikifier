import gzip, json, os , sys
import re
import argparse
from collections import defaultdict
"""
This script computes the counts necessary to compute trainsition probabilities in the wikifier algorithm. It will capture the counts of a particular label:Qnode combination and store that in a dictionary format

"""
parser = argparse.ArgumentParser()
parser.add_argument("-l","--labelmap")
parser.add_argument("-o","--output")
parser.add_argument("-w","--wikidatapath")

args = parser.parse_args()

linecount = -1
mapOfNeighbors = defaultdict(list)

# Add all the languages that we want to extract here
languages = ['en']
def clean(string: str):
    string = ' '.join(string.split()).strip()
    return string
fp = open(args.labelmap,'r')
labels = json.load(fp)
print("loaded dictionary of labels")
label_count_dictionary = defaultdict(int)
print("Being processing....")
labelrev = defaultdict(list)

for key in labels:
    list_of_labels = labels[key]
    list_of_labels = [x for x in list_of_labels if len(x.split()) < 7]
    for x in list_of_labels:
        labelrev[x].append(key)
# Generates a reverse mapping from the labels to qnodes, which can be used for a reverse lookup to see what qnodes will be the possible candidates given a phrase
with open('candidates_map.json','w') as out:
    out.write(json.dumps(labelrev))

labelrev.clear()
print("Completed step 1 : Processing candidates map")
print("Starting step 2: Processing transition probabilities")

with gzip.GzipFile(args.wikidatapath, 'r') as fin:
    for line in fin:
        linecount+=1

        if linecount % 10000 == 0:
            print(linecount)
        js = line.strip().decode('utf-8')
        try:
            data = json.loads(js)
            # Extract labels based on languages set initially
            doc_id = data['id']
            edges = set()
            statements = data['claims']
            for statement in statements:
                val = statements[statement]
                assert isinstance(val, list), "This should be list"
                for details in val:
                    #print(details)
                    if details['type'] == "statement" and 'mainsnak' in details.keys():
                        if details['mainsnak'] != {} and details['mainsnak']['datatype'] == 'wikibase-item' and details['mainsnak']['snaktype']=='value':
                            try:
                                id = details['mainsnak']['datavalue']['value']['id']
                                edges.add(id)
                            except Exception as e:
                                print("Exception while processing, but continuing {}".format(e.args))
                                pass
            for edge in edges:
                if edge in labels:
                    label_list = labels[edge]
                    label_list = [x for x in label_list if len(x.split()) < 7]
                    for label in label_list:
                        label_count_dictionary[label+":"+edge]+=1
        except Exception as e:
            print("Error while loading a json line {}".format(e.args))
with open(args.output,"w") as out:
    out.write(json.dumps(label_count_dictionary))

print("Done")

