from __future__ import absolute_import

import falcon
import json

from tracker.validators import validate_request
from tracker.utils import create_cart_id
from tracker.hooks import queue_request


class CartItem(object):
    def __init__(self):
        self.cart_id = None

    @falcon.before(validate_request)
    @falcon.after(queue_request)
    def on_post(self, req, resp, cart_id=None):
        if not cart_id:
            cart_id = create_cart_id()
        self.cart_id = cart_id

        resp.set_cookie('cart_id', cart_id)
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'cart_id': cart_id})

app = falcon.API()

cart_item = CartItem()

app.add_route('/item', cart_item)
app.add_route('/item/{cart_id}', cart_item)
