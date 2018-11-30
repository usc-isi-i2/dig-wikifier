import redis

class RedisManager(object):
    def __init__(self, host, port):
        self.redis = redis.StrictRedis(host, int(port), charset="utf-8", decode_responses=True)
        return

    def getKey(self, key):
        # Retreive all the members of the set 'key'
        elements = self.redis.smembers(key)
        return elements


    def setKey(self, key, vals):
        # Adding all the values in the iterable to the set stored at key
        self.sadd(key, *(vals))
        return