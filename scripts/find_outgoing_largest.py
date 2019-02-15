import gzip, json, os , sys
import re
from collections import defaultdict
linecount = -1

# Add all the languages that we want to extract here
languages = ['en']
out_th = set()
out_fiveh = set()
out_hund = set()
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
            statements = data['claims']
            neighbors = set()
            for statement in statements:
                val = statements[statement]
                assert isinstance(val, list), "This should be list"
                for details in val:
                    #print(details)
                    if details['type'] == "statement" and 'mainsnak' in details.keys():
                        if details['mainsnak'] != {} and details['mainsnak']['datatype'] == 'wikibase-item' and details['mainsnak']['snaktype']=='value':
                            try:
                                id = details['mainsnak']['datavalue']['value']['id']
                                neighbors.add(id)
                            except Exception as e:
                                print("Exception while processing, but continuing {}".format(e.args))
                                pass
            if len(neighbors) > 1000:
                out_th.add(doc_id)
            elif len(neighbors) > 500:
                out_fiveh.add(doc_id)
            elif len(neighbors) > 100:
                out_hund.add(doc_id)
        except Exception as e:
            print("Error while loading a json line {}".format(e.args))
print("Nodes with 100-500 outgoing edges : {}".format(len(out_hund)))
print("Nodes with 500-1000 outgoing edges : {}".format(len(out_fiveh)))
print("Nodes with 1000+ outgoiing edges: {}".format(len(out_th)))

with open("nodes.txt","w") as out:
    out.write(json.dumps(out_th))
    out.write(json.dumps(out_fiveh))
    out.write(json.dumps(out_hund))

print("Done")
