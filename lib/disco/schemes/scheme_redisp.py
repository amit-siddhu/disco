import redis
from disco.util import schemesplit

class RedisPStream(file):

    def __init__(self, redis_url, input_data):
        _redis_scheme, rest = schemesplit(redis_url)
        host, port, dbid, output_channel = rest.split(":")
        self.redis = redis.StrictRedis(host=host, port=port, db=dbid)
        self.output_channel = output_channel
        self.input_data = input_data
        self.url = redis_url

    def __iter__(self):
        yield self.read()

    def __len__(self):
        return 1

    def read(self):
        return self.input_data

    def add(self, key, data):
        self.redis.publish(self.output_channel, data)


def input_stream(fd, size, url, params):
    file = RedisPStream(params.output_url, params.input_data)
    return file, len(file), file.url

def redis_output_stream(stream, partition, url, params):
    file = RedisPStream(params.output_url, params.input_data)
    return file, len(file), file.url
