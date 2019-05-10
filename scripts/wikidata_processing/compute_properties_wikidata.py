import gzip, json, os , sys
import re
from collections import defaultdict
import argparse

"""
This script computes a dictionary representing qnodes and the list of properties that they have described in their 'claims'. The script requires the path to the gzip compressed wikidata json dumps and executes the operation on that script.
"""
parser = argparse.ArgumentParser()
parser.add_argument("-w","--wikidatapath")
parser.add_argument("-o","--output")
parser.add_argument("-a","--whitelist")
args = parser.parse_args()


linecount = -1
mapOfNeighbors = defaultdict(list)

# This is a set of properties that we care about, and we will check only these properties while processing each Qnode.
# the file must contain several properties stored one per line as - http://wikidata.org/wiki/P123123 etc

allowed = set()
# Read blocked here - 
with open(args.whitelist,'r') as fin:
    for line in fin:
        allowed.add(line.strip().split('/')[-1])

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

# The property map structure here
pmap = defaultdict(list)

print("Size of property whitelist is {}".format(len(allowed)))

with gzip.GzipFile(args.wikidatapath, 'r') as fin:
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
            properties = set(statements.keys())
            if allowed:
                found_props = list(properties.intersection(allowed))
            else:
                found_props = list(properties)
            pmap[doc_id] = found_props
        except Exception as e:
            print("Error while loading a json line {}".format(e.args))
with open(args.output,"w") as out:
    out.write(json.dumps(pmap))

print("Done")
