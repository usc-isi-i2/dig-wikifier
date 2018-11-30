import redis

class RedisManager(object):
    """
    Class for managing the connection to redis and defines several apis to use to perform the required redis lookups.
    """
    def __init__(self, host, port):
        self.redis = redis.StrictRedis(host, int(port), charset="utf-8", decode_responses=True)
        return

    def getKey(self, key):
        """

        :param key:  the key to fetch
        :return: list of members for that key
        """
        # Retreive all the members of the set 'key'
        elements = self.redis.smembers(key)
        return elements


    def setKey(self, key, vals):
        """

        :param key: key to set
        :param vals: list of members to set for that key
        :return: None
        """
        # Adding all the values in the iterable to the set stored at key
        self.sadd(key, *(vals))
        return

    def getKeys(self ,keys):
        """
        :param keys: List of keys to fetch
        :return: A dictionary of the keys and their corresponding value sets.
        """
        # Fetch several sets of keys using redis pipeline
        pipe = self.redis.pipeline()
        for key in keys:
            pipe.smembers(key)
        data = dict(zip(keys,pipe.execute()))
        return data

