import os
from urllib.parse import urlparse

import redis

DEFAULT_EXPIRES = 60 * 15  # number of seconds before we auto-expire keys
KEY_PREFIX = "{{APP_SLUG}}"

u = urlparse(os.environ["REDIS_URL"])
redis_connection = redis.StrictRedis(host=u.hostname, port=u.port, password=u.password, db=0)


class RedisCache(object):
    """docstring for RedisCache"""
    def __init__(self):
        super(RedisCache, self).__init__()
        if not os.environ["REDIS_URL"]:
            raise Exception("Can't use redis without specifying valid `REDIS_URL` env variable.")

        self.connection = redis_connection

    def _build_key(self, k):
        if type(k) == bytes:
            k = k.decode()  # convert bytes to str
        if k.startswith(f"{KEY_PREFIX}:"):
            return k
        return f"{KEY_PREFIX}:{k}"

    def set(self, k, v, expires=DEFAULT_EXPIRES):
        k = self._build_key(k)
        return self.connection.set(k, v, ex=expires)

    def get(self, k, default=None):
        k = self._build_key(k)
        return self.connection.get(k) or default

    def set_dict(self, k, v):
        return self.connection.hmset(k, v)

    def get_dict(self, k, default=None):
        return self.connection.hgetall(k)

    def delete(self, k):
        k = self._build_key(k)
        return self.connection.delete(k)

    def scan_iter(self, k):
        k = self._build_key(k)
        return self.connection.scan_iter(k)

    def delete_pattern(self, pattern):
        for key in self.scan_iter(pattern):
            self.delete(key)

# instantiate it so we can just import the name 'redis' and use it anywhere
redis = RedisCache()

if __name__ == '__main__':
    # test connection
    redis.set('test:foo', 'bar')
    redis.set('test:hello', 'world')
    for k in redis.scan_iter('test:*'):
        v = redis.get(k)
        print(f"{k} => {v}")

    redis.delete_pattern("test:*")