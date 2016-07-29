import falcon


def validate_cart_id(req, resp, cart_id):
    if cart_id and req.cookies.get('cart_id', False):
        if not cart_id['cart_id'] == req.cookies['cart_id']:
            msg = 'Param cart_id does not match with current session.'
            raise falcon.HTTPBadRequest('Bad request', msg)
