from __future__ import absolute_import

import falcon


class CartItem(object):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201

app = falcon.API()

cart_item = CartItem()

app.add_route('/item', cart_item)
