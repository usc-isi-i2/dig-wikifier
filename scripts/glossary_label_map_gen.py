import gzip, json, os , sys
import re
from collections import defaultdict
linecount = -1
mapOflabels = defaultdict(list)

# Add all the languages that we want to extract here
languages = ['en']
glossary = set()
def clean(string: str):
    string = ' '.join(string.split()).strip()
    return string
#logfile = open('run.log', 'a')
print("Starting file processing ......")
with gzip.GzipFile('wikidata.gz', 'r') as fin:
    for line in fin:
        linecount+=1

        if linecount % 10000 == 0:
            print("< Status update >\n")
            print("Processing entity {}".format(linecount))
            #logfile.write("Processing entity {}\n".format(linecount))
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


with open("label_map.json","w") as out:
    out.write(json.dumps(mapOflabels))

with open("glossary.txt","w") as outfile:
    for word in glossary:
        outfile.write(word + "\n")

print("Done")

