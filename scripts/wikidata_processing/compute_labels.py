import redis
import argparse
from collections import defaultdict
# Install dependencies hiredis, redis
import string
import json, re
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
parser = argparse.ArgumentParser()
parser.add_argument("-x","--host")
parser.add_argument("-p","--port")
parser.add_argument("-o","--outfile")
parser.add_argument("-n","--nodemap")
args = parser.parse_args()

def clean(st):
    translator = str.maketrans(dict.fromkeys(string.punctuation))
    st = ' '.join(st.split()).strip()
    st = st.translate(translator)
    st = re.sub(r'\b[0-9]+\b\s*', '', st)
    words = st.split()
    words = [word for word in words if word not in ENGLISH_STOP_WORDS]
    st = ' '.join(words)
    return st
    
# Load the nodemap for the mapping
nodemap = dict()
with open(args.nodemap, 'r') as filereader:
    nodemap = json.loads(filereader.readline())

redis_client = redis.StrictRedis(
        host=args.host,
        port=int(args.port),
        decode_responses=True)
out = open(args.outfile, 'w')
for key in nodemap:
    l = redis_client.smembers("lbl:Q"+str(key))
    for label in l:
        val = clean(label)
        if len(val.split(' ')) <= 5 and len(val) >= 3:
            out.write(val+'\n')
