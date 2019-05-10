import gzip, json, os , sys
import re
from collections import defaultdict
import argparse

"""
This script is one of the main scripts to process Wikidata. This script goes through the json dump of Wikidata and constructs a dictionary of Qnodes with its corresponding properties and edges. It serves as the intermediary structure that can be assumed to be a representation of the entire wikidata graph with properties minus the additional information (like aliases, labels etc)
Note : Script operates only on the gzipped wikidata json dumps.

"""

linecount = -1
mapOfNeighbors = defaultdict(dict)

parser = argparse.ArgumentParser()
parser.add_argument("-w","--wikidatapath")
parser.add_argument("-o","--output")

args = parser.parse_args()

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


with gzip.GzipFile(args.wikidatapath, 'r') as fin:
    for line in fin:
        linecount+=1
        if linecount == 0 or len(line) < 5:
            continue

        if linecount % 10000 == 0:
            printProgressBar(linecount, 52000000, prefix = 'Progress:', suffix = 'Complete', length = 50)
        js = line.strip().decode('utf-8')[:-1]
        try:
            data = json.loads(js)
            # Extract labels based on languages set initially
            doc_id = data['id']
            statements = data['claims']
            statement_map = defaultdict(list)
            for statement in statements:
                val = statements[statement]
                assert isinstance(val, list), "This should be list"
                for details in val:
                    if details['type'] == "statement" and 'mainsnak' in details.keys():
                        if details['mainsnak'] != {} and details['mainsnak']['datatype'] == 'wikibase-item' and details['mainsnak']['snaktype']=='value':
                            try:
                                id = details['mainsnak']['datavalue']['value']['id']
                                #mapOfNeighbors[id].append(doc_id)
                                statement_map[statement].append(id)
                            except Exception as e:
                                print("Exception while processing, but continuing {}".format(e.args))
                                pass
            mapOfNeighbors[doc_id] = statement_map
        except Exception as e:
            print("Error while loading a json line {}".format(e.args))
        
with open(args.output,"w") as out:
    out.write(json.dumps(mapOfNeighbors))

print("Done")
