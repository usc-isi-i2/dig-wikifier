import gzip, json, os , sys
import re
from collections import defaultdict
linecount = -1
mapOfNeighbors = defaultdict(list)

# Add all the languages that we want to extract here
languages = ['en']
glossary = set()
def clean(string: str):
    string = ' '.join(string.split()).strip()
    return string

with gzip.GzipFile('wikidata.gz', 'r') as fin:
    for line in fin:
        linecount+=1
        if linecount == 0 or len(line) < 5:
            continue

        if linecount % 10000 == 0:
            print(linecount)
        js = line.strip().decode('utf-8')[:-1]
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
                                #mapOfNeighbors[id].append(doc_id)
                            except Exception as e:
                                print("Exception while processing, but continuing {}".format(e.args))
                                pass
        except Exception as e:
            print("Error while loading a json line {}".format(e.args))
        mapOfNeighbors[doc_id] = list(edges)
with open("neighbor_map_forward.json","w") as out:
    out.write(json.dumps(mapOfNeighbors))

print("Done")
