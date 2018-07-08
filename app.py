import os
import time
import redis
from flask import Flask

redis_hostname = os.environ.get('redis_hostname', 'redis')
app = Flask(__name__)
cache = redis.Redis(host=redis_hostname, port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return "Big Ass hole counter: {} queries\n redis_hostname\n".format(count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
