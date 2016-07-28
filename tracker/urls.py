from __future__ import absolute_import

import falcon
import uuid
import json


class CartItem(object):
    def on_post(self, req, resp):
        cart_id = uuid.uuid4()

        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'cart_id': str(cart_id)})

app = falcon.API()

cart_item = CartItem()

app.add_route('/item', cart_item)
