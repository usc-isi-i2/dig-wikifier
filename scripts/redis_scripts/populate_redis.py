import sys, os, json
import argparse
from collections import defaultdict
import time
import redis
from glob import glob

"""
This script is used for loading/unloading from redis. Some commented code shows how we delete keys from redis given a dictionary and how we load a dictionary into redis. This script has been used to load the edge maps, label maps, transition probabilities, properties for qnodes all into redis. Requires a redis server setup and running
"""

# Install dependencies hiredis, redis

parser = argparse.ArgumentParser()
parser.add_argument("-x", "--host")
parser.add_argument("-p", "--port")
parser.add_argument("-d", "--dictionary")
parser.add_argument("-t", "--type")
parser.add_argument("-v", "--prefix")
parser.add_argument("-f", "--folder")
parser.add_argument("-g", "--fpath")
args = parser.parse_args()


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
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


def redis_man(redis_obj, data, data_type, key_prefix=None):
    for key in data:
        val = data[key]
        if not isinstance(val, list):
            val = [val]
        if len(val) < 1000000:
            if len(val) > 0:
                try:
                    if key_prefix is None:
                        if key.endswith("_s") or key.endswith("_o"):
                            key_prefix = 'p_table:'
                        else:
                            key_prefix = "po_table:"
                    rkey = key_prefix + key
                    if data_type == "NUMBER":
                        redis_obj.set(rkey, d)
                    elif data_type == "SET":
                        if len(val) < 500:
                            redis_obj.sadd(rkey, *val)
                        else:
                            d = val
                            while len(d) > 0:
                                p = d[:500]
                                d = d[500:]
                                redis_obj.sadd(rkey, *p)
                    elif data_type == "JSON":
                        d = data[key]
                        redis_obj.set(rkey, json.dumps(d))
                    elif data_type == "DEL":
                        redis_obj.delete(rkey)
                except Exception as e:
                    print("Error wile processing key{} with {}".format(rkey, e))
                    pass
        else:
            print('More than a million values for key: {}'.format(key))


if __name__ == "__main__":
    assert args.type in ["NUMBER", "SET", "JSON", "DEL"]
    r = redis.Redis(
        host=args.host,
        port=int(args.port))
    print("redis connection established")
    key_prefix = args.prefix if args.prefix is not None else ""
    folder_path = args.folder
    file_path = args.fpath
    if folder_path:
        text_files = glob('{}/part*'.format(folder_path))
        for text_file in text_files:
            print("start uploading file: {}".format(text_file))
            f_obj = open(text_file)
            for line in f_obj:
                line = line.replace('\n', '')
                data = json.loads(line)

                redis_man(r, data, args.type)
            print("finished uploading file: {}".format(text_file))
    elif file_path:
        if file_path.endswith(".tsv"):
            f_obj = open(file_path)
            c = 0
            for line in f_obj:
                if c % 1000 == 0:
                    print('loaded {} lines'.format(c))
                c += 1
                line = line.replace('\n', '')
                values = line.split('\t')
                data = {values[0]: values[1:]}
                redis_man(r, data, args.type, key_prefix='embeddings:')
            print('Done')
    else:
        data = defaultdict(list)
        print("Begin loading data ..............")

        with open(args.dictionary, 'r') as fin:
            d = json.load(fin)
            data = defaultdict(list, d)
        print("Done Loading")
        print("Start writing {} keys to redis : ".format(len(data)))

        redis_man(r, data, args.type, key_prefix=key_prefix)
        # for key in data:
        #     rkey = key_prefix + key
        #     i += 1
        #     if i % 10000 == 0:
        #         printProgressBar(i, len(data), prefix='Progress:', suffix='Complete', length=50)
        #     try:
        #         if args.type == "NUMBER":
        #             r.set(rkey, d)
        #         elif args.type == "SET":
        #             if len(data[key]) < 500:
        #                 # print("Passing {} and {}".format(rkey, data[key]))
        #                 # exit(0)
        #                 r.sadd(rkey, *(data[key]))
        #             else:
        #                 d = list()
        #                 d = data[key]
        #                 while len(d) > 0:
        #                     p = d[:500]
        #                     d = d[500:]
        #                     r.sadd(rkey, *p)
        #         elif args.type == "JSON":
        #             d = data[key]
        #             r.set(rkey, json.dumps(d))
        #         elif args.type == "DEL":
        #             r.delete(rkey)
        #     except Exception as e:
        #         print("Error wile processing key{} with {}".format(rkey, e))
        #         pass
        print("\nCompleted inserting to redis")
        print("\nNumber of keys {}".format(len(data)))
