import sys, os, json
import argparse
from collections import defaultdict
import time
import redis

# Install dependencies hiredis, redis

parser = argparse.ArgumentParser()
parser.add_argument("-x","--host")
parser.add_argument("-p","--port")
parser.add_argument("-d","--dictionary")
args = parser.parse_args()


if __name__ == "__main__":

    data = defaultdict(list)
    print("Begin loading data ..............")
    #data = json.load(open(args.dictionary),object_pairs_hook=defaultdict)
    with open(args.dictionary, 'r') as fin:
        line = fin.readline()
        d = json.loads(line)
        data = defaultdict(list,d)
    print("Done Loading")
    print("Start writing {} keys to redis : ".format(len(data)))
    r = redis.Redis(
        host=args.host,
        port=int(args.port))
    print("redis connection established")
    for key in data:
        #print("all:" + key)
        rkey = "all:" +key
        try:
            print("Passing {} and {}".format(rkey, len(data[key])))
            if len(data[key]) < 500:
                #iprint("Passing {} and {}".format(rkey, len(data[key])))
                r.sadd(rkey, *(data[key]))
            else:
                d = list()
                d = data[key]
                while len(d)>0:
                    p = d[:500]
                    d = d[500:]
                    r.sadd(rkey, *p)
                print("Completed loop")
        except Exception as e:
            print("Error wile processing {}".format(e))
            pass
    print("Completed inserting to redis")
    print("Number of keys {}".format(len(data)))
