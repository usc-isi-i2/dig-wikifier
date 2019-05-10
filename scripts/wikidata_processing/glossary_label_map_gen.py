import gzip, json, os , sys
import re
from collections import defaultdict
import argparse

"""
This script is used to operate on the gzipped version of the Wikidata json dumps, process each of the entities and extract their labels and perfrom some simple cleaning operations on the labels as well. The script outputs a dictionary containing all the labels for a given qnode, currently just focuses on the 'en'(English) labels in wikidata. Add more languages to that list to process labels of other languages as well. 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-w","--wikidatapath")
parser.add_argument("-l","--labelout")
parser.add_argument("-g","--glossaryout")

args = parser.parse_args()

mapOflabels = defaultdict(list)

# Add all the languages that we want to extract here
languages = ['en']
glossary = set()
def clean(string: str):
    string = ' '.join(string.split()).strip()
    return string
#logfile = open('run.log', 'a')
print("Starting file processing ......")
with gzip.GzipFile(args.wikidatapath, 'r') as fin:
    for linecount,line in enumerate(fin):

        try:
            js = line.strip().decode('utf-8')[:-1]
            data = json.loads(js)
            temp_glossary = set()
            # Extract labels based on languages set initially
            for lang in languages:
                if lang in data['labels']:
                    lb = clean(data['labels'][lang]['value'])
                    # Add it to glossary as well
                    temp_glossary.add(lb)
                # Add to glossary all the labels and alsoKnownAs words
                if lang in data['aliases']:
                    for alias in data['aliases'][lang]:
                        temp_glossary.add(clean(alias['value']))


            # Finally add everything to globals
            glossary.update(temp_glossary)
            for key in temp_glossary:
                mapOflabels[key].append(data['id'])

        except:
            continue

print("Writing output to file...")

with open(args.labelout,"w") as out:
    out.write(json.dumps(mapOflabels))

with open(args.glossaryout,"w") as outfile:
    for word in glossary:
        outfile.write(word + "\n")


