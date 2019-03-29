import json, os, requests, copy
from collections import defaultdict
import redis

data = defaultdict()

redis_client = redis.StrictRedis(
        host="localhost",
        port=int(6379),
        decode_responses=True)

with open('annotations.json','r') as fin:
    lines = fin.readlines()
    line = ''.join(lines).strip()
    data = json.loads(line)

final = list()
recall = 0
precision = 0
f1 = 0
max_recall = 0
all_aliases = defaultdict(set)
for i,row in enumerate(data):
    text = row['text']
    payload = json.dumps({"text" : {"text_description" :  text  }})
    search_headers = {'Accept': 'application/json', 'Content-Type':'application/json'}
    r = requests.post("http://minds03.isi.edu:4444/annotate",
                      data=payload,
                      headers=search_headers)
    results = r.json()
    canf = set()
    cannotf = set()
    candidates = defaultdict(list)
    for k in row['entities']:
        aliases = redis_client.smembers(k)
        for al in aliases:
            all_aliases[k].update([str(x) for x in redis_client.smembers("lbl:"+al)])
            candidates[k].append('::'.join((al,next(iter(all_aliases[k])) if len(all_aliases[k]) > 0 else "No Label")))
    for k in row['entities']:
        if k in all_aliases[k]:
            canf.add(k)
        else:
            cannotf.add(k)

    n_row = copy.deepcopy(row)
    n_row['wikifier'] = defaultdict(set)
    for res in results['pr_result']:
        val = results['pr_result'][res]
        n_row['wikifier'][res] = val['result']['qnode']
        cand = results['pr_result'][res]['candidates']

    c = 0
    mrc = 0
    iden = set()
    for k in n_row['wikifier']:
        if k in row['entities'] and n_row['entities'][k] == n_row['wikifier'][k]:
            c+=1
            iden.add(k)

    inter_c = (set(row['entities'].keys())).intersection(set(n_row['wikifier'].keys()))
    final.append(n_row)
    # Adding to precision and recall here.
    p = c/len(inter_c)
    rc = c/len(n_row['entities'])
    max_rc = len(canf)/ len(n_row['entities'])
    print("\n intersection {}".format(list(inter_c)))
    print(" \n Precision {} and recall {} and max recall {}".format(p,rc, max_rc))
    precision+= p
    recall+=rc
    max_recall+=max_rc
    n_row['precision'] = p
    n_row['candidates'] = candidates
    n_row['recall'] = rc
    n_row['max_recall'] = max_rc
    n_row['found'] = list(iden)
    n_row['can_find'] = list(canf)
    n_row['cannot_find'] = list(cannotf)
    n_row['key'] = 'graph' + str(i+1)
precision/=21
recall/=21
max_recall/=21
with open('annotations_new.json','w') as fout:
    fout.write(json.dumps(final))
print("Recall {}".format(recall))
print("Precision {}".format(precision))
print("Max Recall {}".format(max_recall))
print("F1 score {}".format((2 * precision * recall)/ (precision + recall)))


