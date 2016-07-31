import redis
import uuid
from sqlalchemy.sql import exists

from tracker.db import Session
from tracker.models import Cart, Item
from tracker.settings import REDIS_URL

cache = redis.StrictRedis.from_url(REDIS_URL)


def create_cart_id():
    """Create valid cart_id in a form of uuid."""
    cart_id = str(uuid.uuid4())
    cache.sadd('cart_ids', cart_id)
    return cart_id


def save_item(item_dict):
    """
    Save or update Item object in database.

    Create corresponding Cart if necessary."""
    session = Session()

    if not session.query(exists().where(
                    Cart.id == item_dict.get('cart_id'))).scalar():
        session.add(Cart(id=item_dict.get('cart_id')))

    item = session.query(Item).filter(
        Item.cart_id == item_dict.get('cart_id'),
        Item.external_id == item_dict.get('external_id'),
    ).first()

    if item:
        for key, value in item_dict.iteritems():
            setattr(item, key, value)
    else:
        item = Item(**item_dict)
        session.add(item)

    session.commit()
