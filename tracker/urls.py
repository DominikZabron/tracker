from __future__ import absolute_import

import falcon
import uuid
import json

from tracker.validation import validate_cart_id


class CartItem(object):

    @falcon.before(validate_cart_id)
    def on_post(self, req, resp, cart_id=None):

        if not cart_id:
            if 'cart_id' in req.cookies:
                cart_id = req.cookies['cart_id']
            else:
                cart_id = str(uuid.uuid4())

        resp.set_cookie('cart_id', cart_id)
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'cart_id': cart_id})

app = falcon.API()

cart_item = CartItem()

app.add_route('/item', cart_item)
app.add_route('/item/{cart_id}', cart_item)
