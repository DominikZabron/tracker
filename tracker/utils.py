import redis
import uuid

cache = redis.StrictRedis(host='localhost', port=6379, db=0)


def create_cart_id():
    cart_id = str(uuid.uuid4())
    cache.sadd('cart_ids', cart_id)
    return cart_id
