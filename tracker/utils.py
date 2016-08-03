import redis
import uuid
import ujson
from sqlalchemy import exc

from tracker.db import Session
from tracker.models import Cart, Item
from tracker.settings import REDIS_URL

cache = redis.StrictRedis.from_url(REDIS_URL)


def create_cart_id():
    """Create valid cart_id in a form of uuid."""
    cart_id = str(uuid.uuid4())
    cache.setex(cart_id, 2592000, '0')  # expire after 30 days
    return cart_id


def cart_id_db_exists(cart_id, db_connection):
    """Return True when given cart_id exists in database, otherwise False."""
    cur = db_connection.cursor()
    cur.execute('SELECT 1 FROM cart WHERE cart.id = (%s);', (cart_id,))
    if cur.fetchone():
        return True
    else:
        return False


def json_loads(obj):
    """Load json-formatted object to python dict."""
    return ujson.loads(obj)


def json_dumps(obj):
    """Dump python dict to json-formatted object."""
    return ujson.dumps(obj)


def save_item(item_dict, session=Session):
    """Insert or update Item object in database.

    Create corresponding Cart if necessary.
    """
    session = session()

    try:
        session.add(Cart(id=item_dict.get('cart_id')))
        session.commit()
    except exc.IntegrityError:
        session.rollback()

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
    session.close()
