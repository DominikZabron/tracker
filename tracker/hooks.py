import psycopg2
from urlparse import urlparse
from tracker.utils import cache
from tracker.settings import DB_DSN
from tracker.validators import (
    validate_cart_ids_differ,
    validate_cart_id_exists,
    deserialize_request,
)

result = urlparse(url=DB_DSN)
db_connection = psycopg2.connect(
    database=result.path[1:],
    user=result.username,
    password=result.password,
    host=result.hostname,
)


def validate_request(req, resp, resource, params):
    """Validate if given request provide necessary information.

    Otherwise raise proper exception and status code.

    Validation includes:
    * check if cookie and url id values are consistent
    * ensure given id exists within created cards
    * raise exception when unable to deserialize request
    * convert fields to desired format if possible

    Return dictionary of valid item-object data.
    """
    param_id = params.get('id', None)
    cookie_id = req.cookies.get('cart_id', None)

    if param_id and cookie_id:
        validate_cart_ids_differ(param_id, cookie_id)

    if param_id or cookie_id:
        # Save cart_id for further use in responder
        params['cart_id'] = param_id if param_id else cookie_id
        validate_cart_id_exists(
            cart_id=params['cart_id'],
            cache=cache,
            db_connection=db_connection,
        )

    item_dict = deserialize_request(req.stream.read())
    params.update(item_dict)
