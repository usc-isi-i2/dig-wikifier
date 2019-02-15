import redis
import argparse
from collections import defaultdict
# Install dependencies hiredis, redis
import math
import json

parser = argparse.ArgumentParser()
parser.add_argument("-x","--host")
parser.add_argument("-p","--port")
parser.add_argument("-d","--dictionary")
args = parser.parse_args()

elements = {
  "Q76": "Barack Obama",
  "Q22686": "Donald Trump",
  "Q167607": "James Comey",
  "Q24313": "Mike Pence",
  "Q29468": "GOP (republican party)",
  "Q29552": "Democratic Party",
  "Q8333": "FBI",
  "Q89": "Apple Fruit",
  "Q169": "Mango Fruit",
  "Q30": "USA",
  "Q2429253": "ISIS",
  "Q796": "Iraq",
  "Q668": "India",
  "Q3731533": "Eric Trump",
  "Q61": "Washington DC",
  "Q96": "Mexico",
  "Q19939": "Tiger",
  "Q7378": "Elephant",
  "Q851": "Saudi Arabia",
  "Q863122": "The apprentice",
  "Q22277395": "Michael Cohen",
  "Q2462124": "Trump Organization",
  "Q6294": "Hillary",
  "Q1065": "UN",
  "Q10978": "Grapes"
}

r = redis.StrictRedis(
        host=args.host,
        port=int(args.port),
        decode_responses=True)

data = defaultdict(list)

list_of_keys = elements.keys()
for ele in list_of_keys:
    data[ele] = r.smembers("all:"+ele)
with open(args.dictionary, 'r') as fin:
    line = fin.readline()
    labels = json.loads(line)

final_scores = defaultdict(list)
for p in list_of_keys:
    for q in list_of_keys:
        if p!=q:
            max_val = max(len(data[p]), len(data[q]))
            min_val = min(len(data[p]), len(data[q]))
            inter_val = len(set(data[p]).intersection(set(data[q])))
            inter = set(data[p]).intersection(set(data[q]))
            my_list = []
            for x in inter:
                my_list.append({"Qnode":x, "Labels":list(labels[x]) if x in labels else ""})
            sr_score = 1
            sim_score = (0 if max_val <= 0 else math.log(max_val, 2) - (0 if inter_val <= 0 else math.log(inter_val, 2))) / ((math.log(53000000, 2)) - (0 if min_val <= 0 else math.log(min_val, 2)))
            sr_score = sr_score - sim_score
            #print("{} -> {}, Intersection:{}, sr_val:{}".format(p,q, inter, sr_score))
            final_scores[elements[p]].append({"QNode":q,"Qnode Name":elements[q],"Score":sr_score,"Intersection_list":list(my_list)})
for key in final_scores:
    v = list(final_scores[key])
    v.sort(key=lambda x: x['Score'], reverse=True)
    final_scores[key] = v
with open("scores_3.json","w") as out:
    out.write(json.dumps(final_scores))
print("Completed")




