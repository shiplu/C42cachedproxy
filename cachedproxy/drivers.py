import abc
import pickle

import redis


def factory(engine, **settings):
    """Creates a driver using engine.
    The settings are passed to driver constructor.
    If a driver abc is required, extend BaseCache and
    name is as 'ABCCache'."""
    classname = "%sCache" % engine.title()
    instance = globals()[classname](**settings)
    return instance


class BaseCache(object):
    """Base Cache driver. To add more driver just implement
    4 methods encode, decode, get, set described here"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def encode(self, obj):
        """Encodes an object. Object should be dict"""

    @abc.abstractmethod
    def decode(self, value):
        """decode an string/bytestring to an object"""

    @abc.abstractmethod
    def get(self, key):
        """get value for key. the value is a dict"""

    @abc.abstractmethod
    def set(self, key, value):
        """set value for key. the value is a dict"""


class RedisCache(BaseCache):

    def __init__(self, host, port):
        self.cluster = redis.StrictRedis(host=host, port=port)

    def encode(self, obj):
        """Encodes an object. Object should be dict.
        This allows complex object to be stored"""
        return pickle.dumps(obj)

    def decode(self, value):
        """decode an string/bytestring to an object
        This allows complex object to be restored"""
        return pickle.loads(value)

    def get(self, key):
        """get value for key. the value is a dict"""
        return self.decode(self.cluster.get(key))

    def set(self, key, value):
        """set value for key. the value is a dict"""
        self.cluster.set(key, self.encode(value))
