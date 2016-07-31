import falcon

from tracker.utils import cache


def validate_request(req, resp, resource, params):
    param_cart_id = params.get('cart_id', None)
    cookie_cart_id = req.cookies.get('cart_id', None)

    # Raise 400 if cart_id in cookie and uri parameter differs
    if param_cart_id and cookie_cart_id:
        if not param_cart_id == cookie_cart_id:
            msg = 'Param cart_id does not match with current session.'
            raise falcon.HTTPBadRequest('Bad request', msg)

    if param_cart_id or cookie_cart_id:
        # Save cart_id for further use in responder
        params['cart_id'] = param_cart_id if param_cart_id else cookie_cart_id

        # Raise 404 if given cart_id is not recognized
        if cache.sismember('cart_ids', params['cart_id']) == 0:
            raise falcon.HTTPNotFound()
