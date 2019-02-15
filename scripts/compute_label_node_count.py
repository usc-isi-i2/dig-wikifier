import gzip, json, os , sys
import re
from collections import defaultdict
linecount = -1
mapOfNeighbors = defaultdict(list)

# Add all the languages that we want to extract here
languages = ['en']
def clean(string: str):
    string = ' '.join(string.split()).strip()
    return string
fp = open("label_map.json",'r')
labels = json.load(fp)
print("loaded dictionary of labels")
label_count_dictionary = defaultdict(int)
print("Being processing....")
with gzip.GzipFile('../wikidata.gz', 'r') as fin:
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
                            except Exception as e:
                                print("Exception while processing, but continuing {}".format(e.args))
                                pass
            for edge in edges:
                if edge in labels:
                    label_list = labels[edge]
                    for label in label_list:
                        label_count_dictionary[label+":"+edge]+=1
        except Exception as e:
            print("Error while loading a json line {}".format(e.args))
with open("label_count_map.json","w") as out:
    out.write(json.dumps(label_count_dictionary))

print("Done")

