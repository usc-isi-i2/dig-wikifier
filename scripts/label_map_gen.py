import gzip, json, os , sys
import re
from collections import defaultdict
import string, argparse
"""

This script operates on the gzipped wikidata json dumps and extracts labels for each Qnode entity in wikidata. Stores the result as a dictionary of lists.

"""

parser = argparse.ArgumentParser()
parser.add_argument("-w","--wikidatapath")
parser.add_argument("-l","--labelout")

args = parser.parse_args()

mapOflabels = defaultdict(list)

# Add all the languages that we want to extract here
languages = ['en']
glossary = set()
def clean(string: str):
    # Cleans rogue whitespaces, tabs etc.
    string = ' '.join(string.split()).strip()
    return string

def clean2(st: str):
    # This function just removes a punctuation from a string
    punc_dict = dict.fromkeys(string.punctuation)
    translator = str.maketrans(punc_dict)
    st = ' '.join(st.split()).strip()
    st = st.translate(translator)
    return st
    
print("Starting file processing ......")
with gzip.GzipFile(args.wikidatapath, 'r') as fin:
    for linecount,line in enumerate(fin):
        try:
            js = line.strip().decode('utf-8')
            data = json.loads(js)
            temp_glossary = set()
            # Extract labels based on languages set initially
            for lang in languages:
                if lang in data['labels']:
                    lb = clean(data['labels'][lang]['value'])
                    # Add it to glossary as well
                    temp_glossary.add(lb)
                    temp_glossary.add(clean2(data['labels'][lang]['value']))
                # Add to glossary all the labels and alsoKnownAs words
                if lang in data['aliases']:
                    for alias in data['aliases'][lang]:
                        temp_glossary.add(clean(alias['value']))
                        temp_glossary.add(clean2(alias['value']))

            # Finally add everything to globals
            glossary.update(temp_glossary)
            for key in temp_glossary:
                mapOflabels[data['id']] = list(temp_glossary)

        except Exception as e:
            print("Exception occured while processing {}".format(e))
            continue

print("Writing output to file...")

with open(args.labelout,"w") as out:
    out.write(json.dumps(mapOflabels))

