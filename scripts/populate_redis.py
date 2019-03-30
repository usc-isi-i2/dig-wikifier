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
    i=0
    for key in data:
        #print("all:" + key)
        #rkey = "lbl:" +key
        rkey = key
        i+=1
        if i%10000 == 0:
            printProgressBar(i, len(data), prefix = 'Progress:', suffix = 'Complete', length = 50)
        try:
            #print("{}->{}".format(rkey, data[key]))
            labels = data[key]
            for label in labels:
                r.delete("old_data:"+label)
            #print("Passing {} and {}".format(rkey, len(data[key])))
            #if len(data[key]) < 500:
                #print("Passing {} and {}".format(rkey, len(data[key])))
            #    r.sadd(rkey, *(data[key]))
            #else:
            #    d = list()
            #    d = data[key]
            #    while len(d)>0:
            #        p = d[:500]
            #        d = d[500:]
            #        r.sadd(rkey, *p)
                #print("Completed loop")
        except Exception as e:
            print("Error wile processing {}".format(e))
            pass
    print("\nCompleted inserting to redis")
    print("\nNumber of keys {}".format(len(data)))
