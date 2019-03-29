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
blocked = set()
blacklist = set()
# Read blocked here - 
with open('blocked.txt','r') as fin:
    for line in fin:
        blocked.add(line.strip())

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

print("Size of blacklist is {}".format(len(blocked)))
filtered_file = gzip.open('wikidata_filtered.gz','wt')
with gzip.GzipFile('../wikidata.gz', 'r') as fin:
    for line in fin:
        linecount+=1
        if linecount == 0 or len(line) < 5:
            continue

        if linecount % 10000 == 0:
            printProgressBar(linecount, 53000000, prefix = 'Progress:', suffix = 'Complete', length = 50)
        js = line.strip().decode('utf-8')[:-1]
        try:
            data = json.loads(js)
            # Extract labels based on languages set initially
            doc_id = data['id']
            if doc_id.startswith('P'):
                continue
            statements = data['claims']
            for statement in statements:
                if statement not in set(['P31','P279']):
                    continue
                val = statements[statement]
                assert isinstance(val, list), "This should be list"
                for details in val:
                    if details['type'] == "statement" and 'mainsnak' in details.keys():
                        try:
                            if details['mainsnak'] != {} and details['mainsnak']['datavalue']['value']['id'] in blocked:
                                id = details['mainsnak']['datavalue']['value']['id']
                                blacklist.add(doc_id)
                        except Exception as e:
                            print("Exception while processing, but continuing {}".format(e.args))
                            pass
                        try:
                            if details['mainsnak'] != {} and details['mainsnak']['datavalue']['value']['id'] in blocked:
                                id = details['mainsnak']['datavalue']['value']['id']
                                blacklist.add(doc_id)
                        except Exception as e:
                            print("Exception while processing, but continuing {}".format(e.args))
                            pass
                if doc_id not in blacklist:
                    filtered_file.write(js + "\n")
        except Exception as e:
            print("Error while loading a json line {}".format(e.args))
with open("blacklist.json","w") as out:
    out.write(json.dumps(list(blacklist)))

print("Done")
