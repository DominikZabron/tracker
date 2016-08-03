import falcon

from tracker.utils import json_loads
from tracker.utils import cart_id_db_exists


def validate_cart_ids_differ(param_id, cookie_id):
    """Raise 400 if cart_id in cookie and uri parameter differs."""
    if not param_id == cookie_id:
        msg = 'Param cart_id does not match with current session.'
        raise falcon.HTTPBadRequest('Bad request', msg)


def validate_cart_id_exists(cart_id, cache, db_connection):
    """Raise 404 if given cart_id is not recognized."""
    if cache.exists(cart_id) == 0:
        if not cart_id_db_exists(cart_id, db_connection):
            raise falcon.HTTPNotFound()


def deserialize_request(json_body):
    """Raise 400 if request body could not be deserialized."""
    try:
        raw_item = json_loads(json_body)
    except:
        msg = 'Invalid json format.'
        raise falcon.HTTPBadRequest('Bad request', msg)

    return validate_item_values(raw_item)


def validate_item_values(item_dict):
    """Raise 400 if unable to convert item values to proper types."""
    msg = None

    if 'external_id' not in item_dict:
        msg = "Field 'external_id' is required."
    else:
        try:
            item_dict['external_id'] = str(item_dict.get('external_id'))
        except ValueError:
            msg = "Field 'external_id' must be an ascii string."

    if 'name' in item_dict:
        try:
            item_dict['name'] = str(item_dict.get('name'))
        except ValueError:
            msg = "Field 'name' must be an ascii string."

    if 'value' in item_dict:
        try:
            item_dict['value'] = int(item_dict.get('value'))
        except ValueError:
            msg = "Field 'value' must be an integer."

    if msg:
        raise falcon.HTTPBadRequest('Bad request', msg)
    else:
        return item_dict
