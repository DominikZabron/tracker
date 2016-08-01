import falcon
import pytest
import uuid

from tracker.db import Session
from tracker.models import Cart, Item
from tracker.utils import cache
from tracker.urls import app as application

application.req_options.auto_parse_form_urlencoded = True
session = Session()


def setup_function(function):
    global session


def teardown_function(function):
    session.commit()
    session.close()


@pytest.fixture
def app():
    return application


def test_integration(client):
    """Integrity checking if whole API works in accordance to assumptions.

    Scenario for integrity checking:
    1. Create 1st Cart with new Item
    2. Create 2nd Cart with new Item
    3. Add new Item to 1st Cart (using param)
    4. Modify existing Item in 2nd Cart (using cookie)
    5. Add new Item to 2nd Cart without external_id field
    6. Add new Item to unknown Cart

    The database should return 2 Carts and 3 Items.
    """
    # Creating 1st Cart
    payload = {'external_id': 'abc'}
    headers = {'Content-Type': 'application/json'}
    resp = client.post('/item', payload, headers=headers)
    cart_id_1 = resp.json['cart_id']
    assert resp.status == falcon.HTTP_201

    # Creating 2nd Cart
    payload.update({'name': 'Old name'})
    resp = client.post('/item', payload, headers=headers)
    cart_id_2 = resp.json['cart_id']
    assert resp.status == falcon.HTTP_201

    # Adding Item to 1st Cart
    payload_2 = {'external_id': 'xyz'}
    resp = client.post('/item/{0}'.format(cart_id_1), payload_2, headers=headers)
    assert resp.status == falcon.HTTP_201

    # Modifying Item in 2nd Cart
    payload.update({'name': 'New name', 'value': 1})
    cookie = 'cart_id={0}'.format(cart_id_2)
    headers_2 = headers.copy()
    headers_2.update({'Cookie': cookie})
    resp = client.post('/item', payload, headers=headers_2)
    assert resp.status == falcon.HTTP_201

    # Add invalid Item to 2nd Cart
    resp = client.post('/item/{0}'.format(cart_id_2), {}, headers=headers)
    assert resp.status == falcon.HTTP_400

    # Add new Item to unknown Cart
    bad_id = str(uuid.uuid4())
    resp = client.post('/item/{0}'.format(bad_id), payload, headers=headers)
    assert resp.status == falcon.HTTP_404

    # Checking existing state in database
    session.close()
    assert session.query(Cart).filter(
        Cart.id.in_([cart_id_1, cart_id_2])).count() == 2
    assert session.query(Item).filter(
        Item.cart_id.in_([cart_id_1, cart_id_2])).count() == 3

    # Cleanup
    session.query(Item).filter(Item.cart_id.in_(
        [cart_id_1, cart_id_2])).delete(synchronize_session=False)
    session.query(Cart).filter(Cart.id.in_(
        [cart_id_1, cart_id_2])).delete(synchronize_session=False)
    cache.srem('cart_ids', [cart_id_1, cart_id_2])
