from __future__ import absolute_import

import falcon
import json

from tracker.utils import create_cart_id
from tracker.hooks import validate_request
from tracker.tasks import db_save


class CartItem(object):

    @falcon.before(validate_request)
    def on_post(self, req, resp, **params):
        params['cart_id'] = params.get('cart_id', create_cart_id())
        db_save.delay(params)

        resp.set_cookie('cart_id', params.get('cart_id'))
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'cart_id': params.get('cart_id')})

app = falcon.API()

cart_item = CartItem()

app.add_route('/item', cart_item)
app.add_route('/item/{id}', cart_item)
