import os
from urllib.parse import urlparse

import redis

DEFAULT_EXPIRES = 60 * 15  # number of seconds before we auto-expire keys

u = urlparse(os.environ["REDIS_URL"])
redis_connection = redis.StrictRedis(host=u.hostname, port=u.port, password=u.password, db=0)


class RedisCache(object):
    """docstring for RedisCache"""
    def __init__(self):
        super(RedisCache, self).__init__()
        if not os.environ["REDIS_URL"]:
            raise Exception("Can't use redis without specifying valid `REDIS_URL` env variable.")

        self.connection = redis_connection

    def set(self, k, v, expires=DEFAULT_EXPIRES):
        return self.connection.set(k, v, ex=int(expires))

    def get(self, k, default=None):
        return self.connection.get(k) or default

    def delete(self, k):
        return self.connection.delete(k)

    def scan_iter(self, k):
        return self.connection.scan_iter(k)

    def delete_pattern(self, pattern):
        for key in self.connection.scan_iter(pattern):
            self.connection.delete(key)

# instantiate it so we can just import the name 'redis' and use it anywhere
redis = RedisCache()

if __name__ == '__main__':
    # test connection
    redis.set('test:hartley', 'rulez')
    print(redis.get('test:hartley'))
    # redis.delete_pattern("test:*")