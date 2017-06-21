import os
from urlparse import urlparse

import redis

DEFAULT_EXPIRES = 60 * 15  # number of seconds before we auto-expire keys


class RedisCache(object):
    """docstring for RedisCache"""
    def __init__(self):
        super(RedisCache, self).__init__()
        if not os.environ["REDIS_URL"]:
            raise Exception("Can't use redis without specifying valid `REDIS_URL` env variable.")

        u = urlparse(os.environ["REDIS_URL"])
        self.redis = redis.StrictRedis(host=u.hostname, port=u.port, password=u.password, db=0)

    def set(self, k, v, expires=DEFAULT_EXPIRES):
        return self.redis.set(k, v, ex=int(expires))

    def get(self, k, default=None):
        return self.redis.get(k) or default

    def delete(self, k):
        return self.redis.delete(k)

    def scan_iter(self, k):
        return self.redis.scan_iter(k)

    def delete_pattern(self, pattern):
        for key in redis.scan_iter(pattern):
            redis.delete(key)

if __name__ == '__main__':
    # test connection
    r = RedisCache()
    r.set('hartley', 'rulez')
    print r.get('hartley')

else:
    # instantiate it so we can just import the name 'redis' and use it anywhere
    redis = RedisCache()