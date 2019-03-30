import gzip, json, os , sys
import re
from collections import defaultdict
import string

mapOflabels = defaultdict(list)

# Add all the languages that we want to extract here
languages = ['en']
glossary = set()
def clean(string: str):
    string = ' '.join(string.split()).strip()
    return string

def clean2(st: str):
    punc_dict = dict.fromkeys(string.punctuation)
    translator = str.maketrans(punc_dict)
    st = ' '.join(st.split()).strip()
    st = st.translate(translator)
    return st
    
print("Starting file processing ......")
with gzip.GzipFile('wikidata_filtered.gz', 'r') as fin:
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

with open("label_map.json","w") as out:
    out.write(json.dumps(mapOflabels))

